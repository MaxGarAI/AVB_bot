from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.audience_profile import AudienceProfile
from app.models.business_profile import BusinessProfile
from app.models.channel import CommunicationChannel
from app.models.metric import InterviewMetric
from app.models.opportunity import Opportunity
from app.models.segment import AudienceSegment
from app.models.session import InterviewSession

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/sessions", response_class=HTMLResponse)
def admin_sessions_list(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    sessions = db.execute(
        select(InterviewSession).order_by(InterviewSession.created_at.desc()).limit(50)
    ).scalars().all()

    return templates.TemplateResponse(
        "admin_sessions.html",
        {"request": request, "sessions": sessions},
    )


@router.get("/sessions/{token}", response_class=HTMLResponse)
def admin_session_detail(request: Request, token: str, db: Session = Depends(get_db)) -> HTMLResponse:
    session = db.execute(
        select(InterviewSession).where(InterviewSession.session_token == token)
    ).scalar_one_or_none()
    if session is None:
        return HTMLResponse("Session not found", status_code=404)

    business = db.execute(
        select(BusinessProfile).where(BusinessProfile.session_id == session.id)
    ).scalar_one_or_none()
    audience = db.execute(
        select(AudienceProfile).where(AudienceProfile.session_id == session.id)
    ).scalar_one_or_none()
    segments = db.execute(
        select(AudienceSegment).where(AudienceSegment.session_id == session.id)
    ).scalars().all()
    channels = db.execute(
        select(CommunicationChannel).where(CommunicationChannel.session_id == session.id)
    ).scalars().all()
    opportunities = db.execute(
        select(Opportunity).where(Opportunity.session_id == session.id)
    ).scalars().all()
    metrics = db.execute(
        select(InterviewMetric).where(InterviewMetric.session_id == session.id)
    ).scalar_one_or_none()

    return templates.TemplateResponse(
        "admin_session_detail.html",
        {
            "request": request,
            "session": session,
            "business": business,
            "audience": audience,
            "segments": segments,
            "channels": channels,
            "opportunities": opportunities,
            "metrics": metrics,
        },
    )