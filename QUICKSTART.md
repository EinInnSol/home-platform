# 🚀 Quick Start - Local Development

Get H.O.M.E. Platform running locally in 5 minutes.

---

## Prerequisites

- Python 3.11+
- GCP account with Firestore enabled
- gcloud CLI configured

---

## Step 1: Clone & Setup (2 minutes)

```bash
# Clone repository
git clone https://github.com/EinInnSol/home-platform.git
cd home-platform/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Configure Environment (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env
nano .env
```

**Minimal .env for local development:**
```bash
DEBUG=true
SECRET_KEY=your-secret-key-here-change-in-production
GCP_PROJECT_ID=your-gcp-project-id
GCP_REGION=us-central1
```

---

## Step 3: Seed Demo Data (1 minute)

```bash
# Set up GCP authentication
gcloud auth application-default login

# Run seed script
cd backend
python scripts/seed_data.py
```

You should see:
```
🌱 Seeding H.O.M.E. Platform demo data...
✅ Demo data seeded successfully!
```

---

## Step 4: Start Server (30 seconds)

```bash
# From backend directory
uvicorn app.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## Step 5: Test API (30 seconds)

Open browser or use curl:

### Health Check
```bash
curl http://localhost:8000/health
```

### API Documentation
Open: http://localhost:8000/docs

### Test Intake Flow

**1. Start intake:**
```bash
curl -X POST "http://localhost:8000/api/v1/intake/start?qr_code=QR001"
```

**2. Submit assessment:**
```bash
curl -X POST "http://localhost:8000/api/v1/intake/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "qr_code": "QR001",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+15555555678",
    "email": "john@example.com",
    "primary_language": "english",
    "intake_data": {
      "currently_homeless": true,
      "nights_homeless_past_3_years": 180,
      "chronic_health": true,
      "substance_use": false,
      "mental_health": true,
      "has_income": false,
      "has_id": true,
      "has_social_security_card": false,
      "has_family_support": false,
      "has_friends_support": true,
      "transportation_barriers": true,
      "childcare_barriers": false,
      "employment_barriers": true,
      "history_foster_care": false,
      "history_incarceration": false,
      "history_victimization": false
    }
  }'
```

**3. Check caseworker queue:**
```bash
curl "http://localhost:8000/api/v1/caseworkers/queue?caseworker_id=cw_demo_1"
```

**4. Get city metrics:**
```bash
curl "http://localhost:8000/api/v1/city/metrics"
```

---

## 📊 Interactive API Testing

Visit: **http://localhost:8000/docs**

This gives you a beautiful interactive API explorer where you can:
- See all endpoints
- Try requests with form inputs
- View responses
- See data models

---

## 🐛 Troubleshooting

### "Firestore connection failed"

**Fix:**
```bash
# Re-authenticate
gcloud auth application-default login

# Verify project
gcloud config get-value project

# Check Firestore exists
gcloud firestore databases list
```

### "Module not found"

**Fix:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify virtual environment is activated
which python  # Should show venv path
```

### "Port 8000 already in use"

**Fix:**
```bash
# Use different port
uvicorn app.main:app --reload --port 8080

# Or kill existing process
lsof -ti:8000 | xargs kill -9  # Mac/Linux
```

---

## 🎯 What to Test

### Intake Flow
1. Start intake with different QR codes (QR001-QR005)
2. Submit with varying VI-SPDAT scores
3. Check assigned caseworkers change based on zone

### VI-SPDAT Scoring
Test different scenarios:
- **High acuity (8+ pts):** chronic_health=true, mental_health=true, nights_homeless_past_3_years=365+
- **Medium acuity (4-7 pts):** some barriers, shorter homelessness
- **Low acuity (0-3 pts):** minimal barriers, recent homelessness

### Caseworker Queue
- Check queue prioritization (high acuity = priority 5)
- Verify action items created automatically
- Test multiple clients assigned to same caseworker

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── core/
│   │   └── config.py        # Settings management
│   ├── models/
│   │   └── client.py        # Data models
│   ├── services/
│   │   ├── database.py      # Firestore operations
│   │   └── vi_spdat.py      # Scoring logic
│   └── api/
│       └── v1/
│           ├── intake.py    # Intake endpoints
│           ├── caseworkers.py  # Caseworker endpoints
│           └── city.py      # City dashboard endpoints
├── scripts/
│   └── seed_data.py         # Demo data seeder
└── requirements.txt         # Python dependencies
```

---

## 🔗 Useful Links

- **API Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **GitHub Repo:** https://github.com/EinInnSol/home-platform

---

## 💡 Pro Tips

1. **Use the interactive docs** - Much easier than curl for testing
2. **Check logs** - API logs everything to console
3. **Firestore Console** - View data in real-time: https://console.firebase.google.com
4. **Hot reload enabled** - Changes to code auto-restart server

---

## 🚀 Next: Deploy to Production

See [DEPLOYMENT.md](DEPLOYMENT.md) for Cloud Run deployment instructions.

---

*Happy coding! Questions? Open an issue on GitHub.* 🏠
