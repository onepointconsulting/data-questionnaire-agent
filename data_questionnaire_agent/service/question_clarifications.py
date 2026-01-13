from typing import AsyncIterator

from langchain_core.messages import BaseMessageChunk
from langchain_core.prompts import ChatPromptTemplate

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.service.persistence_service_prompt_async import get_prompts



async def prompt_factory_question_clarifications(language: str) -> ChatPromptTemplate:
    extraction_prompts = await get_prompts(language)["questionnaire"]["clarification"]
    return ChatPromptTemplate.from_messages(
        [
            ("system", extraction_prompts["system_message"]),
            ("human", extraction_prompts["human_message"]),
        ]
    )


async def chain_factory_question_clarifications(
    question: str, language: str
) -> AsyncIterator[BaseMessageChunk]:
    input = await prompt_factory_question_clarifications(language).format(question=question)
    return cfg.llm_stream.astream(input)


if __name__ == "__main__":
    import asyncio

    async def stream_response():
        question = "What is the meaning of data governance?"
        async for token in await chain_factory_question_clarifications(question):
            print(token.content, end="", flush=True)

    asyncio.run(stream_response())
