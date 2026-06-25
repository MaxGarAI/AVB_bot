from pydantic import BaseModel, Field


class ChatMessageCreate(BaseModel):
    message: str = Field(min_length=1)


class ChatMessageResponse(BaseModel):
    assistant_message: str
    status: str
    current_stage: str
    completion_score: int
