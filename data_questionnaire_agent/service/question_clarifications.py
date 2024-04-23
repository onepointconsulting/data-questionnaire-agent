from typing import AsyncIterator

from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessageChunk

from data_questionnaire_agent.toml_support import prompts
from data_questionnaire_agent.config import cfg


def prompt_factory_question_clarifications() -> ChatPromptTemplate:
    extraction_prompts = prompts["questionnaire"]["clarification"]
    return ChatPromptTemplate.from_messages(
        [
            ("system", extraction_prompts["system_message"]),
            ("human", extraction_prompts["human_message"]),
        ]
    )


question_clarifications_prompt = prompt_factory_question_clarifications()


async def chain_factory_question_clarifications(
    question: str,
) -> AsyncIterator[BaseMessageChunk]:
    input = question_clarifications_prompt.format(question=question)
    return cfg.llm_stream.astream(input)


if __name__ == "__main__":
    import asyncio

    async def stream_response():
        question = "What is the meaning of data governance?"
        async for token in await chain_factory_question_clarifications(question):
            print(token.content, end="", flush=True)

    asyncio.run(stream_response())
