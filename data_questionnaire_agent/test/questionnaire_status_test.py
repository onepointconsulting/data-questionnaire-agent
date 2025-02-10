from data_questionnaire_agent.model.questionnaire_status import QuestionnaireStatus
from data_questionnaire_agent.test.provider.questionnaire_status_provider import (
    create_simple,
)


def test_has_advice_questionnaire():
    qs: QuestionnaireStatus = create_simple()
    assert qs is not None
    difference = qs.updated_at - qs.created_at
    assert difference.seconds < 2
