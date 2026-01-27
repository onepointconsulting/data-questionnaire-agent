from datetime import datetime

from pydantic import BaseModel, Field


class SessionCompletedData(BaseModel):
    created_at: datetime = Field(..., description="The created at")
    start_answer: str = Field(..., description="The start answer")
    end_advice: str = Field(..., description="The end question")
    session_id: str = Field(..., description="The session id")


class SessionCompletedDataList(BaseModel):
    sessions: list[SessionCompletedData] = Field(
        ..., description="The list of completed sessions"
    )
