"""
Client Portal API endpoints
Handles client authentication and self-service features
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from datetime import datetime
import logging
import secrets

from app.services.database import db_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/client", tags=["client"])


@router.post("/auth/login")
async def client_login(
    confirmation_code: str = Query(..., description="Confirmation code from intake"),
    phone_last4: str = Query(..., min_length=4, max_length=4, description="Last 4 digits of phone")
):
    """
    Client authentication using confirmation code + phone verification
    
    Simple auth for Phase 0:
    - No passwords required
    - Just confirmation code + last 4 of phone
    - Returns client_id for subsequent requests
    
    Phase 1+ will add:
    - SMS verification codes
    - JWT tokens
    - More secure session management
    """
    
    # Search for client by confirmation code
    # TODO: Add index on confirmation_code in Firestore for performance
    clients = await db_service.list_clients(limit=1000)
    
    matching_client = None
    for client in clients:
        if client.get('confirmation_code') == confirmation_code:
            # Verify last 4 of phone matches
            client_phone = client.get('phone', '')
            if client_phone.endswith(phone_last4):
                matching_client = client
                break
    
    if not matching_client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid confirmation code or phone number"
        )
    
    # Log successful login
    logger.info(f"Client login successful: {matching_client['id']}")
    
    return {
        'authenticated': True,
        'client_id': matching_client['id'],
        'message': 'Login successful',
        # Phase 1: Return JWT token here
    }


@router.get("/profile/{client_id}")
async def get_client_profile(client_id: str):
    """
    Get client's own profile information
    
    Returns:
    - Basic client info
    - Current status
    - Assigned caseworker
    - Organization info
    - VI-SPDAT score (if assessed)
    """
    
    client = await db_service.get_client(client_id)
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Get caseworker info if assigned
    caseworker = None
    if client.get('assigned_caseworker_id'):
        caseworker = await db_service.get_caseworker(
            client['assigned_caseworker_id']
        )
    
    # Get organization info
    organization = None
    if client.get('organization_id'):
        organization = await db_service.get_organization(
            client['organization_id']
        )
    
    return {
        'client': {
            'id': client['id'],
            'first_name': client.get('first_name'),
            'preferred_name': client.get('preferred_name'),
            'status': client.get('status'),
            'created_at': client.get('created_at'),
        },
        'caseworker': {
            'name': caseworker.get('name') if caseworker else None,
            'phone': caseworker.get('phone') if caseworker else None,
            'email': caseworker.get('email') if caseworker else None,
        } if caseworker else None,
        'organization': {
            'name': organization.get('name') if organization else None,
            'contact_phone': organization.get('contact_phone') if organization else None,
        } if organization else None,
        'assessment': {
            'vi_spdat_score': client.get('vi_spdat_score'),
            'acuity_level': client.get('vi_spdat_score', {}).get('acuity_level'),
        } if client.get('vi_spdat_score') else None
    }


@router.get("/progress/{client_id}")
async def get_client_progress(client_id: str):
    """
    Get client's progress through the housing process
    
    Returns milestone-based progress tracking:
    - Intake complete
    - Caseworker assigned
    - Assessment complete
    - Housing matched
    - Move-in scheduled
    - Housed successfully
    
    Calculates completion percentage and next steps
    """
    
    client = await db_service.get_client(client_id)
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Define milestone progression
    milestones = [
        {
            'step': 'Intake Complete',
            'completed': client.get('intake_completed_at') is not None,
            'date': client.get('intake_completed_at'),
            'icon': '✓',
            'description': 'Your information has been submitted'
        },
        {
            'step': 'Caseworker Assigned',
            'completed': client.get('assigned_caseworker_id') is not None,
            'date': client.get('created_at') if client.get('assigned_caseworker_id') else None,
            'icon': '👤',
            'description': 'A caseworker is reviewing your case'
        },
        {
            'step': 'Assessment Complete',
            'completed': client.get('status') in ['assessed', 'matched', 'placed'],
            'date': client.get('created_at') if client.get('status') != 'intake' else None,
            'icon': '📋',
            'description': 'Your needs have been evaluated'
        },
        {
            'step': 'Housing Match Found',
            'completed': client.get('status') in ['matched', 'placed'],
            'date': client.get('matched_housing_id') if client.get('matched_housing_id') else None,
            'icon': '🏠',
            'description': 'We found housing that fits your needs'
        },
        {
            'step': 'Move-In Process',
            'completed': client.get('status') == 'placed',
            'date': client.get('housing_placed_at'),
            'icon': '🔑',
            'description': 'Preparing for your move-in'
        }
    ]
    
    # Calculate completion percentage
    completed_count = sum(1 for m in milestones if m['completed'])
    total_count = len(milestones)
    completion_percentage = int((completed_count / total_count) * 100)
    
    # Determine current step and next action
    current_step = None
    next_action = None
    
    for i, milestone in enumerate(milestones):
        if not milestone['completed']:
            current_step = milestone['step']
            if i == 0:
                next_action = "Complete your intake assessment"
            elif i == 1:
                next_action = "Your caseworker will contact you within 24-72 hours"
            elif i == 2:
                next_action = "Your caseworker is reviewing your assessment"
            elif i == 3:
                next_action = "Searching for housing matches"
            elif i == 4:
                next_action = "Preparing move-in paperwork"
            break
    
    if current_step is None:
        current_step = "Housed Successfully"
        next_action = "Congratulations! Stay in touch with your caseworker."
    
    return {
        'completion_percentage': completion_percentage,
        'current_step': current_step,
        'next_action': next_action,
        'milestones': milestones,
        'estimated_time_to_housing': '30-45 days',  # TODO: Make dynamic based on acuity
        'status': client.get('status')
    }


@router.get("/caseworker/{client_id}")
async def get_client_caseworker(client_id: str):
    """
    Get detailed information about client's assigned caseworker
    
    Returns:
    - Caseworker name, contact info
    - Office hours
    - Best way to reach them
    - Response time expectations
    """
    
    client = await db_service.get_client(client_id)
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    if not client.get('assigned_caseworker_id'):
        return {
            'assigned': False,
            'message': 'A caseworker will be assigned within 24 hours'
        }
    
    caseworker = await db_service.get_caseworker(
        client['assigned_caseworker_id']
    )
    
    if not caseworker:
        return {
            'assigned': False,
            'message': 'Caseworker information not available'
        }
    
    return {
        'assigned': True,
        'caseworker': {
            'name': caseworker.get('name'),
            'phone': caseworker.get('phone'),
            'email': caseworker.get('email'),
            'organization': caseworker.get('organization_id'),
            'office_hours': '9:00 AM - 5:00 PM, Monday-Friday',  # TODO: Make dynamic
            'response_time': '24-48 hours',  # TODO: Make dynamic
            'preferred_contact': 'Phone call or text message'  # TODO: Make dynamic
        }
    }


@router.get("/resources/{client_id}")
async def get_nearby_resources(
    client_id: str,
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    radius_miles: float = Query(5.0, ge=1.0, le=50.0)
):
    """
    Get nearby resources and services
    
    Returns list of:
    - Emergency shelters
    - Food banks
    - Health clinics
    - Support services
    
    Filtered by distance from client's location
    Phase 0: Returns static list
    Phase 2: Returns dynamic based on geolocation
    """
    
    client = await db_service.get_client(client_id)
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Phase 0: Return static resources for Long Beach
    # Phase 2: Query Firestore with geolocation
    resources = [
        {
            'name': 'Long Beach Rescue Mission',
            'type': 'emergency_shelter',
            'address': '1335 Pacific Ave, Long Beach, CA 90813',
            'phone': '+15624351357',
            'hours': '24/7',
            'services': ['shelter', 'meals', 'showers', 'case_management'],
            'distance_miles': 1.2,
            'walking_time': '15 minutes'
        },
        {
            'name': 'Long Beach Community Health Center',
            'type': 'health_clinic',
            'address': '1333 Chestnut Ave, Long Beach, CA 90813',
            'phone': '+15624341234',
            'hours': 'Mon-Fri 8am-5pm',
            'services': ['primary_care', 'mental_health', 'dental'],
            'distance_miles': 0.8,
            'walking_time': '10 minutes'
        },
        {
            'name': 'Long Beach Food Bank',
            'type': 'food_bank',
            'address': '4545 Long Beach Blvd, Long Beach, CA 90805',
            'phone': '+15625674124',
            'hours': 'Mon-Wed-Fri 9am-12pm',
            'services': ['food_pantry', 'hot_meals'],
            'distance_miles': 2.1,
            'walking_time': '25 minutes'
        }
    ]
    
    return {
        'client_location': {
            'latitude': latitude,
            'longitude': longitude
        } if latitude and longitude else None,
        'search_radius_miles': radius_miles,
        'resources': resources,
        'total_count': len(resources)
    }
