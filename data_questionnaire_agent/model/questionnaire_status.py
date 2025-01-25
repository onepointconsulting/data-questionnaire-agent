from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field


class QuestionnaireStatus(BaseModel):
    id: Union[int, None] = Field(default=None, description="The unique identifier")
    session_id: str = Field(..., description="The session identifier")
    question: str = Field(..., description="The question")
    answer: Union[str, None] = Field(default="", description="The optional answer")
    final_report: bool = Field(..., description="Whether this is the final report")
    created_at: Union[datetime, None] = Field(
        default=None, description="The created timestamp"
    )
    updated_at: Union[datetime, None] = Field(
        default=None, description="The updated timestamp"
    )
    total_cost: float = Field(default=0, description="")
    clarification: Union[str, None] = Field(
        default=None, description="The clarification or explanation of the question"
    )
    question_id: int | None = Field(default=None, description="The question identifier in case a question is NOT generated")
