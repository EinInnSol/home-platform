"""
Seed demo data for H.O.M.E. Platform
Run this to populate Firestore with test data for the demo
"""

from google.cloud import firestore
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings

def seed_data():
    """Seed Firestore with demo data"""
    
    print("🌱 Seeding H.O.M.E. Platform demo data...")
    print(f"   Project: {settings.GCP_PROJECT_ID}")
    
    # Initialize Firestore
    db = firestore.Client(
        project=settings.GCP_PROJECT_ID,
        database=settings.FIRESTORE_DATABASE
    )
    
    # 1. Create demo organization
    print("\n📊 Creating organization...")
    org_data = {
        'name': 'Long Beach Demo Services',
        'contact_email': 'demo@longbeach.gov',
        'contact_phone': '+15625551234',
        'address': '333 W Ocean Blvd, Long Beach, CA 90802',
        'zones': ['downtown', 'north', 'west', 'east'],
        'active': True,
        'created_at': datetime.utcnow()
    }
    db.collection('organizations').document('org_demo').set(org_data)
    print("   ✅ Organization: Long Beach Demo Services")
    
    # 2. Create demo caseworkers
    print("\n👥 Creating caseworkers...")
    caseworkers = [
        {
            'id': 'cw_demo_1',
            'name': 'Jane Smith',
            'email': 'jane.smith@demo.com',
            'phone': '+15625551001',
            'organization_id': 'org_demo',
            'assigned_zones': ['downtown', 'north'],
            'active': True,
            'created_at': datetime.utcnow()
        },
        {
            'id': 'cw_demo_2',
            'name': 'Mike Johnson',
            'email': 'mike.johnson@demo.com',
            'phone': '+15625551002',
            'organization_id': 'org_demo',
            'assigned_zones': ['west', 'east'],
            'active': True,
            'created_at': datetime.utcnow()
        }
    ]
    
    for cw in caseworkers:
        cw_id = cw.pop('id')
        db.collection('caseworkers').document(cw_id).set(cw)
        print(f"   ✅ Caseworker: {cw['name']}")
    
    # 3. Create QR codes
    print("\n📱 Creating QR codes...")
    qr_codes = [
        {
            'code': 'QR001',
            'location': 'Main Library - 101 Pacific Ave',
            'zone': 'downtown',
            'lat': 33.7701,
            'lng': -118.1937
        },
        {
            'code': 'QR002',
            'location': 'Community Center - 1150 E 4th St',
            'zone': 'north',
            'lat': 33.7723,
            'lng': -118.1776
        },
        {
            'code': 'QR003',
            'location': 'West Park - 1859 W 25th St',
            'zone': 'west',
            'lat': 33.7969,
            'lng': -118.2134
        },
        {
            'code': 'QR004',
            'location': 'East Bus Terminal - 1498 Long Beach Blvd',
            'zone': 'east',
            'lat': 33.7795,
            'lng': -118.1890
        },
        {
            'code': 'QR005',
            'location': 'Central Shelter - 1335 Pacific Ave',
            'zone': 'downtown',
            'lat': 33.7812,
            'lng': -118.1921
        }
    ]
    
    for qr in qr_codes:
        code = qr['code']
        qr_data = {
            'organization_id': 'org_demo',
            'location': qr['location'],
            'zone': qr['zone'],
            'coordinates': {
                'lat': qr['lat'],
                'lng': qr['lng']
            },
            'scan_count': 0,
            'active': True,
            'created_at': datetime.utcnow(),
            'last_scanned_at': None
        }
        db.collection('qr_codes').document(code).set(qr_data)
        print(f"   ✅ QR Code: {code} at {qr['location']}")
    
    # 4. Create sample housing resources
    print("\n🏠 Creating housing resources...")
    resources = [
        {
            'id': 'housing_001',
            'name': 'Long Beach Emergency Shelter',
            'type': 'emergency_shelter',
            'capacity': 100,
            'available_beds': 12,
            'address': '1335 Pacific Ave, Long Beach, CA 90813',
            'phone': '+15625552000',
            'requirements': ['ID preferred but not required', 'Intake assessment'],
            'services': ['meals', 'showers', 'laundry', 'case_management']
        },
        {
            'id': 'housing_002',
            'name': 'Transitional Living Center',
            'type': 'transitional',
            'capacity': 50,
            'available_beds': 5,
            'address': '456 Elm St, Long Beach, CA 90802',
            'phone': '+15625552001',
            'requirements': ['Background check', 'Employment or job search', 'Sobriety'],
            'services': ['case_management', 'life_skills', 'employment_support']
        }
    ]
    
    for resource in resources:
        resource_id = resource.pop('id')
        resource['created_at'] = datetime.utcnow()
        resource['updated_at'] = datetime.utcnow()
        db.collection('housing_resources').document(resource_id).set(resource)
        print(f"   ✅ Resource: {resource['name']}")
    
    print("\n✅ Demo data seeded successfully!")
    print("\n📋 Summary:")
    print("   • 1 organization")
    print("   • 2 caseworkers")
    print("   • 5 QR codes")
    print("   • 2 housing resources")
    print("\n🎯 Ready for demo!")
    print("\n💡 Test intake URL:")
    print("   https://YOUR-API-URL/api/v1/intake/start?qr_code=QR001")

if __name__ == "__main__":
    try:
        seed_data()
    except Exception as e:
        print(f"\n❌ Error seeding data: {e}")
        print("\nMake sure:")
        print("1. GCP_PROJECT_ID is set in .env")
        print("2. You have Firestore permissions")
        print("3. Application default credentials are set:")
        print("   gcloud auth application-default login")
        sys.exit(1)
