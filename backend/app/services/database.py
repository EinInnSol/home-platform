"""
Firestore database service
Handles all database operations for H.O.M.E. Platform
"""

from google.cloud import firestore
from google.api_core.exceptions import NotFound
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class FirestoreService:
    """Firestore database operations"""
    
    def __init__(self):
        """Initialize Firestore client"""
        self.db = firestore.Client(
            project=settings.GCP_PROJECT_ID,
            database=settings.FIRESTORE_DATABASE
        )
        logger.info(f"Firestore connected: {settings.GCP_PROJECT_ID}")
    
    # ==================== Client Operations ====================
    
    async def create_client(self, client_data: Dict[str, Any]) -> str:
        """Create a new client record"""
        client_data['created_at'] = datetime.utcnow()
        client_data['updated_at'] = datetime.utcnow()
        
        doc_ref = self.db.collection('clients').document()
        doc_ref.set(client_data)
        
        logger.info(f"Created client: {doc_ref.id}")
        return doc_ref.id
    
    async def get_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get client by ID"""
        doc_ref = self.db.collection('clients').document(client_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return None
        
        data = doc.to_dict()
        data['id'] = doc.id
        return data
    
    async def update_client(
        self, 
        client_id: str, 
        update_data: Dict[str, Any]
    ) -> bool:
        """Update client record"""
        update_data['updated_at'] = datetime.utcnow()
        
        doc_ref = self.db.collection('clients').document(client_id)
        doc_ref.update(update_data)
        
        logger.info(f"Updated client: {client_id}")
        return True
    
    async def list_clients(
        self,
        organization_id: Optional[str] = None,
        caseworker_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """List clients with filters"""
        query = self.db.collection('clients')
        
        if organization_id:
            query = query.where('organization_id', '==', organization_id)
        if caseworker_id:
            query = query.where('assigned_caseworker_id', '==', caseworker_id)
        if status:
            query = query.where('status', '==', status)
        
        # Order by created date (newest first)
        query = query.order_by('created_at', direction=firestore.Query.DESCENDING)
        query = query.limit(limit).offset(offset)
        
        docs = query.stream()
        
        clients = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            clients.append(data)
        
        return clients
    
    async def count_clients(
        self,
        organization_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> int:
        """Count clients with filters"""
        query = self.db.collection('clients')
        
        if organization_id:
            query = query.where('organization_id', '==', organization_id)
        if status:
            query = query.where('status', '==', status)
        
        # Get count
        docs = list(query.stream())
        return len(docs)
    
    # ==================== QR Code Operations ====================
    
    async def get_qr_code(self, qr_code: str) -> Optional[Dict[str, Any]]:
        """Get QR code info"""
        doc_ref = self.db.collection('qr_codes').document(qr_code)
        doc = doc_ref.get()
        
        if not doc.exists:
            return None
        
        return doc.to_dict()
    
    async def increment_qr_scan(self, qr_code: str):
        """Increment scan count for QR code"""
        doc_ref = self.db.collection('qr_codes').document(qr_code)
        doc_ref.update({
            'scan_count': firestore.Increment(1),
            'last_scanned_at': datetime.utcnow()
        })
    
    # ==================== Organization Operations ====================
    
    async def get_organization(
        self, 
        organization_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get organization by ID"""
        doc_ref = self.db.collection('organizations').document(organization_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return None
        
        return doc.to_dict()
    
    # ==================== Caseworker Operations ====================
    
    async def get_caseworker(
        self, 
        caseworker_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get caseworker by ID"""
        doc_ref = self.db.collection('caseworkers').document(caseworker_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return None
        
        return doc.to_dict()
    
    async def get_caseworker_by_zone(
        self,
        organization_id: str,
        zone: str
    ) -> Optional[Dict[str, Any]]:
        """Find available caseworker for zone"""
        query = self.db.collection('caseworkers')
        query = query.where('organization_id', '==', organization_id)
        query = query.where('assigned_zones', 'array_contains', zone)
        query = query.limit(1)
        
        docs = list(query.stream())
        if not docs:
            return None
        
        data = docs[0].to_dict()
        data['id'] = docs[0].id
        return data
    
    # ==================== Action Queue Operations ====================
    
    async def create_action_item(
        self,
        caseworker_id: str,
        action_data: Dict[str, Any]
    ) -> str:
        """Create action item for caseworker"""
        action_data['created_at'] = datetime.utcnow()
        action_data['completed'] = False
        
        doc_ref = self.db.collection('caseworkers').document(caseworker_id)
        doc_ref = doc_ref.collection('action_queue').document()
        doc_ref.set(action_data)
        
        return doc_ref.id
    
    async def get_caseworker_queue(
        self,
        caseworker_id: str,
        completed: bool = False,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get caseworker's action queue"""
        doc_ref = self.db.collection('caseworkers').document(caseworker_id)
        query = doc_ref.collection('action_queue')
        query = query.where('completed', '==', completed)
        query = query.order_by('priority', direction=firestore.Query.DESCENDING)
        query = query.order_by('created_at')
        query = query.limit(limit)
        
        docs = query.stream()
        
        items = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            items.append(data)
        
        return items
    
    # ==================== Analytics Operations ====================
    
    async def get_city_metrics(self) -> Dict[str, Any]:
        """Get citywide metrics for dashboard"""
        # Count total clients
        total_clients = await self.count_clients()
        
        # Count by status
        intake_count = await self.count_clients(status='intake')
        assessed_count = await self.count_clients(status='assessed')
        matched_count = await self.count_clients(status='matched')
        placed_count = await self.count_clients(status='placed')
        
        return {
            'total_clients': total_clients,
            'by_status': {
                'intake': intake_count,
                'assessed': assessed_count,
                'matched': matched_count,
                'placed': placed_count
            },
            'placement_rate': (placed_count / total_clients * 100) if total_clients > 0 else 0
        }


# Global Firestore instance
db_service = FirestoreService()
