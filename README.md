# HomeLeads
HomeLeads is a real estate lead capture and matching platform for Lagos. It combines a React front end for tenant intake with a FastAPI backend that stores leads in PostgreSQL, scores them, and prepares them for agent matching and payment workflows.

## Problem
Finding rental property in Lagos is often fragmented, slow, and noisy. Tenants fill out repeated forms, while agents spend time sorting low-quality inquiries and manually following up on leads.

## Solution
HomeLeads centralizes tenant intake into a guided form, normalizes the submitted data, and stores it in a structured backend. The backend computes a lead score, exposes CRUD APIs for leads and agents, and scaffolds the matching, payment, and notification flows needed for a brokerage workflow.

## Features
- Multi-step tenant lead form with client-side validation.
- Nigerian phone-number normalization and location standardization.
- Lead scoring based on budget, urgency, location, and property type.
- FastAPI backend with async SQLAlchemy and PostgreSQL.
- Agent signup and login endpoints with JWT-based auth scaffolding.
- CRUD endpoints for leads and agents.
- Paystack payment endpoints scaffolded for lead purchase flows.
- Alembic migrations for schema management.
- Soft delete for agents and status tracking for leads.

## Architecture
HomeLeads is structured as a small full-stack monorepo.

- `frontend/` contains the Vite + React app used by tenants.
- `backend/` contains the FastAPI service, ORM models, schemas, routes, and business logic.
- PostgreSQL is the primary datastore for leads, agents, purchases, and match history.
- Rule-based scoring is used instead of an ML model. Lead quality is computed from form inputs and matching is handled by deterministic heuristics.
- External integrations are scaffolded for Paystack and WhatsApp, but the current implementation still uses placeholder behavior in those paths.

A notable implementation choice is that lead creation persists the submission and computes a score first; automated agent matching and WhatsApp notifications are present in the codebase but are not fully wired into the lead-creation flow yet. That keeps the MVP stable while the surrounding workflows are completed.

## Tech Stack

### Frontend
- React 19
- TypeScript
- Vite
- React Router
- Axios
- Lucide React
- Tailwind CSS v4 tooling, with most styling defined in custom CSS

### Backend
- FastAPI
- Uvicorn
- SQLAlchemy 2 async ORM
- asyncpg
- Alembic
- Pydantic v2 and pydantic-settings
- python-jose for JWT support
- Passlib with Argon2 password hashing
- python-dotenv
- structlog

### Database
- PostgreSQL
- Alembic-managed schema migrations

### Deployment
- Vercel configuration is present in `vercel.json`
- The config serves the frontend at `/` and exposes the Python backend service under `/_/backend`
- The backend still requires a reachable PostgreSQL instance and the expected environment variables at runtime

## Project Structure

- `backend/app/main.py` is the FastAPI entry point and router registration point.
- `backend/app/core/` contains configuration, database setup, and auth helpers.
- `backend/app/models/` contains SQLAlchemy ORM models for agents, tenant leads, purchases, and lead matches.
- `backend/app/schemas/` contains Pydantic request and response models.
- `backend/app/routes/` contains the API endpoints for auth, leads, agents, and payments.
- `backend/app/services/` contains scoring, matching, and WhatsApp service logic.
- `backend/app/utils/helpers.py` contains phone and location normalization helpers.
- `backend/alembic/` contains the migration environment and revisions.
- `frontend/src/pages/` contains the landing page, lead form, and confirmation screen.
- `frontend/src/services/api.ts` contains the Axios client used by the form.
- `frontend/src/assets/` contains static assets used by the React app.

## Installation

### Prerequisites
- Python 3.10 or newer
- Node.js 18 or newer
- PostgreSQL 12 or newer
- npm

### 1. Clone the repository
```bash
git clone <repo-url>
cd HouseLeads
```

### 2. Configure the backend
```bash
cd backend
python -m venv venv
```

Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Create a `backend/.env` file with at least the following values:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/homeleads
PAYSTACK_SECRET_KEY=your_paystack_secret_key
PAYSTACK_PUBLIC_KEY=your_paystack_public_key
JWT_SECRET_KEY=your_long_random_secret
DEBUG=true
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
```

Run the database migrations:

```bash
alembic upgrade head
```

Start the backend:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You can also use `run.bat` on Windows or `run.sh` on macOS/Linux.

### 3. Configure the frontend
Open a new terminal and run:

```bash
cd frontend
npm install
```

Create a `frontend/.env` file if the API is not running at the default address:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Start the frontend:

```bash
npm run dev
```

## Usage
1. Open the frontend in the browser.
2. Start on the landing page and click through to the multi-step lead form.
3. Select preferred locations, property type, budget, move-in date, and contact details.
4. Submit the form to create a tenant lead in the backend.
5. Review the confirmation screen after a successful submission.

The backend also exposes Swagger UI at `/docs` and ReDoc at `/redoc` for manual API exploration.

Screenshots: none are currently committed. Add application screenshots under `docs/images/` and reference them here once they are available.

## API
All backend routes are versioned under `/api/v1`.

### Health
- `GET /` returns basic API metadata.
- `GET /health` returns a lightweight health check.

### Authentication
- `POST /api/v1/auth/signup` creates an agent account.
- `POST /api/v1/auth/login` authenticates an agent and returns a JWT access token.

### Leads
- `POST /api/v1/leads/` creates a tenant lead.
- `GET /api/v1/leads/` lists leads with optional status and location filters.
- `GET /api/v1/leads/{lead_id}` returns one lead.
- `PATCH /api/v1/leads/{lead_id}` updates lead status.
- `DELETE /api/v1/leads/{lead_id}` deletes a lead.

### Agents
- `POST /api/v1/agents/` creates an agent.
- `GET /api/v1/agents/` lists agents with optional filters.
- `GET /api/v1/agents/{agent_id}` returns one agent.
- `PATCH /api/v1/agents/{agent_id}` updates an agent.
- `DELETE /api/v1/agents/{agent_id}` soft-deletes an agent by marking it inactive.

### Payments
- `POST /api/v1/payments/initialize` scaffolds a Paystack payment initialization response.
- `POST /api/v1/payments/verify/{reference}` returns a mock verification response.
- `POST /api/v1/payments/webhook` is the webhook entry point for Paystack events.

## Machine Learning Details
No machine learning model is implemented in the current repository.

Lead scoring and agent matching are rule-based:
- `backend/app/services/lead_scoring.py` computes a 0-100 lead score from budget, move-in urgency, preferred location, and property type.
- `backend/app/services/matching.py` computes a weighted match score from location proximity, agent rating, lead score, and conversion rate.

If a model is added later, this section should be expanded with the training data, preprocessing steps, evaluation metrics, and inference pipeline.

## Future Improvements
- Wire the lead-creation route to persist lead matches and notify matched agents.
- Replace the Paystack placeholders with the real SDK flow and webhook handling.
- Add an agent dashboard for managing matched leads and purchase history.
- Add automated tests for the API routes and the matching logic.
- Add a persisted audit trail for lead status changes.
- Add documented environment templates for both backend and frontend.
- Add screenshots and a short product walkthrough to the repository.

## Contributing
1. Fork the repository.
2. Create a feature branch.
3. Make focused changes and keep the API contracts stable where possible.
4. Run the backend and frontend checks before opening a pull request.
5. Submit a pull request with a clear description of the change and any setup notes.

## License
A license has not been specified in this repository yet.
