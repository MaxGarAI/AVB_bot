from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.session import InterviewSession
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse
from app.services.interview_service import InterviewService

router = APIRouter(tags=["chat"])
templates = Jinja2Templates(directory="app/templates")
interview_service = InterviewService()


@router.get("/chat/{token}", response_class=HTMLResponse)
def chat_page(token: str, request: Request) -> HTMLResponse:
    return templates.TemplateResponse("chat.html", {"request": request, "session_token": token})


@router.post("/api/chat/{token}/messages", response_model=ChatMessageResponse)
def create_chat_message(token: str, payload: ChatMessageCreate, db: Session = Depends(get_db)) -> ChatMessageResponse:
    session = db.query(InterviewSession).filter(InterviewSession.session_token == token).first()
    if session is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Session not found")

    _, assistant_message, session = interview_service.process_user_message(db, session, payload.message)
    return ChatMessageResponse(
        assistant_message=assistant_message.content,
        status=session.status,
        current_stage=session.current_stage,
        completion_score=session.completion_score,
    )