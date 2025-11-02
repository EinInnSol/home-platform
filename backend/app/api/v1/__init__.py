"""
API v1 router aggregation
Combines all API endpoints
"""

from fastapi import APIRouter

from app.api.v1 import intake, caseworkers, city

# Create main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(intake.router)
api_router.include_router(caseworkers.router)
api_router.include_router(city.router)
