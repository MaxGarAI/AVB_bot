from fastapi import FastAPI

from app.api.routes_admin import router as admin_router
from app.api.routes_chat import router as chat_router
from app.api.routes_sessions import router as sessions_router
from app.db import Base, engine
from app.models import InterviewSession  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dealer MVP")
app.include_router(chat_router)
app.include_router(sessions_router)
app.include_router(admin_router)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
