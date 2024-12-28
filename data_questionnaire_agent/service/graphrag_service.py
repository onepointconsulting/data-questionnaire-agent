from typing import Union

import httpx

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger


async def graphrag_context(question: str) -> Union[str, None]:
    params = {
        "question": question,
        "use_context_records": False,
        "search": cfg.graphrag_mode,
        "context_size": cfg.graphrag_context_size,
        "project": cfg.graphrag_project
    }

    params = {key: value for key, value in params.items() if value is not None}

    headers = {
        "Authorization": f"Bearer {cfg.graphrag_jwt}"  # Add the JWT to the Authorization header
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{cfg.graphrag_base_url}/context", params=params, headers=headers
            )

            if response.status_code == 200:
                json_result = response.json()
                if "context_text" in json_result:
                    return json_result["context_text"]
                else:
                    logger.warning("Could not find context_text field in json")
                    return None
            else:
                logger.warning(
                    f"Failed with status code {response.status_code}: {response.text}"
                )
                return None
        except httpx.RequestError:
            logger.exception("Failed to process query to fetch graphrag context.")
            return None
