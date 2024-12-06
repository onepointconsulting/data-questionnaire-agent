from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

from data_questionnaire_agent.model.report_aggregation_schema import ReportDocumentSummarization
from data_questionnaire_agent.service.prompt_support import (
    factory_prompt,
)
from data_questionnaire_agent.config import cfg



def prompt_factory_summarization_prompt(language: str) -> ChatPromptTemplate:
    return factory_prompt(
        lambda prompt: prompt["reporting"]["summarization_prompt"],
        ["full_questionnaire"],
        language,
    )


def create_summarization_call(language: str = "en") -> RunnableSequence:
    model = cfg.llm.with_structured_output(ReportDocumentSummarization)
    prompt = prompt_factory_summarization_prompt(language)
    return prompt | model
