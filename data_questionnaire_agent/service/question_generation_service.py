from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)
from langchain_core.runnables.base import RunnableSequence

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.confidence_schema import ConfidenceRating
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
            "confidence_report",
        ],
        prompts,
        prompt_transformer,
    )


def prompt_factory_recreate_question(
    session_properties: SessionProperties,
) -> ChatPromptTemplate:
    language = session_properties.session_language
    regenerate_template = prompt_factory_secondary_questions(session_properties)
    # Build the normal prompt template and then modify it to avoid code duplication
    main_message_index = 1
    main_template: HumanMessagePromptTemplate = regenerate_template.messages[
        main_message_index
    ]
    main_template_prompt: PromptTemplate = main_template.prompt
    template, input_variables = (
        main_template_prompt.template,
        main_template_prompt.input_variables,
    )
    input_variables.append("previous_question")
    insertion_mark = "\n==== KNOWLEDGE BASE START ====\n"
    insertion_index = template.find(insertion_mark)
    prompts = get_prompts(language)
    # manipulate the template
    section_mod_human_message = prompts["questionnaire"]["secondary_regenerate"][
        "human_message"
    ]
    previous = template[0:insertion_index]
    after = template[insertion_index:]
    changed_template = f"""{previous}
{section_mod_human_message}
{after}
"""
    main_template_prompt.template = changed_template
    return regenerate_template


def create_structured_question_call(
    session_properties: SessionProperties, is_recreate: bool = False
) -> RunnableSequence:
    model = cfg.llm.with_structured_output(ResponseQuestions)
    prompt = (
        prompt_factory_secondary_questions(session_properties)
        if not is_recreate
        else prompt_factory_recreate_question(session_properties)
    )
    return prompt | model


def chain_factory_secondary_question(
    session_properties: SessionProperties,
) -> RunnableSequence:
    model = cfg.llm.with_structured_output(ResponseQuestions)
    prompt = prompt_factory_secondary_questions(session_properties)
    return prompt | model


def prepare_secondary_question(
    questionnaire: Questionnaire,
    knowledge_base: str,
    questions_per_batch: int = cfg.questions_per_batch,
    is_recreate: bool = False,
    confidence_rating: ConfidenceRating | None = None,
) -> dict:
    confidence_report = "No confidence report available."
    if confidence_rating is not None:
        confidence_report = confidence_rating.reasoning
    params = {
        "knowledge_base": knowledge_base,
        "questions_answers": str(questionnaire),
        "answers": questionnaire.answers_str(),
        "questions_per_batch": questions_per_batch,
        "questionnaire_topic": (
            questionnaire.questions[0].answer
            if len(questionnaire.questions) > 0
            else ""
        ),
        "confidence_report": confidence_report,
    }
    if is_recreate:
        params["previous_question"] = questionnaire.questions[-1].question
    return params
