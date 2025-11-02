"""
Client data models for H.O.M.E. Platform
Represents homeless individuals in the system
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List
from pydantic import BaseModel, Field, EmailStr


class ClientStatus(str, Enum):
    """Client status in the system"""
    INTAKE = "intake"                    # Initial intake
    ASSESSED = "assessed"                # VI-SPDAT complete
    MATCHED = "matched"                  # Housing matched
    PLACED = "placed"                    # Housing secured
    FOLLOW_UP = "follow_up"              # Post-placement
    INACTIVE = "inactive"                # No longer active


class HousingType(str, Enum):
    """Types of housing programs"""
    EMERGENCY_SHELTER = "emergency_shelter"
    TRANSITIONAL = "transitional"
    RAPID_REHOUSING = "rapid_rehousing"
    PERMANENT_SUPPORTIVE = "permanent_supportive"
    OTHER = "other"


class ClientBase(BaseModel):
    """Base client information"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = None
    preferred_name: Optional[str] = None
    
    # Contact
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    preferred_contact: str = "phone"  # phone, email, sms
    
    # Demographics (HUD required)
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    race: Optional[List[str]] = None
    ethnicity: Optional[str] = None
    veteran_status: Optional[bool] = None
    
    # Language
    primary_language: str = "english"
    needs_interpreter: bool = False


class IntakeData(BaseModel):
    """40 HUD assessment questions"""
    # This will be populated with actual VI-SPDAT questions
    # For Phase 0, simplified version
    
    # Housing situation
    currently_homeless: bool
    nights_homeless_past_3_years: Optional[int] = None
    living_situation: Optional[str] = None
    
    # Health
    chronic_health: bool = False
    substance_use: bool = False
    mental_health: bool = False
    
    # History
    history_foster_care: bool = False
    history_incarceration: bool = False
    history_victimization: bool = False
    
    # Resources
    has_income: bool = False
    income_source: Optional[str] = None
    monthly_income: Optional[float] = None
    has_id: bool = False
    has_social_security_card: bool = False
    
    # Support
    has_family_support: bool = False
    has_friends_support: bool = False
    
    # Barriers
    transportation_barriers: bool = False
    childcare_barriers: bool = False
    employment_barriers: bool = False
    
    # Additional notes
    additional_info: Optional[str] = None


class VISPDATScore(BaseModel):
    """VI-SPDAT vulnerability assessment score"""
    total_score: int = Field(..., ge=0, le=17)  # 0-17 scale
    housing_history_score: int = Field(..., ge=0)
    wellness_score: int = Field(..., ge=0)
    risk_score: int = Field(..., ge=0)
    
    # Recommendation based on score
    # 0-3: Low acuity
    # 4-7: Medium acuity
    # 8+: High acuity
    acuity_level: str  # low, medium, high
    recommended_housing_type: HousingType
    
    calculated_at: datetime = Field(default_factory=datetime.utcnow)


class ClientCreate(ClientBase):
    """Data needed to create a new client"""
    qr_code: str  # QR code scanned for intake
    intake_data: IntakeData


class ClientUpdate(BaseModel):
    """Data that can be updated"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[ClientStatus] = None
    notes: Optional[str] = None


class Client(ClientBase):
    """Full client record"""
    id: str  # Firestore document ID
    status: ClientStatus = ClientStatus.INTAKE
    
    # Intake info
    intake_completed_at: Optional[datetime] = None
    qr_code: str
    organization_id: str
    assigned_caseworker_id: Optional[str] = None
    
    # Assessment
    intake_data: Optional[IntakeData] = None
    vi_spdat_score: Optional[VISPDATScore] = None
    
    # Housing
    matched_housing_id: Optional[str] = None
    housing_placed_at: Optional[datetime] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Notes
    notes: List[str] = []
    
    class Config:
        from_attributes = True


class ClientListResponse(BaseModel):
    """Paginated list of clients"""
    clients: List[Client]
    total: int
    page: int = 1
    page_size: int = 20
    has_more: bool


class ClientActionItem(BaseModel):
    """Action item for caseworker queue"""
    client_id: str
    client_name: str
    action_type: str  # "initial_contact", "follow_up", "document_needed", etc.
    priority: int  # 1-5, 5 being highest
    due_date: Optional[datetime] = None
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
