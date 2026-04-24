# HomeLeads API

A FastAPI-based real estate lead matching and management platform for Nigeria. Intelligently matches tenant leads with real estate agents based on location, budget, and agent ratings.

---

## Quick Start

### Prerequisites
- Python 3.10 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### 1. Clone & Setup

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example to actual .env
cp .env.example .env

# Edit .env with your actual values:
# - DATABASE_URL (PostgreSQL connection)
# - PAYSTACK_SECRET_KEY & PAYSTACK_PUBLIC_KEY
# - JWT_SECRET_KEY
```

### 5. Start the Application

**Windows:**
```bash
run.bat
```

**Linux/macOS:**
```bash
bash run.sh
```

**Or manually:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access the API

- **API Documentation (Swagger):** http://localhost:8000/docs
- **API Schema (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health
- **API Base:** http://localhost:8000/api/v1

---

## Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py           # Environment configuration
│   │   ├── database.py         # SQLAlchemy async setup
│   │   └── security.py         # JWT auth (future)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── agent.py            # Agent ORM model
│   │   ├── tenant_lead.py      # Tenant lead ORM model
│   │   ├── lead_purchase.py    # Purchase records
│   │   └── lead_match.py       # Match history
│   ├── schemas/
│   │   ├── agent.py            # Agent request/response schemas
│   │   ├── tenant_lead.py      # Lead request/response schemas
│   │   └── payment.py          # Payment schemas
│   ├── services/
│   │   ├── matching.py         # Lead-to-agent matching algorithm
│   │   └── whatsapp_service.py # WhatsApp notifications (placeholder)
│   ├── routes/
│   │   ├── agents.py           # Agent CRUD endpoints
│   │   ├── leads.py            # Lead CRUD endpoints
│   │   └── payments.py         # Payment integration endpoints
│   ├── utils/
│   │   └── helpers.py          # Utility functions
│   └── main.py                 # FastAPI app initialization
├── alembic/                    # Database migrations
├── .env                        # Environment variables (git-ignored)
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows startup script
├── run.sh                      # Linux/macOS startup script
└── README.md                   # This file
```

---

## 🔌 API Endpoints

### Health & Info
- `GET /` - API information
- `GET /health` - Health check

### Leads (`/api/v1/leads`)
- `POST /` - Create new lead
- `GET /` - List leads (with filtering & pagination)
- `GET /{id}` - Get lead details
- `PATCH /{id}` - Update lead
- `DELETE /{id}` - Delete lead (soft delete)

### Agents (`/api/v1/agents`)
- `POST /` - Create new agent
- `GET /` - List agents (sorted by rating)
- `GET /{id}` - Get agent details
- `PATCH /{id}` - Update agent
- `DELETE /{id}` - Delete agent (soft delete)

### Payments (`/api/v1/payments`)
- `POST /initialize` - Initialize Paystack payment
- `POST /verify/{reference}` - Verify payment
- `POST /webhook` - Paystack webhook endpoint

---

## Lead Matching Algorithm

Matches leads to agents using weighted scoring:

```
Match Score = (40% × Location) + (30% × Rating) + (20% × Quality) + (10% × Conversion)
```

- **Location Score (40%):** 1.0 (same), 0.7 (nearby), 0.0 (far)
- **Rating Score (30%):** Agent rating / 5.0
- **Lead Quality (20%):** 1.0 (high), 0.5 (medium), 0.0 (low)
- **Conversion Rate (10%):** Leads converted / Total leads

---

## Database Schema

### Tables

#### `agents`
- `id` (Integer, PK)
- `name`, `email` (unique), `phone` (unique)
- `location`, `rating`, `specialization`
- `total_leads_matched`, `total_leads_converted`
- `is_active` (soft delete)
- `created_at`, `updated_at`

#### `tenant_leads`
- `id` (Integer, PK)
- `email` (unique), `phone` (unique, Nigerian format)
- `location`, `budget_min`, `budget_max`
- `lead_quality`, `status`
- `lead_score` (0-100, calculated on creation)
- `move_in_date`
- `created_at`, `updated_at`

#### `lead_purchases`
- `id` (Integer, PK)
- `agent_id` (FK), `lead_id` (FK)
- `amount`, `payment_reference`, `status`
- Unique index on (agent_id, lead_id)
- `created_at`, `updated_at`

#### `lead_matches`
- `id` (Integer, PK)
- `lead_id` (FK), `agent_id` (FK)
- `match_score` (0.0-1.0), `match_reason`
- `status` (matched, contacted, interested, purchased, rejected)
- Unique index on (lead_id, agent_id)
- `created_at`, `updated_at`

---

## Security Notes

- **Database URLs:** Use strong passwords, never commit .env
- **JWT Secrets:** Change `JWT_SECRET_KEY` in production
- **Paystack Keys:** Use test keys for development, live keys for production
- **CORS:** Update `allow_origins` in `app/main.py` for production frontend URL

---

## Installing New Dependencies

```bash
pip install <package_name>
pip freeze > requirements.txt
```

---

## Troubleshooting

### Database Connection Error
```
Check DATABASE_URL in .env
Ensure PostgreSQL is running
Verify credentials and database exists
```

### Port 8000 Already in Use
```bash
uvicorn app.main:app --reload --port 8001
```

### Virtual Environment Not Activating
```bash
# Linux/macOS
source venv/bin/activate

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat
```

---

## Deployment

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Using Docker
```bash
docker build -t homeleads .
docker run -p 8000:8000 --env-file .env homeleads
```

---

## License

Proprietary - HomeLeads

---

## Support

For issues or questions, contact: support homeleads.com
