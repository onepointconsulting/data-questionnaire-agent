from data_questionnaire_agent.log_init import logger
from chainlit.onepoint.tracker_db import ONEPOINT_SQL_LITE_DB, list_activity_log

if __name__ == "__main__":
    logger.info("Database location: %s", ONEPOINT_SQL_LITE_DB)
    logger.info("")
    for row in list_activity_log():
        logger.info(row)
