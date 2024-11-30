from enum import StrEnum
from typing import Dict, List

from pydantic import BaseModel, Field


class ProbleSeverity(StrEnum):
    VERY_NEGATIVE = "very negative"
    NEGATIVE = "negative"
    MODERATE = "moderate"


class Problem(BaseModel):
    name: str = Field(..., description="The problem name")
    area: str = Field(..., description="The area of the problem")
    severity: ProbleSeverity = Field(..., description="The severity of the problem")


class Concept(BaseModel):
    name: str = Field(..., description="The name of the concept")
    area: str = Field(..., description="The area of the concept")


class Recommendation(Concept):
    """
    Represents a recommendation.
    """

    class Config:
        title = "Recommendation"
        description = "A recommendation in a specific area"


class NegativeRecommendation(Concept):
    """
    Represents a negative recommendation. What you should not be doing.
    """

    class Config:
        title = "Negative Recommendation"
        description = "A negative recommendation in a specific area"


class PositiveOutcomes(Concept):
    """
    Represents a positive outcome, in case you follow recommendations
    """

    class Config:
        title = "Positive Outcome"
        description = "A positive outcome in a specific area"


class ReportAggregationKeywords(BaseModel):
    problems: List[Problem] = Field(
        ..., description="The problems found overall in the questionnaires"
    )
    concepts: List[Concept] = Field(
        ..., description="The conceots that were found in the questionnaires"
    )
    recommendations: List[Recommendation] = Field(
        ..., description="A recommendation in a specific area"
    )
    negative_recommendations: List[Recommendation] = Field(
        ..., description="A recommendation in a specific area"
    )
    positive_outcomes: List[PositiveOutcomes] = Field(
        ..., description="The list of positive outcomes"
    )


def bulletize(items: List[str]) -> str:
    return "\n".join([f"- {p}" for p in items if p])


class ExtendedReportAggregationKeywords(ReportAggregationKeywords):
    problem_area: List[str] = Field(..., description="The problem areas")

    def get_problem_bullets(self) -> List[str]:
        return bulletize([p.name for p in self.problems])

    def get_problem_area_bullets(self) -> List[str]:
        return bulletize([c.area for c in self.problems])

    def get_concept_bullets(self) -> List[str]:
        return bulletize([c.name for c in self.concepts])

    def get_recommendation_bullets(self) -> List[str]:
        return bulletize([r.name for r in self.recommendations])

    def get_negative_recommendation_bullets(self) -> List[str]:
        return bulletize([r.name for r in self.negative_recommendations])

    def get_positive_outcome_bullets(self) -> List[str]:
        return bulletize([o.name for o in self.positive_outcomes])

class KeyValue(BaseModel):
    key: str = Field(
        ...,
        description="A key as string"
    )
    value: bool = Field(
        ...,
        description="A boolean to indicate whether the key is true or not"
    )


class KeyCount(BaseModel):
    key: str = Field(
        ...,
        description="A key as string"
    )
    count: int = Field(
        ...,
        description="The frequency of a problem"
    )


class ReportDocumentClassification(BaseModel):
    problem_dict: List[KeyValue] = Field(
        ...,
        description="List where keys are problems and values are booleans indicating whether the problem is mentioned in the questionnaire.",
        example={"poor data quality": True, "resistance to change": False},
    )
    concept_dict: List[KeyValue] = Field(
        ...,
        description="List where keys are concepts and values are booleans indicating whether the concept is mentioned in the questionnaire.",
        example={"data governance": True, "active metadata management": False},
    )
    problem_area_dict: List[KeyValue] = Field(
        ...,
        description="List where keys are problem areas and values are booleans indicating whether the problem area is mentioned in the questionnaire.",
        example={"data quality": True, "human resources": False},
    )
    recommendation_dict: List[KeyValue] = Field(
        ...,
        description="List where keys are recommendations and values are booleans indicating whether the recommendation is mentioned in the questionnaire.",
        example={
            "implement data validation process": True,
            "leverage data profiling tools": False,
        },
    )
    negative_recommendations_dict: List[KeyValue] = (
        Field(
            ...,
            description="List where keys are negative recommendations and values are booleans indicating whether the negative recommendation is mentioned in the questionnaire.",
            example={
                "Avoid relying solely on manual processes for data validation and merging": True,
                "Do not neglect the importance of data quality automation": False,
            },
        ),
    )
    positive_outcomes_dict: List[KeyValue] = Field(
        ...,
        description="List where keys are positive outcomes and values are booleans indicating whether the positive outcome is mentioned in the questionnaire.",
        example={
            "Enhanced data quality and integrity": True,
            "Increased Employee Engagement": False,
        },
    )


class ReportDocumentClassificationContainer(BaseModel):
    classification_list: List[ReportDocumentClassification] = Field(
        ..., description="A list of report document classifications"
    )


class ReportItemCount(BaseModel):
    problem_count: List[KeyCount] = Field(
        ...,
        description="List with the counts for each problem.",
        example={"poor data quality": 5, "resistance to change": 1},
    )
    concept_count: List[KeyCount] = Field(
        ...,
        description="List with the counts for each concept.",
        example={"data governance": 5, "active metadata management": 1},
    )
    problem_area_count: List[KeyCount] = Field(
        ...,
        description="List with the counts for each problem area.",
        example={"data quality": 4, "human resources": 2},
    )
    recommendation_count: List[KeyCount] = Field(
        ...,
        description="List with the counts for each recommendation.",
        example={
            "implement data validation process": 4,
            "leverage data profiling tools": 2,
        },
    )
    negative_recommendations_count: List[KeyCount] = (
        Field(
            ...,
            description="List with the counts for each negative recommendation.",
            example={
                "Avoid relying solely on manual processes for data validation and merging": 1,
                "Do not neglect the importance of data quality automation": 2,
            },
        ),
    )
    positive_outcomes_count: List[KeyCount] = Field(
        ...,
        description="List with the counts for each positive outcome.",
        example={
            "Enhanced data quality and integrity": 3,
            "Increased Employee Engagement": 2,
        },
    )

if __name__ == "__main__":
    print(ReportDocumentClassification.schema_json())