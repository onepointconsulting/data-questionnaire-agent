from time import sleep

from openai import AsyncOpenAI
from openai.types.responses.response import Response

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.application_schema import (
    QuestionAnswer,
    Questionnaire,
)
from data_questionnaire_agent.model.deep_research import (
    Citation,
    DeepResearchAdviceInput,
    DeepResearchAdviceOutput,
)
from data_questionnaire_agent.toml_support import get_prompts


class DeepResearchCallback:
    async def on_response_update(self, response: Response):
        logger.info(f"Current status: {response.status}")

    async def on_response_complete(self, output: DeepResearchAdviceOutput):
        logger.info(output.deep_research_output)


async def deep_research(
    deep_research_advice_input: DeepResearchAdviceInput,
    language: str = "en",
    callback: DeepResearchCallback = None,
) -> DeepResearchAdviceOutput:
    prompts = get_prompts(language)
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
        sleep(5)
        response = await client.responses.retrieve(response.id)

    if callback:
        await callback.on_response_update(response)

    final_output = response.output[-1].content[0].text
    citations = []
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
        deep_research_output=final_output,
        citations=citations,
    )
    if callback:
        await callback.on_response_complete(output)
    return output


