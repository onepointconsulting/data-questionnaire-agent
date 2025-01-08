from collections import Counter, OrderedDict
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence
from ulid import ULID

from data_questionnaire_agent.config import cfg, report_agg_cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.mail_data import Email
from data_questionnaire_agent.model.questionnaire_status import QuestionnaireStatus
from data_questionnaire_agent.model.report_aggregation_schema import (
    ExtendedReportAggregationKeywords,
    KeyCount,
    ReportAggregationKeywords,
    ReportDocumentClassification,
    ReportDocumentClassificationContainer,
    ReportItemCount,
)
from data_questionnaire_agent.service.mail_sender import send_mail_with_attachment
from data_questionnaire_agent.service.persistence_service_async import (
    select_questionnaires_by_tokens,
)
from data_questionnaire_agent.service.prompt_support import (
    factory_prompt,
    prompt_factory_generic,
)
from data_questionnaire_agent.service.report_aggregation_service import (
    convert_to_str,
)
from data_questionnaire_agent.service.report_aggregation_summarization_service import (
    aexecute_summarization_batch_str,
)
from data_questionnaire_agent.service.similarity_search import num_tokens_from_string
from data_questionnaire_agent.toml_support import get_prompts
from data_questionnaire_agent.translation import t


def create_structured_question_call(language: str = "en") -> RunnableSequence:
    model = cfg.llm.with_structured_output(ReportAggregationKeywords)
    prompt = prompt_factory_keyword_extraction_prompt(language)
    return prompt | model


def prompt_factory_keyword_extraction_prompt(
    language: str = "en",
) -> ChatPromptTemplate:
    return factory_prompt(
        lambda prompts: prompts["reporting"]["keyword_extraction_prompt"],
        [
            "full_questionnaires",
        ],
        language,
    )


def create_document_classifier_call(language: str = "en") -> RunnableSequence:
    model = cfg.llm.with_structured_output(ReportDocumentClassification)
    prompt = prompt_factory_document_classifier_prompt(language)
    return prompt | model


def prompt_factory_document_classifier_prompt(
    language: str = "en",
) -> ChatPromptTemplate:
    prompts = get_prompts(language)
    section = prompts["reporting"]["keyword_document_classifier"]
    return prompt_factory_generic(
        section,
        [
            "problems",
            "problem_areas",
            "concepts",
            "recommendations",
            "negative_recommendations",
            "positive_outcomes",
            "full_questionnaire",
        ],
        prompts,
    )


def batch_list(
    questionnaire_list_str: List[str], token_limit: int
) -> Tuple[List[List[str]], List[int]]:
    batch_list = []
    current_list = []
    token_counts = []
    total = 0
    for string in questionnaire_list_str:
        num_tokens = num_tokens_from_string(string)
        total += num_tokens
        if total > token_limit:
            token_counts.append(total - num_tokens)
            batch_list.append(current_list)
            current_list = [string]
            total = num_tokens
        else:
            current_list.append(string)
    batch_list.append(current_list)
    token_counts.append(total)
    return batch_list, token_counts


def count_all_tokens(all_questionnaires: List[str]) -> int:
    return sum([num_tokens_from_string(string) for string in all_questionnaires])


async def extract_report_dimensions(
    questionnaire_data: List[QuestionnaireStatus], language: str
) -> List[ReportAggregationKeywords]:
    questionnaire_list_str = convert_to_str(questionnaire_data)
    sum_tokens = count_all_tokens(questionnaire_list_str)
    # Only summarize in case the token count is high
    if sum_tokens > report_agg_cfg.report_token_limit:
        questionnaire_list_str = await aexecute_summarization_batch_str(
            questionnaire_list_str
        )
    batched_list, count_list = batch_list(
        questionnaire_list_str, report_agg_cfg.report_token_limit
    )
    assert sum([len(b) for b in batched_list]) == len(
        questionnaire_list_str
    ), "The batching operation is not accurate."
    logger.info("Batch sizes in tokens:")
    for c in count_list:
        logger.info("Batch size: %d", c)
    chain = create_structured_question_call(language)
    keyword_list = []
    for batch in batched_list:
        questionnaire_list_str = "\n".join(batch)
        res = await chain.ainvoke({"full_questionnaires": questionnaire_list_str})
        keyword_list.append(res)
    return keyword_list


def merge_reports(
    keyword_aggregations: List[ReportAggregationKeywords],
) -> ExtendedReportAggregationKeywords:
    problem_map = OrderedDict()
    problem_area_map = OrderedDict()
    concept_map = OrderedDict()
    recommendation_map = OrderedDict()
    negative_recommendation_map = OrderedDict()
    positive_outcomes_map = OrderedDict()

    def set_default_lower(d: OrderedDict, key: str, val: any):
        d.setdefault(key.lower().strip(), val)

    for keyword_aggregation in keyword_aggregations:
        for problem in keyword_aggregation.problems:
            set_default_lower(problem_map, problem.name, problem)
            set_default_lower(problem_area_map, problem.area, problem.area)
        for concept in keyword_aggregation.concepts:
            set_default_lower(concept_map, concept.name, concept)
        for recommendation in keyword_aggregation.recommendations:
            set_default_lower(recommendation_map, recommendation.name, recommendation)
        for negative_recommendation in keyword_aggregation.negative_recommendations:
            set_default_lower(
                negative_recommendation_map,
                negative_recommendation.name,
                negative_recommendation,
            )
        for positive_outcome in keyword_aggregation.positive_outcomes:
            set_default_lower(
                positive_outcomes_map, positive_outcome.name, positive_outcome
            )
    return ExtendedReportAggregationKeywords(
        problems=list(problem_map.values()),
        concepts=list(concept_map.values()),
        recommendations=list(recommendation_map.values()),
        negative_recommendations=list(negative_recommendation_map.values()),
        positive_outcomes=list(positive_outcomes_map.values()),
        problem_area=list(problem_area_map.values()),
    )


