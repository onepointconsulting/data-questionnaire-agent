import asyncio
from typing import List

from data_questionnaire_agent.model.application_schema import (
    Questionnaire,
)
from data_questionnaire_agent.model.confidence_schema import ConfidenceRating
from data_questionnaire_agent.service.confidence_service import (
    calculate_confidence_rating,
    prompt_factory_confidence,
)
from data_questionnaire_agent.test.provider.questionnaire_provider import (
    create_questionnaire_2_questions,
    create_questionnaire_3_questions,
    create_questionnaire_4_questions,
    create_questionnaire_4_questions_german,
)


def test_prompt_factory_confidence():
    prompt_template = prompt_factory_confidence("en")
    assert prompt_template is not None
    assert prompt_template.messages is not None
    assert len(prompt_template.messages) > 0


def test_calculate_confidence_rating_mediocre():
    eval_questionnaire(create_questionnaire_2_questions(), ["low", "mediocre"])


def test_calculate_confidence_rating_mediocre_2():
    eval_questionnaire(create_questionnaire_3_questions(), ["mediocre", "medium"])


def test_calculate_confidence_rating_stronger():
    eval_questionnaire(
        create_questionnaire_4_questions(), ["mediocre", "medium", "high"]
    )


def test_calculate_confidence_rating_german():
    eval_questionnaire(
        create_questionnaire_4_questions_german(), ["mediocre", "medium", "high"], "de"
    )


def eval_questionnaire(
    questionnaire: Questionnaire, expected: List[str], language: str = "en"
):
    confidence_rating: ConfidenceRating = asyncio.run(
        calculate_confidence_rating(questionnaire, "en")
    )
    assert confidence_rating is not None
    assert confidence_rating.rating is not None
    assert confidence_rating.reasoning is not None
    assert confidence_rating.rating in expected
