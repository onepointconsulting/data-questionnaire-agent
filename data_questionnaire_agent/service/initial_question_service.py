from typing import Callable, List, Union

from langchain.chains.llm import LLMChain
from langchain.chains.openai_functions import create_structured_output_chain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.openai_schema import ResponseQuestions
from data_questionnaire_agent.toml_support import get_prompts


def prompt_factory_generic(
    section: dict,
    input_variables: List[str],
    prompts: object,
    prompt_transform: Union[Callable, None] = None,
) -> ChatPromptTemplate:
    human_message = section["human_message"]
    human_message = (
        prompt_transform(human_message)
        if prompt_transform is not None
        else human_message
    )
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


def prompt_factory_initial_questions(language: str) -> ChatPromptTemplate:
    prompts = get_prompts(language)
    section = prompts["questionnaire"]["initial"]
    return prompt_factory_generic(
        section,
        [
            "knowledge_base",
            "question",
            "answer",
            "questions_per_batch",
        ],
        prompts,
    )


def chain_factory_initial_question(language: str) -> LLMChain:
    return create_structured_output_chain(
        ResponseQuestions,
        cfg.llm,
        prompt_factory_initial_questions(language),
        verbose=cfg.verbose_llm,
    )


def prepare_initial_question(
    question: str,
    answer: str,
    questions_per_batch: int = 1,
    knowledge_base: str = "",
) -> dict:
    return {
        "knowledge_base": knowledge_base,
        "question": question,
        "answer": answer,
        "questions_per_batch": questions_per_batch,
    }


if __name__ == "__main__":
    import asyncio

    from data_questionnaire_agent.log_init import logger
    from data_questionnaire_agent.service.knowledge_base_service import fetch_context

    language = "en"
    initial_question = get_prompts(language)["questionnaire"]["initial"]["question"]
    assert initial_question is not None

    answer = "Expired Passport"  # Supposed the client answer
    search_res = asyncio.run(fetch_context(answer))
    input = prepare_initial_question(
        question=initial_question,
        answer=answer,
        questions_per_batch=1,
        knowledge_base=search_res,
    )
    chain = chain_factory_initial_question(language)
    res: dict = chain.invoke(input)
    assert res is not None
    response_questions: ResponseQuestions = res["function"]

    logger.info("Results: ")
    logger.info(response_questions)
