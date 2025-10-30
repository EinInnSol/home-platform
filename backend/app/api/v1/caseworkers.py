"""
Caseworker API endpoints
Handles caseworker dashboard and action queue
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional, List
import logging

from app.models.client import Client, ClientListResponse, ClientActionItem
from app.services.database import db_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/caseworkers", tags=["caseworkers"])


@router.get("/queue", response_model=List[ClientActionItem])
async def get_action_queue(
    caseworker_id: str = Query(..., description="Caseworker ID"),
    completed: bool = Query(False, description="Show completed items"),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Get caseworker's action queue
    
    Returns prioritized list of actions to take:
    - Priority 5: High acuity, immediate contact needed
    - Priority 3: Medium acuity, contact within 72 hours
    - Priority 1: Low acuity, standard follow-up
    """
    
    # Verify caseworker exists
    caseworker = await db_service.get_caseworker(caseworker_id)
    if not caseworker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caseworker not found"
        )
    
    # Get action queue
    queue = await db_service.get_caseworker_queue(
        caseworker_id=caseworker_id,
        completed=completed,
        limit=limit
    )
    
    return [ClientActionItem(**item) for item in queue]


@router.get("/clients", response_model=ClientListResponse)
async def list_assigned_clients(
    caseworker_id: str = Query(..., description="Caseworker ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    List all clients assigned to this caseworker
    """
    
    offset = (page - 1) * page_size
    
    clients = await db_service.list_clients(
        caseworker_id=caseworker_id,
        status=status,
        limit=page_size,
        offset=offset
    )
    
    total = await db_service.count_clients(
        caseworker_id=caseworker_id,
        status=status
    )
    
    return ClientListResponse(
        clients=[Client(**c) for c in clients],
        total=total,
        page=page,
        page_size=page_size,
        has_more=(offset + len(clients)) < total
    )


@router.get("/clients/{client_id}", response_model=Client)
async def get_client_details(
    client_id: str,
    caseworker_id: str = Query(..., description="Caseworker ID")
):
    """
    Get detailed client information
    """
    
    client = await db_service.get_client(client_id)
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Verify caseworker has access
    if client.get('assigned_caseworker_id') != caseworker_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: client not assigned to this caseworker"
        )
    
    return Client(**client)


@router.post("/action/{action_id}/complete")
async def complete_action(
    action_id: str,
    caseworker_id: str = Query(..., description="Caseworker ID"),
    notes: Optional[str] = None
):
    """
    Mark an action item as completed
    """
    
    # TODO: Implement action completion
    # For Phase 0, just acknowledge
    
    return {
        'status': 'completed',
        'action_id': action_id,
        'message': 'Action marked as complete'
    }


@router.get("/stats")
async def get_caseworker_stats(
    caseworker_id: str = Query(..., description="Caseworker ID")
):
    """
    Get caseworker performance statistics
    """
    
    # Get caseworker info
    caseworker = await db_service.get_caseworker(caseworker_id)
    if not caseworker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caseworker not found"
        )
    
    # Count clients by status
    total_clients = len(
        await db_service.list_clients(caseworker_id=caseworker_id, limit=1000)
    )
    
    intake_count = await db_service.count_clients(
        caseworker_id=caseworker_id,
        status='intake'
    )
    assessed_count = await db_service.count_clients(
        caseworker_id=caseworker_id,
        status='assessed'
    )
    matched_count = await db_service.count_clients(
        caseworker_id=caseworker_id,
        status='matched'
    )
    placed_count = await db_service.count_clients(
        caseworker_id=caseworker_id,
        status='placed'
    )
    
    # Get pending actions
    pending_actions = await db_service.get_caseworker_queue(
        caseworker_id=caseworker_id,
        completed=False,
        limit=100
    )
    
    return {
        'caseworker': {
            'id': caseworker_id,
            'name': caseworker.get('name', 'Unknown'),
            'organization': caseworker.get('organization_id')
        },
        'clients': {
            'total': total_clients,
            'by_status': {
                'intake': intake_count,
                'assessed': assessed_count,
                'matched': matched_count,
                'placed': placed_count
            },
            'placement_rate': (placed_count / total_clients * 100) if total_clients > 0 else 0
        },
        'actions': {
            'pending': len(pending_actions),
            'high_priority': len([a for a in pending_actions if a.get('priority', 0) >= 4])
        }
    }
