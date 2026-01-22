from langchain_core.prompts import (
    ChatPromptTemplate,
)
from langchain_core.runnables import RunnableSequence

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.openai_schema import ResponseQuestions
from data_questionnaire_agent.service.persistence_service_prompt_async import (
    get_prompts,
)
from data_questionnaire_agent.service.prompt_support import prompt_factory_generic


async def prompt_factory_initial_questions(language: str) -> ChatPromptTemplate:
    prompts = await get_prompts(language)
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


async def chain_factory_initial_question(language: str) -> RunnableSequence:
    model = cfg.llm.with_structured_output(ResponseQuestions)
    prompt = await prompt_factory_initial_questions(language)
    return prompt | model


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

    async def test_initial_question():
        language = "en"
        prompts = await get_prompts(language)
        initial_question = prompts["questionnaire"]["initial"]["question"]
        assert initial_question is not None

        answer = "Expired Passport"  # Supposed the client answer
        search_res = await fetch_context(answer)
        input = prepare_initial_question(
            question=initial_question,
            answer=answer,
            questions_per_batch=1,
            knowledge_base=search_res.context_text,
        )
        chain = await chain_factory_initial_question(language)
        res: dict = chain.invoke(input)
        assert res is not None
        response_questions: ResponseQuestions = res["function"]

        logger.info("Results: ")
        logger.info(response_questions)

    asyncio.run(test_initial_question())
