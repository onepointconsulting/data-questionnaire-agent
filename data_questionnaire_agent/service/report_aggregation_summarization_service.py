from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.report_aggregation_schema import (
    ReportDocumentSummarization,
)
from data_questionnaire_agent.service.prompt_support import (
    factory_prompt,
)

KEY_QUESTIONNAIRE = "full_questionnaire"


async def prompt_factory_summarization_prompt(language: str) -> ChatPromptTemplate:
    return await factory_prompt(
        lambda prompt: prompt["reporting"]["summarization_prompt"],
        [KEY_QUESTIONNAIRE],
        language,
    )


async def create_summarization_call(language: str = "en") -> RunnableSequence:
    model = cfg.llm.with_structured_output(ReportDocumentSummarization)
    prompt = await prompt_factory_summarization_prompt(language)
    return prompt | model


async def aexecute_summarization_batch(
    inputs: list[str], batch_size: int = 2, language: str = "en"
) -> list[ReportDocumentSummarization]:
    chain = await create_summarization_call(language)
    summaries = []
    inputs_dict = [{KEY_QUESTIONNAIRE: s} for s in inputs]
    batches = [
        inputs_dict[i : i + batch_size] for i in range(len(inputs_dict))[::batch_size]
    ]
    for i, b in enumerate(batches):
        try:
            res = await chain.abatch(b)
            summaries.extend(res)
            logger.info(f"Summarized {(i + batch_size) * batch_size} records.")
        except Exception as e:
            logger.exception(e)
    return summaries


async def aexecute_summarization_batch_str(
    inputs: list[str], batch_size: int = 2, language: str = "en"
) -> list[str]:
    logger.info("Summarizing %d questionnaires.", len(inputs))
    return [
        summ.summary
        for summ in await aexecute_summarization_batch(inputs, batch_size, language)
    ]
