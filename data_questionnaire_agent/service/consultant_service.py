import json
from typing import TypedDict

import jinja2
from consultant_info_generator.model import Consultant
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.consultant_rating import (
    SCORES,
    ConsultantRatings,
    ScoredConsultantRating,
)
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.persistence_service_async import (
    select_questionnaire_statuses,
)
from data_questionnaire_agent.service.persistence_service_consultants_async import (
    read_consultants,
)
from data_questionnaire_agent.service.prompt_support import (
    prompt_factory_generic,
)
from data_questionnaire_agent.toml_support import get_prompts


class ConsultantCallData(TypedDict):
    questions_answers: str
    conditional_advice: str
    cvs: str


def convert_to_markdown(consultants: list[Consultant], language: str = "en") -> str:
    context = {
        "consultants": consultants,
    }
    template_loader = jinja2.FileSystemLoader(cfg.template_location)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("consultants-template.md")
    return template.render(context)


async def convert_all_consultants() -> str:
    consultants = await read_consultants()
    return convert_to_markdown(consultants)


def prompt_factory_consultants(language: str) -> ChatPromptTemplate:
    # Assuming get_prompts() returns the required dictionary
    prompts = get_prompts(language)
    section = prompts["consultants"]["evaluation"]
    return prompt_factory_generic(
        section=section,
        input_variables=["questions_answers", "conditional_advice", "cvs"],
        prompts=prompts,
    )


def create_structured_consultant_call(language: str) -> RunnableSequence:
    model = cfg.llm.with_structured_output(ConsultantRatings)
    prompt = prompt_factory_consultants(language)
    return prompt | model


async def prepare_consultant_call(
    questions_answers: Questionnaire,
    conditional_advice: ConditionalAdvice,
) -> ConsultantCallData:
    return {
        "questions_answers": str(questions_answers),
        "conditional_advice": str(conditional_advice),
        "cvs": await convert_all_consultants(),
    }


async def calculate_consultant_ratings_for(
    session_id, language: str = "en"
) -> ConsultantRatings | None:
    questionnaire_statuses = await select_questionnaire_statuses(session_id)
    if not questionnaire_statuses:
        return None
    final_report_list = [qs for qs in questionnaire_statuses if qs.final_report]
    if not final_report_list:
        return None
    advice_dict = json.loads(final_report_list[0].question)
    advice = ConditionalAdvice.parse_obj(advice_dict)
    prompt_data = await prepare_consultant_call(
        Questionnaire(questions=questionnaire_statuses), advice
    )
    runnable_sequence = create_structured_consultant_call(language)
    consultant_ratings: ConsultantRatings = await runnable_sequence.ainvoke(prompt_data)
    consultant_ratings = sorted([
        ScoredConsultantRating(
            analyst_name=cr.analyst_name,
            analyst_linkedin_url=cr.analyst_linkedin_url,
            reasoning=cr.reasoning,
            rating=cr.rating,
            score=SCORES[cr.rating],
        )
        for cr in consultant_ratings.consultant_ratings
    ], key=lambda cr: cr.score, reverse=True)
    return ConsultantRatings(consultant_ratings=consultant_ratings)
