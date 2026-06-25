from datetime import datetime

from pydantic import BaseModel, Field


class CreateSessionRequest(BaseModel):
    sales_manager_name: str | None = Field(default=None, max_length=255)
    source_campaign: str | None = Field(default=None, max_length=255)
    custom_prompt_instructions: str | None = None


class CreateSessionResponse(BaseModel):
    session_token: str
    chat_url: str
    status: str
    current_stage: str


class SessionDetailResponse(BaseModel):
    session_token: str
    sales_manager_name: str | None
    source_campaign: str | None
    custom_prompt_instructions: str | None
    status: str
    current_stage: str
    completion_score: int
    created_at: datetime
    updated_at: datetime
