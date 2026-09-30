# CampusConnect

CampusConnect is a production-style full-stack student platform based on the supplied project brief: **"Your Campus. Your Community. Your Opportunities."** It includes student and admin roles, authentication, database-backed CRUD, event registration, club joining, saved opportunities/resources, support tickets, notifications, global search, responsive UI, and demo data.

## Stack

- Frontend: React + TypeScript + Tailwind CSS + Vite
- Backend: FastAPI + SQLAlchemy + Pydantic
- Database: SQLite locally; PostgreSQL-compatible in deployment
- Auth: JWT + bcrypt password hashing

## Demo accounts

**Student**
- Email: `student@campusconnect.com`
- Password: `Student@123`

**Admin**
- Email: `admin@campusconnect.com`
- Password: `Admin@123`

Change demo credentials before real deployment.

## Local development

### Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend uses `VITE_API_URL=http://localhost:8000/api` when you want to point it to a separately running API. Without it, production builds expect `/api` on the same host.

## Production / Render-style deployment

This repository can be deployed as a **single service** because FastAPI serves the built React app when `frontend/dist` exists.

1. Build the frontend: `cd frontend && npm ci && npm run build`
2. Install backend requirements.
3. Start with: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT` from the repository root, or use the included backend start script after adjusting the working directory.
4. Set a strong `JWT_SECRET` and a persistent PostgreSQL `DATABASE_URL` in production.

For a managed PostgreSQL database, use any PostgreSQL provider that gives you a connection string. The application automatically converts common `postgres://` and `postgresql://` URLs to the psycopg SQLAlchemy driver form.

## API docs

When the API is running: `/api/docs`

## Functional demo flow

Browse homepage → Events → search Hackathon → open Campus Hackathon → login → register → Dashboard → join Coding Club → save an opportunity → save a resource → submit support ticket → view notifications → edit profile → logout → login again and verify persistence.

## Notes

- Resource and opportunity demo links currently use `example.com` placeholders so the app is functional without external institutional integrations.
- Social footer links are placeholders and can be replaced with real accounts.
- File uploads are not wired to external object storage; the resource model is ready for a URL-based resource workflow.
