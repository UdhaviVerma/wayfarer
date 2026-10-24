# Wayfarer — Global Developer Relocation Advisor

AI-powered full-stack application that helps software engineers compare relocation options across 10 countries using salary, taxes, cost of living, visa complexity, PR pathways, and work-life signals.

## Tech Stack

- Frontend: Next.js, TypeScript, TailwindCSS, Recharts
- Backend: FastAPI, SQLAlchemy, JWT auth
- Database: PostgreSQL
- DevOps: Docker, Docker Compose, GitHub Actions, Render blueprint

## Features

- Country comparison table (salary, taxes, rent, living cost, savings, WLB, visa, PR, healthcare, safety)
- AI relocation advisor with Top-5 personalized recommendations + risk assessment
- Savings calculator with charted expense breakdown
- Visa roadmap timeline generator
- Job market analysis by country and skills
- AI chatbot for relocation Q&A
- Downloadable PDF recommendation report
- Dark mode and light mode

## Repository Structure

- `backend/` FastAPI app, migrations, seed script, tests
- `frontend/` Next.js app with landing + dashboard pages
- `docs/ERD.md` database ER diagram
- `.github/workflows/ci.yml` CI pipeline
- `docker-compose.yml` local full-stack setup

## Local Setup

1. Copy env values:
   - `cp .env.example .env` (or create manually on Windows)
2. Run full stack:
   - `docker compose up --build`
3. Access apps:
   - Frontend: `http://localhost:3000`
   - Backend: `http://localhost:8000`
   - Swagger: `http://localhost:8000/docs`

## Backend Commands

From `backend/`:

- Install: `pip install -r requirements.txt`
- Run API: `uvicorn app.main:app --reload`
- Migrate: `alembic upgrade head`
- Seed: `python -m app.seed`
- Test: `pytest`

## Frontend Commands

From `frontend/`:

- Install: `npm install`
- Dev: `npm run dev`
- Build: `npm run build`
- Start: `npm run start`

## API Endpoints

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/countries/compare`
- `POST /api/v1/recommendations/advisor`
- `POST /api/v1/recommendations/report`
- `POST /api/v1/savings/calculator`
- `POST /api/v1/visa/roadmap`
- `GET /api/v1/jobs/market`
- `POST /api/v1/chatbot/query`
- `GET /api/v1/dashboard/executive`
- `GET /api/v1/dashboard/rankings`
- `GET /api/v1/dashboard/heatmap`

## Render Deployment

### Option A: Blueprint (recommended)

1. Push repo to GitHub.
2. In Render, choose **New +** → **Blueprint**.
3. Select this repository (contains `render.yaml`).
4. Set secret env vars (`POSTGRES_PASSWORD`, `SECRET_KEY`) when prompted.
5. Deploy services.

### Option B: Manual

- Deploy PostgreSQL service first.
- Deploy backend Docker service with backend env vars.
- Deploy frontend Docker service with `NEXT_PUBLIC_API_URL` pointing to backend.

## GitHub Push Steps

From root `wayfarer/`:

```bash
git init
git add .
git commit -m "feat: initial wayfarer release"
git branch -M main
git remote add origin https://github.com/<your-username>/wayfarer.git
git push -u origin main
```

## LinkedIn Launch Post Template

> I built **Wayfarer: Global Developer Relocation Advisor** 🚀  
> It compares 10 countries for software engineers using salary, tax, rent, savings, PR difficulty, and work-life balance.  
> Includes AI recommendations, visa roadmap, job-market insights, and downloadable PDF strategy reports.  
> Tech stack: Next.js + FastAPI + PostgreSQL + Docker.  
> GitHub: <your-repo-url>  
> Live demo: <your-render-url>

## Notes

- Seed data is benchmarked for demo and portfolio use; replace with production datasets for real financial decisions.
- Update `SECRET_KEY` and tighten CORS before production launch.
