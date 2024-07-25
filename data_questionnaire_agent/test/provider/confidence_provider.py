from data_questionnaire_agent.model.confidence_schema import (
    ConfidenceDegree,
    ConfidenceRating,
)


def create_confidence_rating() -> ConfidenceRating:
    return ConfidenceRating(
        rating=ConfidenceDegree.low,
        reasoning="""Based on the provided information, I only know the main problem of the customer, which is poor data quality. However, I do not have detailed information about the causes of the problem, the technological landscape, or the data governance strategies of the customer. Therefore, my confidence in giving advice is low.""",
    )
