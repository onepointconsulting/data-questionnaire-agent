from typing import Union

import httpx

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.context import Context


async def graphrag_context(question: str) -> Union[Context, None]:
    params = {
        "question": question,
        "use_context_records": False,
        "search": cfg.graphrag_mode,
        "context_size": cfg.graphrag_context_size,
        "project": cfg.graphrag_project,
        "engine": cfg.graphrag_engine,
        "format": "json_string_with_json",
    }

    params = {key: value for key, value in params.items() if value is not None}

    headers = {
        "Authorization": f"Bearer {cfg.graphrag_jwt}"  # Add the JWT to the Authorization header
    }

    async with httpx.AsyncClient() as client:
        timeout = httpx.Timeout(
            connect=5.0,  # 5 seconds for connection establishment
            read=cfg.graphrag_read_timeout,  # 20 seconds for reading response
            write=10.0,  # 10 seconds for sending request data
            pool=5.0,  # 5 seconds for acquiring a connection from the pool
        )
        context_url = f"{cfg.graphrag_base_url}/context"
        try:
            response = await client.get(
                context_url, params=params, headers=headers, timeout=timeout
            )

            if response.status_code == 200:
                json_result = response.json()
                if "context_text" in json_result:
                    return Context(**json_result)
                else:
                    logger.warning("Could not find context_text field in json")
                    return None
            else:
                logger.warning(
                    f"Failed with status code {response.status_code}: {response.text}"
                )
                return None
        except httpx.RequestError:
            logger.exception(
                f"Failed to process query ({context_url}) to fetch graphrag context."
            )
            return None


if __name__ == "__main__":
    import asyncio

    res = asyncio.run(
        graphrag_context(
            "Which areas of your data ecosystem are you most converned about?"
        )
    )
    print(res)
