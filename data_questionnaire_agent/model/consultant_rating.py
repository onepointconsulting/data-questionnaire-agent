from enum import StrEnum
from typing import Optional

from pydantic.v1 import BaseModel, Field


class AnalystRating(StrEnum):
    very_suitable = "very suitable"
    suitable = "suitable"
    moderately_suitable = "moderately suitable"
    hardly_suitable = "hardly suitable"
    unsuitable = "unsuitable"


SCORES = {
    AnalystRating.very_suitable: 5,
    AnalystRating.suitable: 4,
    AnalystRating.moderately_suitable: 3,
    AnalystRating.hardly_suitable: 2,
    AnalystRating.unsuitable: 1,
}


class ConsultantRating(BaseModel):
    """Represents the degree to which a consultant with a specific profile can help a customer that answered a questionnaire."""

    analyst_name: str = Field(..., description="The analyst's name.")

    analyst_linkedin_url: Optional[str] = Field(
        ..., description="The optional analyst LinkedIN URL"
    )

    reasoning: str = Field(
        ...,
        description="The models's reasoning behind the analyst rating. Why is this analyst suitable or not to support the client which answered the questionnnaire.",
    )

    rating: AnalystRating = Field(
        ...,
        description="The rating of the consulting capabilities of the consultant to help the customer",
    )


class ScoredConsultantRating(ConsultantRating):
    """Rrepresents a scored consultant rating."""

    score: int = Field(
        ...,
        description="The score applied to this consultant for the current customer.",
    )


class ConsultantRatings(BaseModel):
    consultant_ratings: list[ConsultantRating] = Field(
        ..., description="The list of consultant ratings"
    )