async def generate_document_classification(
    questionnaire_data: List[QuestionnaireStatus],
    aggregation_keywords: ExtendedReportAggregationKeywords,
    batch_size: int = 2,
    language: str = 2,
) -> ReportDocumentClassificationContainer:
    questionnaire_list_str = convert_to_str(questionnaire_data)
    chain = create_document_classifier_call(language)
    final_results = []
    chain_inputs = [
        {
            "problems": aggregation_keywords.get_problem_bullets(),
            "problem_areas": aggregation_keywords.get_problem_area_bullets(),
            "concepts": aggregation_keywords.get_concept_bullets(),
            "recommendations": aggregation_keywords.get_recommendation_bullets(),
            "negative_recommendations": aggregation_keywords.get_negative_recommendation_bullets(),
            "positive_outcomes": aggregation_keywords.get_positive_outcome_bullets(),
            "full_questionnaire": questionnaire,
        }
        for questionnaire in questionnaire_list_str
    ]
    batches = [
        chain_inputs[i : i + batch_size] for i in range(len(chain_inputs))[::batch_size]
    ]
    for i, batch in enumerate(batches):
        try:
            batch_res = await chain.abatch(batch)
            final_results.extend(batch_res)
            logger.info(f"Processed {i * batch_size + batch_size}  documents")
        except Exception as e:
            logger.exception(e)

    return ReportDocumentClassificationContainer(classification_list=final_results)


def group_reports(
    report_doc_classification: ReportDocumentClassificationContainer,
) -> ReportItemCount:
    classification_list = report_doc_classification.classification_list

    def perform_count(fetch_dict: callable) -> List[KeyCount]:
        counter = Counter()
        for cl in classification_list:
            for p in fetch_dict(cl):
                if p.value:
                    counter.update([p.key])
        return [KeyCount(key=key, count=value) for key, value in counter.items()]

    problem_count = perform_count(lambda x: x.problem_dict)
    concept_count = perform_count(lambda x: x.concept_dict)
    problem_area_count = perform_count(lambda x: x.problem_area_dict)
    recommendation_count = perform_count(lambda x: x.recommendation_dict)
    negative_recommendations_count = perform_count(
        lambda x: x.negative_recommendations_dict
    )
    positive_outcomes_count = perform_count(lambda x: x.positive_outcomes_dict)
    return ReportItemCount(
        problem_count=problem_count,
        concept_count=concept_count,
        problem_area_count=problem_area_count,
        recommendation_count=recommendation_count,
        negative_recommendations_count=negative_recommendations_count,
        positive_outcomes_count=positive_outcomes_count,
    )


def convert_to_dataframe(report_item_count: ReportItemCount) -> Dict[str, pd.DataFrame]:
    def convert_to_map(key_counts: List[KeyCount], key_name: str) -> pd.DataFrame:
        col_count = "count"
        data = []
        for kc in key_counts:
            data.append({key_name: kc.key, col_count: kc.count})
        df = pd.DataFrame(data)
        if len(df) > 0:
            df = df.sort_values(by=col_count, ascending=False).reset_index(drop=True)
            df["percent"] = (df["count"] / sum(df["count"]) * 100).round(2)
        else:
            logger.warning("The dataframe is empty.")
        return df

    problem_df = convert_to_map(report_item_count.problem_count, "Problem")
    problem_area_df = convert_to_map(
        report_item_count.problem_area_count, "Problem Area"
    )
    concept_df = convert_to_map(report_item_count.concept_count, "Concept")
    recommendation_df = convert_to_map(
        report_item_count.recommendation_count, "Recommendation"
    )
    negative_recommendations_count_df = convert_to_map(
        report_item_count.negative_recommendations_count, "What to avoid"
    )
    positive_outcomes_count_df = convert_to_map(
        report_item_count.positive_outcomes_count, "Potential positive outcomes"
    )
    return {
        "problem_df": {"df": problem_df, "sheet name": "Problems"},
        "problem_area_df": {"df": problem_area_df, "sheet name": "Problem Area"},
        "concept_df": {"df": concept_df, "sheet name": "Concepts"},
        "recommendation_df": {"df": recommendation_df, "sheet name": "Recommendations"},
        "negative_recommendations_count_df": {
            "df": negative_recommendations_count_df,
            "sheet name": "What to avoid",
        },
        "positive_outcomes_count_df": {
            "df": positive_outcomes_count_df,
            "sheet name": "Predicted outcomes",
        },
    }


