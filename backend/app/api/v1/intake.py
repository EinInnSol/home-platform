"""
Intake API endpoints
Handles client intake process via QR codes
"""

from fastapi import APIRouter, HTTPException, status
from typing import Optional
import logging

from app.models.client import ClientCreate, Client, IntakeData
from app.services.database import db_service
from app.services.vi_spdat import vi_spdat_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/intake", tags=["intake"])


@router.post("/start", response_model=dict)
async def start_intake(qr_code: str):
    """
    Start a new intake process by scanning QR code
    
    Returns:
    - qr_code: The QR code scanned
    - organization_id: Organization associated with QR
    - organization_name: Name of organization
    - intake_url: URL to complete intake form
    """
    
    # Get QR code info
    qr_data = await db_service.get_qr_code(qr_code)
    
    if not qr_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid QR code"
        )
    
    # Increment scan count
    await db_service.increment_qr_scan(qr_code)
    
    # Get organization details
    org_data = await db_service.get_organization(qr_data['organization_id'])
    
    if not org_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Organization not found"
        )
    
    return {
        'qr_code': qr_code,
        'organization_id': qr_data['organization_id'],
        'organization_name': org_data.get('name', 'Unknown'),
        'location': qr_data.get('location', 'Unknown'),
        'zone': qr_data.get('zone', 'default'),
        'intake_url': f"/intake/form/{qr_code}"
    }


@router.post("/submit", response_model=Client)
async def submit_intake(client_data: ClientCreate):
    """
    Submit completed intake assessment
    
    Process:
    1. Validate QR code
    2. Calculate VI-SPDAT score
    3. Assign to caseworker based on zone
    4. Create action item for caseworker
    5. Send confirmation to client
    6. Return client record
    """
    
    # Validate QR code
    qr_data = await db_service.get_qr_code(client_data.qr_code)
    if not qr_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid QR code"
        )
    
    # Calculate VI-SPDAT score
    vi_spdat_score = vi_spdat_service.calculate_score(client_data.intake_data)
    
    # Get recommendations
    recommendations = vi_spdat_service.get_intervention_recommendations(
        vi_spdat_score
    )
    
    # Find caseworker for zone
    caseworker = await db_service.get_caseworker_by_zone(
        organization_id=qr_data['organization_id'],
        zone=qr_data.get('zone', 'default')
    )
    
    if not caseworker:
        logger.warning(
            f"No caseworker found for org={qr_data['organization_id']}, "
            f"zone={qr_data.get('zone')}"
        )
        caseworker_id = None
    else:
        caseworker_id = caseworker['id']
    
    # Create client record
    client_dict = client_data.model_dump()
    client_dict['organization_id'] = qr_data['organization_id']
    client_dict['assigned_caseworker_id'] = caseworker_id
    client_dict['vi_spdat_score'] = vi_spdat_score.model_dump()
    client_dict['status'] = 'assessed'  # Automatically assessed
    
    client_id = await db_service.create_client(client_dict)
    
    # Create action item for caseworker
    if caseworker_id:
        action_data = {
            'client_id': client_id,
            'client_name': f"{client_data.first_name} {client_data.last_name}",
            'action_type': 'initial_contact',
            'priority': 5 if vi_spdat_score.acuity_level == 'high' else 3,
            'description': f"New intake: {vi_spdat_score.acuity_level} acuity, "
                          f"score {vi_spdat_score.total_score}/17",
            'recommendations': recommendations
        }
        
        await db_service.create_action_item(caseworker_id, action_data)
    
    # TODO Phase 1: Send SMS/email confirmation
    # TODO Phase 1: Trigger MAYA agent for analysis
    
    logger.info(
        f"Intake completed: client_id={client_id}, "
        f"score={vi_spdat_score.total_score}, "
        f"acuity={vi_spdat_score.acuity_level}"
    )
    
    # Fetch and return full client record
    client_record = await db_service.get_client(client_id)
    return Client(**client_record)


@router.get("/{intake_id}", response_model=dict)
async def get_intake_status(intake_id: str):
    """
    Get status of intake submission
    Allows client to check status after submission
    """
    
    client = await db_service.get_client(intake_id)
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Intake not found"
        )
    
    return {
        'client_id': client['id'],
        'status': client['status'],
        'intake_completed': client.get('intake_completed_at') is not None,
        'caseworker_assigned': client.get('assigned_caseworker_id') is not None,
        'vi_spdat_score': client.get('vi_spdat_score', {}),
        'next_steps': 'Your caseworker will contact you within 24-72 hours.'
    }
