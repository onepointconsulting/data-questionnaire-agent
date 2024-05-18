from typing import List, Any, Optional, Type

from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain.agents import initialize_agent, AgentType, AgentExecutor
from duckduckgo_search import DDGS

from data_questionnaire_agent.config import cfg

RESULT_LIMIT = 5


class SearchTermsInput(BaseModel):
    """Search terms used for the search"""

    search_terms: List[str] = Field(
        ...,
        description="Search terms used to get more information from the search engine",
    )


class DuckDuckGoTool(BaseTool):
    name = "get_search_duck_duck_go"
    description = "Useful to find search results on all possible topics. It produces searches for information via duck duck go search engine."

    def _run(self, search_terms: List[str]) -> Any:
        """Use the tool.

        Add run_manager: Optional[CallbackManagerForToolRun] = None
        to child implementations to enable tracing,
        """
        search_res = text_search("".join(search_terms), limit=RESULT_LIMIT)
        return "\n".join([r["body"] for r in search_res])

    args_schema: Optional[Type[BaseModel]] = SearchTermsInput


def create_clarification_agent() -> AgentExecutor:
    tools = [DuckDuckGoTool()]
    return initialize_agent(
        tools, cfg.llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True
    )


def text_search(input: str, limit: int = 10) -> List[dict]:
    from itertools import islice

    res_list = []
    with DDGS() as ddgs:
        for r in islice(
            ddgs.text(input, region="wt-wt", safesearch="off", timelimit="y"), limit
        ):
            res_list.append(r)
    return res_list


def answers(input: str):
    with DDGS() as ddgs:
        for r in ddgs.answers(input):
            print(r)


if __name__ == "__main__":

    def test_search():
        res_list = text_search("Dark data")
        for res in res_list:
            print(res)

    tool = DuckDuckGoTool(
        name="search_duck_duck_go",
        description="Used to find answers and explanations based on keywords",
    )
    res = tool.run({"search_terms": ["Weather in London tomorrow"]})
    from data_questionnaire_agent.log_init import logger

    logger.info(res)
    agent_executor = create_clarification_agent()
    response = agent_executor.run("What is dark data?")
    logger.info("Agent response: %s", response)
    logger.info("Agent response type: %s", type(response))
