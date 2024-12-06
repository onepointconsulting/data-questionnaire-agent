import pickle
from typing import List

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.questionnaire_status import QuestionnaireStatus
from data_questionnaire_agent.service.report_aggregation_service import convert_to_str
from data_questionnaire_agent.service.similarity_search import num_tokens_from_string


def test_convert_to_str():
    questionnaire_pkl = cfg.project_root / "data/questionnaire.pkl"
    assert questionnaire_pkl.exists()
    with open(questionnaire_pkl, "rb") as f:
        questionnaire_data = pickle.load(f)
        questionnaire_statuses: List[QuestionnaireStatus] = convert_to_str(questionnaire_data)
        assert len(questionnaire_statuses) > 0
        print(num_tokens_from_string("\n".join(questionnaire_statuses)))
