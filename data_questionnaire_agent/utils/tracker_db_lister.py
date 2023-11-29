import csv
import sys

from data_questionnaire_agent.log_init import logger
from chainlit.onepoint.tracker_db import ONEPOINT_SQL_LITE_DB, list_activity_log


class TrackingPositions:
    ID = 0
    OPERATION = 1
    USER_ID = 2
    SESSION_ID = 3
    MESSAGE = 4
    TIMESTAMP = 5


TRACKING_FIELD_PROPERTIES = [
    {"name": "id"},
    {"name": "operation"},
    {"name": "user_id"},
    {"name": "session_id"},
    {"name": "message"},
    {"name": "timestamp"},
]


if __name__ == "__main__":
    logger.info("Database location: %s", ONEPOINT_SQL_LITE_DB)
    logger.info("")

    logwriter = csv.writer(sys.stdout, delimiter=",", lineterminator="\n")
    logwriter.writerow([f['name'] for f in TRACKING_FIELD_PROPERTIES])

    for row in list_activity_log():
        # id: int = row[TrackingPositions.ID]
        # operation: str = row[TrackingPositions.OPERATION]
        # user_id: int = row[TrackingPositions.USER_ID]
        # session_id: str = row[TrackingPositions.SESSION_ID]
        # message: str = row[TrackingPositions.MESSAGE]
        # timestamp: str = row[TrackingPositions.TIMESTAMP]
        logwriter.writerow(row)
        
