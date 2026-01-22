import asyncio

import socketio
from openai import AsyncOpenAI
from openai.types.responses.response import Response

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.deep_research import (
    Citation,
    DeepResearchAdviceOutput,
    DeepResearchStatus,
)
from data_questionnaire_agent.model.deep_research_input import DeepResearchAdviceInput
from data_questionnaire_agent.server.socket_commands import Commands
from data_questionnaire_agent.service.persistence_deep_research_async import (
    read_deep_research,
    save_deep_research,
)
from data_questionnaire_agent.service.persistence_service_async import (
    select_questionnaire,
)
from data_questionnaire_agent.service.persistence_service_prompt_async import (
    get_prompts,
)


class DeepResearchCallback:
    async def on_response_update(self, response: Response):
        logger.info(f"Current status: {response.status}")
        logger.info(f"Response: {response.model_dump_json()}")

    async def on_response_complete(self, output: DeepResearchAdviceOutput):
        logger.info(output.deep_research_output)

    async def on_response_fail(self, message: str):
        logger.error(f"Deep research failed: {message}")


class DeepResearchWebsocketCallback(DeepResearchCallback):
    def __init__(self, sid: str, sio: socketio.AsyncServer, advice: str):
        self.sid = sid
        self.sio = sio
        self.advice = advice

    async def on_response_update(self, response: Response):
        await super().on_response_update(response)
        try:
            data = DeepResearchStatus(
                status=response.status, advice=self.advice
            ).model_dump_json()
            logger.info(
                f"Emitting DEEP_RESEARCH_UPDATE to sid={self.sid}, status={response.status}"
            )
            await self.sio.emit(
                Commands.DEEP_RESEARCH_UPDATE.value,
                data,
                to=self.sid,
            )
            logger.info(f"Successfully emitted DEEP_RESEARCH_UPDATE to sid={self.sid}")
        except Exception as e:
            logger.error(f"Error emitting deep research update: {e}", exc_info=True)

    async def on_response_complete(self, output: DeepResearchAdviceOutput):
        await super().on_response_complete(output)
        try:
            data = output.model_dump_json()
            logger.info(f"Emitting DEEP_RESEARCH_COMPLETE to sid={self.sid}")
            await self.sio.emit(
                Commands.DEEP_RESEARCH_COMPLETE.value,
                data,
                to=self.sid,
            )
            logger.info(
                f"Successfully emitted DEEP_RESEARCH_COMPLETE to sid={self.sid}"
            )
        except Exception as e:
            logger.error(f"Error emitting deep research complete: {e}", exc_info=True)


async def deep_research_websocket(
    session_id: str,
    advice: str,
    sid: str,
    sio: socketio.AsyncServer,
) -> DeepResearchAdviceOutput | None:
    saved_deep_researches = await read_deep_research(session_id, advice)
    saved_deep_research = saved_deep_researches.outputs
    if len(saved_deep_research) > 0:
        return saved_deep_research[0]
    questionnaire = await select_questionnaire(session_id)
    deep_research_advice_input = DeepResearchAdviceInput(
        questionnaire=questionnaire,
        conditional_advice=advice,
    )
    callback = DeepResearchWebsocketCallback(sid, sio, advice)
    deep_research_output = await deep_research(
        deep_research_advice_input, callback=callback
    )
    if deep_research_output is None:
        return None
    await save_deep_research(session_id, advice, deep_research_output)
    return deep_research_output


async def deep_research(
    deep_research_advice_input: DeepResearchAdviceInput,
    language: str = "en",
    callback: DeepResearchCallback = None,
) -> DeepResearchAdviceOutput | None:
    prompts = await get_prompts(language)
    assert (
        "deep_research" in prompts
    ), "Make sure that you have the deep research prompt in your prompts file."
    section = prompts["deep_research"]["advice"]
    client = AsyncOpenAI()
    user_query = section["human_message"].format(
        questions_answers=str(deep_research_advice_input.questionnaire),
        conditional_advice=deep_research_advice_input.conditional_advice,
    )
    response = await client.responses.create(
        model=cfg.deep_research_model,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": section["system_message"],
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": user_query,
                    }
                ],
            },
        ],
        reasoning={"summary": "auto"},
        tools=[
            {"type": "web_search_preview"},
        ],
        background=True,
    )
    while response.status in {"queued", "in_progress"}:
        if callback:
            await callback.on_response_update(response)
        await asyncio.sleep(5)
        response = await client.responses.retrieve(response.id)

    if callback:
        await callback.on_response_update(response)

    final_output = response.output[-1].content[0].text
    citations = []
    if len(response.output) == 0:
        if callback:
            await callback.on_response_fail(
                f"No output from deep research response: {response.model_dump_json()}"
            )
        return None
    annotations = response.output[-1].content[0].annotations
    for i, citation in enumerate(annotations):
        citations.append(
            Citation(
                index=i,
                title=citation.title,
                url=citation.url,
                start_index=citation.start_index,
                end_index=citation.end_index,
                text=final_output[citation.start_index : citation.end_index],
            )
        )
    output = DeepResearchAdviceOutput(
        advice=deep_research_advice_input.conditional_advice,
        deep_research_output=final_output,
        citations=citations,
    )
    if callback:
        await callback.on_response_complete(output)
    return output
