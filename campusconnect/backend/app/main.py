from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .database.database import Base, engine
from .seed import seed
from .routers import auth, events, clubs, opportunities, resources, support, notifications, profile, admin, search, announcements

app = FastAPI(title="CampusConnect API", version="1.0.0", docs_url="/api/docs", redoc_url="/api/redoc")
app.add_middleware(CORSMiddleware, allow_origins=[o.strip() for o in __import__('os').getenv('CORS_ORIGINS','*').split(',')], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

Base.metadata.create_all(bind=engine)
try:
    seed()
except Exception as exc:
    print("Seed warning:", exc)

for router in [auth.router, events.router, clubs.router, opportunities.router, resources.router, support.router, notifications.router, profile.router, admin.router, search.router, announcements.router]:
    app.include_router(router, prefix="/api")

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "CampusConnect API"}

frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="assets")

    from fastapi.responses import FileResponse
    from starlette.requests import Request
    @app.get("/{full_path:path}")
    async def spa(full_path: str, request: Request):
        if full_path.startswith("api/"):
            return {"detail": "Not found"}
        index = frontend_dist / "index.html"
        return FileResponse(index)
