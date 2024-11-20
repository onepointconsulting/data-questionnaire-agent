from typing import Union
import httpx

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger


async def graphrag_context(question: str) -> Union[str, None]:
    params = {
        "question": question,
        "use_context_records": False,
        "search": cfg.graphrag_mode,
        "context_size": cfg.graphrag_context_size
    }
    
    params = {key: value for key, value in params.items() if value is not None}

    async with httpx.AsyncClient() as client:

        try:
            response = await client.get(f"{cfg.graphrag_base_url}/context", params=params)
            
            if response.status_code == 200:
                json_result = response.json()
                if "context_text" in json_result:
                    return json_result["context_text"]
                else:
                    logger.warn("Could not find context_text field in json")
                    return None
            else:
                print(f"Failed with status code {response.status_code}: {response.text}")
        except httpx.RequestError as exc:
            logger.exception("Failed to process query to fetch graphrag context.")
            return None
        

if __name__ == "__main__":
    import asyncio

    result = asyncio.run(graphrag_context("What are the main topics?"))
    with open("./xxx_test_context.txt", "w", encoding="utf-8") as f:
        f.write(result)
    print(len(result))
