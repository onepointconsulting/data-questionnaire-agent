from pathlib import Path
from typing import Dict

import pandas as pd

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.report_aggregation_schema import (
    ReportDocumentClassificationContainer,
    ReportItemCount,
)
from data_questionnaire_agent.service.report_aggregation_main_service import (
    convert_to_dataframe,
    create_multiple_excel,
    group_reports,
    prompt_factory_document_classifier_prompt,
    prompt_factory_keyword_extraction_prompt,
)


def test_prompt_factory_keyword_extraction_prompt():
    template = prompt_factory_keyword_extraction_prompt(language="en")
    assert template is not None, "Template should not be none"


def test_prompt_factory_document_classifier_prompt():
    template = prompt_factory_document_classifier_prompt(language="en")
    assert template is not None, "Template should not be none"


def test_group_reports():
    sample_file = (
        cfg.project_root
        / "data/report_doc_classification_01JDYZ52AD3KYM2Q7VF5NHV3ER.json"
    )
    assert (sample_file).exists()
    document_classification = ReportDocumentClassificationContainer.model_validate_json(
        sample_file.read_text()
    )
    report_item_count = group_reports(document_classification)
    assert report_item_count is not None
    assert report_item_count.problem_count is not None
    assert report_item_count.problem_area_count is not None
    assert report_item_count.recommendation_count is not None


def generate_df_dict() -> Dict[str, pd.DataFrame]:
    sample_file = (
        cfg.project_root / "data/report_item_count_01JDZBAA5T6Z0MHZ10KY0HF938.json"
    )
    assert (sample_file).exists()
    report_item_count = ReportItemCount.model_validate_json(sample_file.read_text())
    return convert_to_dataframe(report_item_count)


def test_convert_to_dataframe():
    df_dict = generate_df_dict()
    assert df_dict is not None
    assert df_dict["problem_df"] is not None
    assert len(df_dict["problem_df"]["df"]) > 0
    assert df_dict["problem_area_df"] is not None
    assert len(df_dict["problem_area_df"]["df"]) > 0


def test_create_multiple_excel():
    df_dict = generate_df_dict()
    assert df_dict is not None
    excel_path = Path("./report_aggregation_counts.xlsx")
    create_multiple_excel(df_dict, excel_path)
    assert excel_path.exists(), "Cannot find multiple excel report"
