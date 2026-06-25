from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.models.session import InterviewSession
from app.schemas.api import CreateSessionRequest, CreateSessionResponse, SessionDetailResponse
from app.services.token_service import generate_session_token

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.post("", response_model=CreateSessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(payload: CreateSessionRequest, db: Session = Depends(get_db)) -> CreateSessionResponse:
    token = generate_session_token()
    session = InterviewSession(
        session_token=token,
        sales_manager_name=payload.sales_manager_name,
        source_campaign=payload.source_campaign,
        custom_prompt_instructions=payload.custom_prompt_instructions,
        status="created",
        current_stage="INIT",
        completion_score=0,
    )
    db.add(session)
    db.commit()

    settings = get_settings()
    return CreateSessionResponse(
        session_token=token,
        chat_url=f"{settings.app_base_url}/chat/{token}",
        status=session.status,
        current_stage=session.current_stage,
    )


@router.get("/{token}", response_model=SessionDetailResponse)
def get_session(token: str, db: Session = Depends(get_db)) -> SessionDetailResponse:
    session = db.query(InterviewSession).filter(InterviewSession.session_token == token).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return SessionDetailResponse(
        session_token=session.session_token,
        sales_manager_name=session.sales_manager_name,
        source_campaign=session.source_campaign,
        custom_prompt_instructions=session.custom_prompt_instructions,
        status=session.status,
        current_stage=session.current_stage,
        completion_score=session.completion_score,
        created_at=session.created_at,
        updated_at=session.updated_at,
    )
