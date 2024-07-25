from data_questionnaire_agent.model.confidence_schema import (
    ConfidenceDegree,
    ConfidenceRating,
)


def test_simple_confidence_rating():
    degree = ConfidenceDegree.high
    rating = ConfidenceRating(
        reasoning="We know the main problem of the user and the causes well. The only thing missing is more background information about the technological landscpae of the user.",
        rating=degree,
    )
    assert rating is not None
