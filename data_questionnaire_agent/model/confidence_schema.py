from enum import Enum
from typing import Union

from pydantic import BaseModel, Field

from data_questionnaire_agent.translation import t


class ConfidenceDegree(str, Enum):
    outstanding = "outstanding"
    high = "high"
    medium = "medium"
    mediocre = "mediocre"
    low = "low"


CONFIDENCE_DEGREE_DICT = {
    ConfidenceDegree.outstanding: 5,
    ConfidenceDegree.high: 4,
    ConfidenceDegree.medium: 3,
    ConfidenceDegree.mediocre: 2,
    ConfidenceDegree.low: 1,
}


class ConfidenceRating(BaseModel):
    """Represents a rating of how confident the model is to give advice to a customer based on a questionnaire"""

    class Config:
        use_enum_values = True

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

    def _value(self) -> int:
        return CONFIDENCE_DEGREE_DICT[self.rating]

    def __lt__(self, other):
        if isinstance(other, ConfidenceRating):
            return self._value() < other._value()
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, ConfidenceRating):
            return self._value() <= other._value()
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, ConfidenceRating):
            return self._value() > other._value()
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, ConfidenceRating):
            return self._value() >= other._value()
        return NotImplemented

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

    
if __name__ == "__main__":
    import asyncio

    rating = ConfidenceRating(
        id=1, reasoning="The model is very confident", rating=ConfidenceDegree.outstanding
    )
    print(rating.schema_json(indent=2))