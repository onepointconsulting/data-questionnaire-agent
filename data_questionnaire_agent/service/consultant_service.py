import asyncio
import json
from typing import TypedDict

import jinja2
from consultant_info_generator.model import Consultant
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.consultant_rating import (
    SCORES,
    ConsultantRating,
    ConsultantRatings,
    ScoredConsultantRating,
)
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.persistence_service_async import (
    select_questionnaire_statuses,
)
from data_questionnaire_agent.service.persistence_service_consultants_async import (
    read_consultants,
    read_session_consultant_ratings,
    save_session_consultant_ratings,
)
from data_questionnaire_agent.service.prompt_support import (
    prompt_factory_generic,
)
from data_questionnaire_agent.toml_support import get_prompts

CONSULTANT_BATCH_SIZE = 10


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


async def convert_all_consultants(offset: int = None, limit: int = None) -> str:
    consultants = await read_consultants(offset, limit)
    if len(consultants) == 0:
        return ""
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
    questions_answers: Questionnaire, conditional_advice: ConditionalAdvice, cvs: str
) -> ConsultantCallData:
    return {
        "questions_answers": str(questions_answers),
        "conditional_advice": str(conditional_advice),
        "cvs": cvs,
    }


async def calculate_consultant_ratings_for(
    session_id, language: str = "en"
) -> ConsultantRatings | None:
    cached_consultant_ratings = await read_session_consultant_ratings(session_id)
    if (
        cached_consultant_ratings
        and len(cached_consultant_ratings.consultant_ratings) > 0
    ):
        # Return cached
        return cached_consultant_ratings
    questionnaire_statuses = await select_questionnaire_statuses(session_id)
    if not questionnaire_statuses:
        return None
    final_report_list = [qs for qs in questionnaire_statuses if qs.final_report]
    if not final_report_list:
        return None
    advice_dict = json.loads(final_report_list[0].question)
    advice = ConditionalAdvice.parse_obj(advice_dict)

    consultant_cvs = []
    start = 0
    while True:
        cvs = await convert_all_consultants(start, start + CONSULTANT_BATCH_SIZE)
        if cvs == "":
            break
        consultant_cvs.append(cvs)
        start += CONSULTANT_BATCH_SIZE

    consultant_ratings: list[ConsultantRating] = []
    invocations = []
    for cvs in consultant_cvs:
        prompt_data = await prepare_consultant_call(
            Questionnaire(questions=questionnaire_statuses), advice, cvs
        )
        runnable_sequence = create_structured_consultant_call(language)
        invocations.append(runnable_sequence.ainvoke(prompt_data))

    try:
        crs: list[ConsultantRatings] = await asyncio.gather(*invocations)
        for cr in crs:
            consultant_ratings.extend(cr.consultant_ratings)

        consultant_ratings = sorted(
            [
                ScoredConsultantRating(
                    analyst_name=cr.analyst_name,
                    analyst_linkedin_url=cr.analyst_linkedin_url,
                    reasoning=cr.reasoning,
                    rating=cr.rating,
                    score=SCORES[cr.rating],
                )
                for cr in consultant_ratings
            ],
            key=lambda cr: cr.score,
            reverse=True,
        )
    except Exception as e:
        logger.exception(e)
    try:
        # Try to cache results
        await save_session_consultant_ratings(
            session_id, ConsultantRatings(consultant_ratings=consultant_ratings)
        )
        return await read_session_consultant_ratings(session_id) # read with extra data, like photos.
    except Exception as e:
        logger.error(f"Failed to save consultant ratings: {e}")
    return ConsultantRatings(consultant_ratings=consultant_ratings)
