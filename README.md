# 🏠 H.O.M.E. Platform

**Housing Opportunity Management Engine**

AI-powered homeless services platform that makes caseworkers superhuman while keeping humans in control.

## 🎯 Mission

Transform homeless services by giving every client a pathway H.O.M.E.

**Built for:** City of Long Beach  
**Demo:** November 15, 2025  
**Opportunity:** $75K Pilot Program

---

## 🏗️ Architecture

### Hybrid Intelligence: 70% Deterministic + 30% AI

**Deterministic Rules Engine:**
- VI-SPDAT scoring
- Eligibility checking
- Program matching
- Compliance validation

**AI Brain (Vertex AI Claude):**
- Complex situation analysis
- Personalized recommendations
- Strategic interventions
- Pattern recognition

### Three AI Agents

1. **MAYA** - Intake Coordinator
2. **SCHEDULER** - Resource Manager
3. **GUARDIAN** - Compliance Officer

---

## 🛠️ Tech Stack

**Frontend:**
- React 18 + TypeScript
- TailwindCSS
- Mobile-first design

**Backend:**
- Python 3.11 FastAPI
- GCP Cloud Run (serverless)
- Firestore + Cloud SQL
- Redis caching

**AI/ML:**
- Vertex AI (Claude via GCP)
- Custom rules engine

**Integrations:**
- Twilio (SMS)
- SendGrid (Email)
- Firebase Auth

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- GCP Account
- Docker (optional)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your API endpoint
npm run dev
```

Frontend runs at `http://localhost:3000`

---

## 📁 Project Structure

```
home-platform/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Config, security
│   │   ├── models/   # Data models
│   │   ├── services/ # Business logic
│   │   └── agents/   # AI agents (Phase 1+)
│   └── tests/
├── frontend/          # React application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── public/
├── infrastructure/    # GCP deployment
│   ├── terraform/
│   └── cloudbuild/
└── docs/             # Documentation
```

---

## 📅 Implementation Phases

- **Phase 0 (Week 1):** Demo Foundation - QR intake + dashboards
- **Phase 1 (Weeks 2-4):** Intelligence - Vertex AI integration
- **Phase 2 (Weeks 5-8):** Agents - Multi-agent orchestration
- **Phase 3 (Weeks 9-10):** Client Portal - Self-service features
- **Phase 4 (Weeks 11-12):** City Oversight - Analytics + reporting
- **Phase 5 (Weeks 13-16):** Learning - System improvements

---

## 🎯 Demo Goals (Nov 15)

- ✅ Working QR code intake flow
- ✅ Caseworker action queue
- ✅ City overview dashboard
- ✅ Mobile-optimized experience
- ✅ Vision clearly communicated

---

## 🤝 Contributing

This is a focused pilot project. Core team only during Phase 0.

---

## 📄 License

Proprietary - Einharjer Innovative Solutions LLC

---

## 🏠 About

**Built by:** Einharjer Innovative Solutions LLC  
**For:** City of Long Beach Homeless Services  
**With:** ❤️ and AI

*Ready to bring everyone H.O.M.E., one person at a time.*
