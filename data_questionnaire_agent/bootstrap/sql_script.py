import asyncio
import sys
from pathlib import Path

from data_questionnaire_agent.db_config import db_cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.service.db_bootstrap_service import execute_script

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Please enter one or more scripts as arguments.")
    if db_cfg.db_create:
        for script in sys.argv[1:]:
            logger.info(f"Processing {script}")
            script_path = Path(script)
            assert script_path.exists(), f"Cannot find {script}."
            res = asyncio.run(execute_script(script_path))
            if isinstance(res, bool):
                if res:
                    logger.info(f"Script {script} executed successfully.")
                else:
                    logger.error(f"Script {script} failed.")
            else:
                logger.error(f"An error has occurred: {res}")
    else:
        logger.info("DB creation turned off.")
