# 🚀 H.O.M.E. Platform Deployment Guide

## Phase 0: Quick Start for Demo

This guide will get you from zero to deployed in under an hour.

---

## Prerequisites

- GCP Account with billing enabled
- Python 3.11+ installed locally
- Node.js 18+ installed locally
- Git installed
- gcloud CLI installed ([install guide](https://cloud.google.com/sdk/docs/install))

---

## Part 1: GCP Project Setup (10 minutes)

### 1.1 Create GCP Project

```bash
# Set your project ID (must be globally unique)
export PROJECT_ID="home-platform-demo"
export REGION="us-central1"

# Create project
gcloud projects create $PROJECT_ID --name="H.O.M.E. Platform"

# Set as active project
gcloud config set project $PROJECT_ID

# Enable billing (do this via console if not already done)
# https://console.cloud.google.com/billing
```

### 1.2 Enable Required APIs

```bash
# Enable all necessary GCP services
gcloud services enable \ 
  run.googleapis.com \
  firestore.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  compute.googleapis.com
```

### 1.3 Create Firestore Database

```bash
# Create Firestore in Native mode
gcloud firestore databases create \
  --region=$REGION \
  --type=firestore-native
```

### 1.4 Set Up Service Account

```bash
# Create service account
gcloud iam service-accounts create home-platform-sa \
  --display-name="H.O.M.E. Platform Service Account"

# Grant necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:home-platform-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/datastore.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:home-platform-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

---

## Part 2: Backend Deployment (15 minutes)

### 2.1 Clone Repository

```bash
git clone https://github.com/EinInnSol/home-platform.git
cd home-platform
```

### 2.2 Configure Environment

```bash
cd backend

# Copy environment template
cp .env.example .env

# Edit .env file
nano .env  # or use your preferred editor
```

**Required .env values:**
```bash
DEBUG=false
SECRET_KEY=$(openssl rand -hex 32)
GCP_PROJECT_ID=your-project-id-here
GCP_REGION=us-central1
```

### 2.3 Store Secrets in GCP Secret Manager

```bash
# Store secret key
echo -n "your-secret-key-from-env" | gcloud secrets create secret-key --data-file=-

# Grant access to Cloud Run
gcloud secrets add-iam-policy-binding secret-key \
  --member="serviceAccount:home-platform-sa@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 2.4 Deploy to Cloud Run

```bash
# Build and deploy
gcloud run deploy home-platform-api \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --service-account home-platform-sa@$PROJECT_ID.iam.gserviceaccount.com \
  --set-env-vars="GCP_PROJECT_ID=$PROJECT_ID,GCP_REGION=$REGION" \
  --set-secrets="SECRET_KEY=secret-key:latest" \
  --max-instances 10 \
  --memory 512Mi \
  --cpu 1

# Get service URL
gcloud run services describe home-platform-api \
  --platform managed \
  --region $REGION \
  --format="value(status.url)"
```

Save this URL! You'll need it for the frontend.

### 2.5 Test API

```bash
# Health check
curl https://YOUR-CLOUD-RUN-URL/health

# Should return:
# {"status":"healthy","database":"connected","cache":"connected"}
```

---

## Part 3: Seed Demo Data (10 minutes)

### 3.1 Create Test Organization

```python
# Run this Python script locally
from google.cloud import firestore
import os

# Set your project ID
os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project-id'

db = firestore.Client()

# Create test organization
org_ref = db.collection('organizations').document('org_demo')
org_ref.set({
    'name': 'Long Beach Demo Services',
    'contact': 'demo@longbeach.gov',
    'zones': ['downtown', 'north', 'west', 'east'],
    'active': True
})

# Create test caseworker
cw_ref = db.collection('caseworkers').document('cw_demo')
cw_ref.set({
    'name': 'Jane Demo',
    'email': 'jane@demo.com',
    'phone': '+15555551234',
    'organization_id': 'org_demo',
    'assigned_zones': ['downtown', 'north']
})

# Create test QR codes
qr_codes = [
    {'code': 'QR001', 'location': 'Main Library', 'zone': 'downtown'},
    {'code': 'QR002', 'location': 'Community Center', 'zone': 'north'},
    {'code': 'QR003', 'location': 'West Park', 'zone': 'west'},
]

for qr in qr_codes:
    qr_ref = db.collection('qr_codes').document(qr['code'])
    qr_ref.set({
        'organization_id': 'org_demo',
        'location': qr['location'],
        'zone': qr['zone'],
        'scan_count': 0,
        'active': True
    })

print("✅ Demo data created!")
```

---

## Part 4: Frontend Setup (Phase 0 - Optional)

**Note:** For the Nov 15 demo, you can test the API with Postman/curl first, then build the React frontend in the next session.

### 4.1 Basic React Setup (coming next)

```bash
cd frontend
npm install
cp .env.example .env.local

# Edit .env.local with your API URL
echo "VITE_API_URL=https://YOUR-CLOUD-RUN-URL" > .env.local

npm run dev
```

---

## Part 5: Testing the Demo Flow (5 minutes)

### Test 1: Start Intake

```bash
curl -X POST "https://YOUR-API-URL/api/v1/intake/start?qr_code=QR001"
```

### Test 2: Submit Intake

```bash
curl -X POST "https://YOUR-API-URL/api/v1/intake/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "qr_code": "QR001",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+15555555678",
    "email": "john@example.com",
    "intake_data": {
      "currently_homeless": true,
      "nights_homeless_past_3_years": 180,
      "chronic_health": true,
      "substance_use": false,
      "mental_health": true,
      "has_income": false,
      "has_id": true,
      "has_social_security_card": false
    }
  }'
```

### Test 3: Check Caseworker Queue

```bash
curl "https://YOUR-API-URL/api/v1/caseworkers/queue?caseworker_id=cw_demo"
```

### Test 4: City Metrics

```bash
curl "https://YOUR-API-URL/api/v1/city/metrics"
```

---

## Troubleshooting

### API Returns 500 Error

**Check logs:**
```bash
gcloud run services logs read home-platform-api \
  --limit 50 \
  --region $REGION
```

### Firestore Connection Issues

**Verify Firestore is created:**
```bash
gcloud firestore databases list
```

**Check service account permissions:**
```bash
gcloud projects get-iam-policy $PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:home-platform-sa*"
```

### Cost Monitoring

**Check current costs:**
```bash
gcloud billing accounts list
```

**Set budget alert (recommended):**
- Go to: https://console.cloud.google.com/billing/budgets
- Create budget: $50/month with 50%, 90%, 100% alerts

---

## Next Steps

1. ✅ Backend API deployed and tested
2. ⏭️ Build React frontend (next session)
3. ⏭️ Create mobile-optimized intake form
4. ⏭️ Build caseworker dashboard
5. ⏭️ Create city overview dashboard
6. ⏭️ Prepare demo script

---

## Demo Day Checklist (Nov 15)

- [ ] API deployed and healthy
- [ ] Demo data seeded
- [ ] Frontend deployed
- [ ] QR codes generated and printed
- [ ] Test full flow: QR scan → intake → queue → dashboard
- [ ] Backup plan: Postman collection + slides
- [ ] 10-minute pitch prepared
- [ ] Questions anticipated and answered

---

## Support

**Issues:** https://github.com/EinInnSol/home-platform/issues  
**Docs:** https://github.com/EinInnSol/home-platform/tree/main/docs

---

*You've got this! Let's bring everyone H.O.M.E.* 🏠
