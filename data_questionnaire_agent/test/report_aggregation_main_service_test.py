from data_questionnaire_agent.service.report_aggregation_main_service import (
    prompt_factory_document_classifier_prompt,
    prompt_factory_keyword_extraction_prompt,
    group_reports
)
from data_questionnaire_agent.model.report_aggregation_schema import (
    ReportDocumentClassificationContainer,
)
from data_questionnaire_agent.config import cfg


def test_prompt_factory_keyword_extraction_prompt():
    template = prompt_factory_keyword_extraction_prompt(language="en")
    assert template is not None, "Template should not be none"


def test_prompt_factory_document_classifier_prompt():
    template = prompt_factory_document_classifier_prompt(language="en")
    assert template is not None, "Template should not be none"

def test_group_reports():
    sample_file = cfg.project_root/"data/report_doc_classification_01JDYZ52AD3KYM2Q7VF5NHV3ER.json"
    assert (sample_file).exists()
    document_classification = ReportDocumentClassificationContainer.model_validate_json(sample_file.read_text())
    report_item_count = group_reports(document_classification)
    assert report_item_count is not None
    assert report_item_count.problem_count is not None
    assert report_item_count.problem_area_count is not None
    assert report_item_count.recommendation_count is not None
