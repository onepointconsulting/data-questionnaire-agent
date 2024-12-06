from langchain.chains.llm import LLMChain
from langchain.chains.openai_functions import create_structured_output_chain
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.openai_schema import ResponseQuestions
from data_questionnaire_agent.model.session_configuration import (
    ChatType,
    SessionProperties,
)
from data_questionnaire_agent.service.prompt_support import (
    prompt_factory_generic,
)
from data_questionnaire_agent.toml_support import get_prompts


def divergent_prompt_transformer(prompt: str, language: str = "en") -> str:
    defaultExclusions = [
        "Main questionnaire topic:",
        "The questions should explore topics related to the main topic",
    ]
    exclusions_by_language = {
        "en": defaultExclusions,
        "de": [
            "Hauptfragebogen-Thema:",
            "Die Fragen sollten Themen im Zusammenhang mit dem Hauptthema",
        ],
    }

    # Get the exclusions for the selected language
    exclusions = exclusions_by_language.get(language, defaultExclusions)

    # Process the lines
    lines = [
        line for line in prompt.splitlines() if not any(e in line for e in exclusions)
    ]

    return "\n".join(lines)


def prompt_factory_secondary_questions(
    session_properties: SessionProperties,
) -> ChatPromptTemplate:
    language = session_properties.session_language
    prompt_transformer = None
    if session_properties.chat_type == ChatType.DIVERGING:
        prompt_transformer = lambda p: divergent_prompt_transformer(
            p, language=language
        )

    prompts = get_prompts(language)
    section = prompts["questionnaire"]["secondary"]
    return prompt_factory_generic(
        section,
        [
            "knowledge_base",
            "questions_answers",
            "answers",
            "questions_per_batch",
        ],
        prompts,
        prompt_transformer,
    )


def create_structured_question_call(
    session_properties: SessionProperties,
) -> RunnableSequence:
    model = cfg.llm.with_structured_output(ResponseQuestions)
    prompt = prompt_factory_secondary_questions(session_properties)
    return prompt | model


def chain_factory_secondary_question(session_properties: SessionProperties) -> LLMChain:
    return create_structured_output_chain(
        ResponseQuestions,
        cfg.llm,
        prompt_factory_secondary_questions(session_properties),
        verbose=cfg.verbose_llm,
    )


def prepare_secondary_question(
    questionnaire: Questionnaire,
    knowledge_base: str,
    questions_per_batch: int = cfg.questions_per_batch,
) -> dict:
    return {
        "knowledge_base": knowledge_base,
        "questions_answers": str(questionnaire),
        "answers": questionnaire.answers_str(),
        "questions_per_batch": questions_per_batch,
        "questionnaire_topic": questionnaire.questions[0].answer
        if len(questionnaire.questions) > 0
        else "",
    }
