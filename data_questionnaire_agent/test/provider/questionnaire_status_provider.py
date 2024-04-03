from datetime import datetime
from data_questionnaire_agent.model.questionnaire_status import QuestionnaireStatus


def create_simple() -> QuestionnaireStatus:
    return QuestionnaireStatus(
        session_id="12312231231",
        question="What is the meaning of this?",
        answer="42",
        final_report=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
