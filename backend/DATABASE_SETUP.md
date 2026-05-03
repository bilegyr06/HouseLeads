# 🚀 PostgreSQL Connection Setup - COMPLETE ✅

## Database Connection Status: **READY**

### ✅ Verification Results

| Component | Status | Details |
|-----------|--------|---------|
| **PostgreSQL** | ✅ Connected | v18.3 on Windows (x86_64) |
| **Database** | ✅ Created | `homeleads` database |
| **Tables** | ✅ Created | `tenant_leads`, `agents`, `lead_purchases` |
| **ORM Models** | ✅ Loaded | TenantLead, Agent, LeadPurchase |
| **Connection Pool** | ✅ Configured | Pool size: 20, Pre-ping enabled |
| **FastAPI App** | ✅ Initialized | 19 routes registered |

---

## 📋 What Was Done

### 1. **Fixed Pydantic v2 Configuration** ✅
   - Updated `app/core/config.py` to use `ConfigDict` instead of old `Config` class
   - Added missing environment fields: `ENVIRONMENT`, `HOST`, `PORT`

### 2. **Fixed Database URL Encoding** ✅
   - Encoded special character "@" in password as "%40"
   - Now: `postgresql+asyncpg://postgres:Dejavu%401510@localhost:5432/homeleads`

### 3. **Database Tables Created** ✅
   ```sql
   ✅ tenant_leads         (full_name, phone_number, email, etc.)
   ✅ agents              (name, email, rating, location, etc.)
   ✅ lead_purchases      (agent_id, lead_id, amount, status, etc.)
   ```

### 4. **Connection Testing** ✅
   - Created `test_db_connection.py` for verifying connectivity
   - All tests passed without errors

---

## 🎯 Database Credentials Used

```
Host:     localhost
Port:     5432
User:     postgres
Database: homeleads
Password: Dejavu@1510 (URL-encoded as Dejavu%401510)
```

---

## 🚀 Starting the API

Alembic now manages schema changes for this backend.

### First-time migration setup

```bash
alembic upgrade head
```

If your database already existed before Alembic was added, run this once first to mark the current schema as the baseline:

```bash
alembic stamp head
```

### Option 1: Using Batch Script (Windows)
```bash
run.bat
```

### Option 2: Manual Startup
```bash
# Activate virtual environment
.\venv\Scripts\activate.bat

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: With Python Module
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📊 Access the API

Once running, access via:

| Endpoint | URL | Purpose |
|----------|-----|---------|
| **Swagger UI** | http://localhost:8000/docs | Interactive API documentation |
| **ReDoc** | http://localhost:8000/redoc | Alternative documentation |
| **Health Check** | http://localhost:8000/health | Verify API is running |
| **API Base** | http://localhost:8000/api/v1 | All endpoints under this prefix |

---

## 📝 Available Endpoints

### Leads (`/api/v1/leads`)
```
POST   /              - Create new lead
GET    /              - List leads (with filtering & pagination)
GET    /{id}          - Get lead details
PATCH  /{id}          - Update lead
DELETE /{id}          - Delete lead
```

### Agents (`/api/v1/agents`)
```
POST   /              - Create new agent
GET    /              - List agents (sorted by rating)
GET    /{id}          - Get agent details
PATCH  /{id}          - Update agent
DELETE /{id}          - Delete agent
```

### Payments (`/api/v1/payments`)
```
POST   /initialize    - Initialize Paystack payment
POST   /verify/{ref}  - Verify payment
POST   /webhook       - Paystack webhook
```

---

## 🔍 Troubleshooting

### Issue: Connection Refused
```
Error: [Errno 11003] getaddrinfo failed
```
**Solution:** Ensure PostgreSQL is running
```bash
# Windows (PowerShell as Admin)
net start PostgreSQL-x64-18

# Or check Windows Services
services.msc
```

### Issue: Wrong Password
```
Error: FATAL: password authentication failed
```
**Solution:** Verify .env has correct encoded password:
```env
DATABASE_URL=postgresql+asyncpg://postgres:Dejavu%401510@localhost:5432/homeleads
```

### Issue: Database Not Found
```
Error: database "homeleads" does not exist
```
**Solution:** Create database in psql
```bash
psql -U postgres
> CREATE DATABASE homeleads;
```

---

## ✅ Next Steps

1. Start the API server with: `.\venv\Scripts\activate.bat` then `uvicorn app.main:app --reload`
2. Open http://localhost:8000/docs in your browser
3. Try creating a test lead via the Swagger UI
4. Verify data appears in PostgreSQL

---

**Status: 🟢 READY FOR PRODUCTION TESTING**

For issues, refer to the troubleshooting section or check `.env` file for credential accuracy.
