"""
Data models for H.O.M.E. Platform
Pydantic models for API validation and Firestore documents
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class ClientStatus(str, Enum):
    """Client status in the system"""
    INTAKE = "intake"
    ASSESSMENT = "assessment"
    HOUSING_SEARCH = "housing_search"
    HOUSING_MATCHED = "housing_matched"
    HOUSED = "housed"
    INACTIVE = "inactive"

class Gender(str, Enum):
    """Gender options (HUD standard)"""
    MALE = "male"
    FEMALE = "female"
    TRANSGENDER_MALE = "transgender_male"
    TRANSGENDER_FEMALE = "transgender_female"
    NON_BINARY = "non_binary"
    QUESTIONING = "questioning"
    OTHER = "other"
    DECLINED = "declined"

class Race(str, Enum):
    """Race/ethnicity options (HUD standard)"""
    AMERICAN_INDIAN = "american_indian"
    ASIAN = "asian"
    BLACK = "black"
    NATIVE_HAWAIIAN = "native_hawaiian"
    WHITE = "white"
    MULTIPLE = "multiple"
    DECLINED = "declined"

class HousingStatus(str, Enum):
    """Current housing status (HUD standard)"""
    UNSHELTERED = "unsheltered"
    EMERGENCY_SHELTER = "emergency_shelter"
    TRANSITIONAL_HOUSING = "transitional_housing"
    TEMPORARY_WITH_FAMILY = "temporary_with_family"
    TEMPORARY_WITH_FRIENDS = "temporary_with_friends"
    HOTEL = "hotel"
    INSTITUTION = "institution"
    OTHER = "other"

# Base Models
class ClientBase(BaseModel):
    """Base client information"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{10,15}$')
    email: Optional[EmailStr] = None
    date_of_birth: Optional[str] = None  # YYYY-MM-DD format
    gender: Optional[Gender] = None
    race: Optional[Race] = None
    hispanic: Optional[bool] = None
    veteran: Optional[bool] = None

class IntakeAssessment(BaseModel):
    """40 HUD questions - simplified for Phase 0"""
    # Basic Demographics (already in ClientBase)
    
    # Housing History
    current_status: HousingStatus
    nights_homeless: Optional[int] = Field(None, ge=0)
    months_homeless: Optional[int] = Field(None, ge=0)
    times_homeless_past_3_years: Optional[int] = Field(None, ge=0)
    
    # Barriers (VI-SPDAT components)
    health_issues: bool = False
    mental_health_issues: bool = False
    substance_use: bool = False
    medication_needs: bool = False
    physical_disability: bool = False
    developmental_disability: bool = False
    
    # Safety & Risk
    fleeing_violence: bool = False
    legal_issues: bool = False
    
    # Income & Support
    has_income: bool = False
    income_amount: Optional[float] = Field(None, ge=0)
    has_benefits: bool = False
    has_identification: bool = False
    
    # Additional Info
    notes: Optional[str] = Field(None, max_length=2000)

class Client(ClientBase):
    """Full client record"""
    id: str
    status: ClientStatus = ClientStatus.INTAKE
    intake_assessment: Optional[IntakeAssessment] = None
    vi_spdat_score: Optional[int] = Field(None, ge=0, le=17)
    
    # Assignment
    assigned_caseworker_id: Optional[str] = None
    assigned_organization_id: Optional[str] = None
    qr_code_used: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "client_abc123",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+15555551234",
                "status": "intake",
                "vi_spdat_score": 8,
                "created_at": "2025-10-29T10:00:00Z",
                "updated_at": "2025-10-29T10:00:00Z"
            }
        }
