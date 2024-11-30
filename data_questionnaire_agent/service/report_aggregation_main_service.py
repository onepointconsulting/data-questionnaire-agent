from collections import Counter, OrderedDict
from typing import List, Tuple

from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from data_questionnaire_agent.config import cfg, report_agg_cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.questionnaire_status import QuestionnaireStatus
from data_questionnaire_agent.model.report_aggregation_schema import (
    ExtendedReportAggregationKeywords,
    KeyCount,
    ReportAggregationKeywords,
    ReportDocumentClassification,
    ReportDocumentClassificationContainer,
    ReportItemCount,
)
from data_questionnaire_agent.service.initial_question_service import (
    prompt_factory_generic,
)
from data_questionnaire_agent.service.similarity_search import num_tokens_from_string
from data_questionnaire_agent.toml_support import get_prompts


def create_structured_question_call(language: str = "en") -> RunnableSequence:
    model = cfg.llm.with_structured_output(ReportAggregationKeywords)
    prompt = prompt_factory_keyword_extraction_prompt(language)
    return prompt | model


def prompt_factory_keyword_extraction_prompt(
    language: str = "en",
) -> ChatPromptTemplate:
    prompts = get_prompts(language)
    section = prompts["reporting"]["keyword_extraction_prompt"]
    return prompt_factory_generic(
        section,
        [
            "full_questionnaires",
        ],
        prompts,
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


async def extract_report_dimensions(
    questionnaire_data: List[QuestionnaireStatus], language: str
) -> List[ReportAggregationKeywords]:
    questionnaire_list_str = convert_to_str(questionnaire_data)
    batched_list, count_list = batch_list(
        questionnaire_list_str, report_agg_cfg.report_token_limit
    )
    assert sum([len(b) for b in batched_list]) == len(
        questionnaire_list_str
    ), "The batching operation is not accurate."
    logger.info("Batch sizes in tokens:")
    for c in count_list:
        logger.info(c)
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
            logger.info(f"Processed {i * batch_size} documents")
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
        positive_outcomes_count=positive_outcomes_count
    )


if __name__ == "__main__":
    import asyncio
    import pickle

    from ulid import ULID

    from data_questionnaire_agent.service.report_aggregation_service import (
        convert_to_str,
    )

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


    def write_report_item_count(
            report_item_count: ReportItemCount
    ):
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

    asyncio.run(test_extract_report_dimensions())
