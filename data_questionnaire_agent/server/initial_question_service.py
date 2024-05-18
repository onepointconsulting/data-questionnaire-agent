from typing import List

from langchain.chains import LLMChain
from langchain.chains.openai_functions import create_structured_output_chain

from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from data_questionnaire_agent.model.openai_schema import ResponseQuestions

from data_questionnaire_agent.config import cfg

from data_questionnaire_agent.toml_support import prompts


def prompt_factory_generic(
    section: dict, input_variables: List[str]
) -> ChatPromptTemplate:
    human_message = section["human_message"]
    prompt_msgs = [
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                template=section["system_message"], input_variables=[]
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=human_message,
                input_variables=input_variables,
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=prompts["general_messages"]["tip_correct_format"],
                input_variables=[],
            )
        ),
        HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=prompts["general_messages"]["tip_language"],
                input_variables=[],
            )
        ),
    ]
    return ChatPromptTemplate(messages=prompt_msgs)


def prompt_factory_initial_questions() -> ChatPromptTemplate:
    section = prompts["questionnaire"]["initial"]
    return prompt_factory_generic(
        section,
        [
            "knowledge_base",
            "question",
            "answer",
            "questions_per_batch",
        ],
    )


def chain_factory_initial_question() -> LLMChain:
    return create_structured_output_chain(
        ResponseQuestions,
        cfg.llm,
        prompt_factory_initial_questions(),
        verbose=cfg.verbose_llm,
    )


def prepare_initial_question(
    question: str,
    answer: str,
    questions_per_batch: int = prompts["general_settings"]["questions_per_batch"],
    knowledge_base: str = "",
) -> dict:
    return {
        "knowledge_base": knowledge_base,
        "question": question,
        "answer": answer,
        "questions_per_batch": questions_per_batch,
    }