def create_multiple_excel(df_dict: Dict[str, pd.DataFrame], excel_path: Path):
    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        workbook = writer.book
        for i, (_, v) in enumerate(df_dict.items()):
            sheet_name = v["sheet name"].replace(" ", "_")
            v["df"].to_excel(writer, sheet_name=sheet_name)
            worksheet = writer.sheets[sheet_name]
            # Create a Pie chart.
            chart = workbook.add_chart({"type": "pie"})
            initial_row = 2
            last_row = len(v["df"]) + initial_row
            # Add the chart series.

            chart.add_series(
                {
                    "categories": f"={sheet_name}!B2:B{last_row}",
                    "values": f"={sheet_name}!C2:C{last_row}",
                }
            )
            worksheet.insert_chart("F1", chart)


def prepare_send_email(
    aggregation_report_path: Path, email_list: list[str], language: str = "en"
):
    if not email_list:
        return
    mail_template = cfg.template_location / "mail-template.html"
    mail_template_text = mail_template.read_text(encoding="utf-8")
    body = mail_template_text.format(
        text=t("Please check the attached report", locale=language)
    )
    for email in email_list:
        send_mail_with_attachment(
            email=Email(
                recipient=email,
                subject=t("Data Wellness Aggregation Report", locale=language),
                html_body=body,
                files=[aggregation_report_path],
            )
        )


async def aggregate_reports_main(
    tokens: List[str], email_list: list[str], language: str = "en"
) -> Path:
    # Fetch statuses from the database
    logger.info("Report: Fetch statuses from the database")
    questionnaire_data: List[
        QuestionnaireStatus
    ] = await select_questionnaires_by_tokens(tokens)
    logger.info(f"Report: {len(questionnaire_data)} reports available.")

    # Extract the dimensions in batches
    logger.info("Report: Extract the dimensions in batches")
    keyword_lists = await extract_report_dimensions(questionnaire_data, language)
    # Merge the batches together
    logger.info("Report: Merge the batches together")
    merged_report_aggregation_keywords = merge_reports(keyword_lists)
    # Generate the document classifications
    logger.info("Report: Generate the document classifications")
    report_doc_classification = await generate_document_classification(
        questionnaire_data, merged_report_aggregation_keywords, batch_size=2
    )
    # Do some counting
    logger.info("Report: Doing the counting")
    report_item_count = group_reports(report_doc_classification)
    # Convert to dataframe
    logger.info("Report: Dataframe conversion")
    df_dict = convert_to_dataframe(report_item_count)
    aggregation_report_path = (
        cfg.aggregator_report_folder / f"aggregation_report_{str(ULID())}.xlsx"
    )
    logger.info("Report: Creating Excel with multiple sheets")
    create_multiple_excel(df_dict, aggregation_report_path)
    logger.info("Report: Aggregated report finished.")
    prepare_send_email(aggregation_report_path, email_list, language)
    return aggregation_report_path


if __name__ == "__main__":
    import asyncio
    import pickle

    def write_to_disk(
        report_aggregation_keywords: ReportAggregationKeywords, aggregate: bool
    ):
        id = str(ULID())
        extra = "_aggregated" if aggregate else ""
        file_path = f"./report_aggregation_service_{id}{extra}.json"
        with open(file_path, "w") as f:
            print("file path", file_path)
            f.write(report_aggregation_keywords.model_dump_json())

    def write_classification_to_disk(
        report_doc_classification: ReportDocumentClassificationContainer,
    ):
        id = str(ULID())
        file_path = f"./report_doc_classification_{id}.json"
        with open(file_path, "w") as f:
            f.write(report_doc_classification.model_dump_json())
            print(f"Wrote to {file_path}")

    def write_report_item_count(report_item_count: ReportItemCount):
        id = str(ULID())
        file_path = f"./report_item_count_{id}.json"
        with open(file_path, "w") as f:
            f.write(report_item_count.model_dump_json())
            print(f"Wrote to {file_path}")

    async def test_extract_report_dimensions():
        questionnaire_pkl = cfg.project_root / "data/questionnaire_all.pkl"
        language = "en"
        assert questionnaire_pkl.exists()
        with open(questionnaire_pkl, "rb") as f:
            questionnaire_data = pickle.load(f)
            keyword_lists = await extract_report_dimensions(
                questionnaire_data, language
            )
            for i, keywords in enumerate(keyword_lists):
                write_to_disk(keywords, False)
                print("Processed", i)
            merged_report_aggregation_keywords = merge_reports(keyword_lists)
            write_to_disk(merged_report_aggregation_keywords, True)
            report_doc_classification = await generate_document_classification(
                questionnaire_data, merged_report_aggregation_keywords, batch_size=2
            )
            write_classification_to_disk(report_doc_classification)
            report_item_count = group_reports(report_doc_classification)
            write_report_item_count(report_item_count)

    async def test_aggregate_reports_main():
        aggregation_report_path = await aggregate_reports_main([])
        print(aggregation_report_path)

    asyncio.run(test_aggregate_reports_main())
