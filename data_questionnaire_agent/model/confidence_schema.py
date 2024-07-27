from enum import Enum
from typing import Union

from pydantic.v1 import BaseModel, Field

from data_questionnaire_agent.translation import t


class ConfidenceDegree(str, Enum):
    outstanding = "outstanding"
    high = "high"
    medium = "medium"
    mediocre = "mediocre"
    low = "low"


class ConfidenceRating(BaseModel):
    """Represents a rating of how confident the model is to give advice to a customer based on a questionnaire"""

    id: Union[int, None] = Field(
        default=None, description="The identifier of this session configuration"
    )

    reasoning: str = Field(
        ..., description="The models's reasoning behind the confidence rating."
    )

    rating: ConfidenceDegree = Field(
        ...,
        description="The confidence rating of the model to give advice to a customer based on a questionnaire",
    )

    def to_markdown(self, locale: str = "en") -> str:
        return f"""
# {t("Confidence Degree", locale=locale)}

`{t("confidence_degree_" + self.rating, locale=locale)}`

## {t("Reasoning", locale=locale)}

{self.reasoning}
"""

    def to_html(self, language: str = "en") -> str:
        return f"""
<div style="text-align: center"><b>{t("confidence_degree_" + self.rating)}</b></div>

<h2>{t("Reasoning", locale=language)}</h2>

<p>{self.reasoning}</p>
"""
