"""
H.O.M.E. Platform - Housing Opportunity Management Engine
Main FastAPI application entry point

Phase 0: Demo Foundation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="H.O.M.E. Platform API",
    description="Housing Opportunity Management Engine - AI-powered homeless services",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "name": "H.O.M.E. Platform API",
        "version": "0.1.0",
        "status": "operational",
        "phase": "Phase 0 - Demo Foundation",
        "demo_date": "November 15, 2025"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Import and include routers (Phase 0)
# from app.api import intake, clients, caseworkers, city
# app.include_router(intake.router, prefix="/api/v1/intake", tags=["intake"])
# app.include_router(clients.router, prefix="/api/v1/clients", tags=["clients"])
# app.include_router(caseworkers.router, prefix="/api/v1/caseworkers", tags=["caseworkers"])
# app.include_router(city.router, prefix="/api/v1/city", tags=["city"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
