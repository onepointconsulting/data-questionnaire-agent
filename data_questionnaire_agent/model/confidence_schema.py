from enum import Enum
from pydantic.v1 import BaseModel, Field


class ConfidenceDegree(str, Enum):
    outstanding = "outstanding"
    high = "high"
    medium = "medium"
    mediocre = "mediocre"
    low = "low"


class ConfidenceRating(BaseModel):
    """Represents a rating of how confident the model is to give advice to a customer based on a questionnaire"""

    reasoning: str = Field(
        ..., description="The models's reasoning behind the confidence rating."
    )
    rating: ConfidenceDegree = Field(
        ...,
        description="The confidence rating of the model to give advice to a customer based on a questionnaire",
    )
