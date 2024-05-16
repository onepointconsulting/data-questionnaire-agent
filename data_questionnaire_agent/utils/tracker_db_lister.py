from typing import Optional
from pathlib import Path
import csv
import sys

from data_questionnaire_agent.log_init import logger
from chainlit.onepoint.tracker_db import ONEPOINT_SQL_LITE_DB, list_activity_log


TRACKING_FIELD_PROPERTIES = [
    {"name": "id"},
    {"name": "operation"},
    {"name": "user_id"},
    {"name": "session_id"},
    {"name": "message"},
    {"name": "timestamp"},
]


def write_log(file: Optional[Path] = None):
    logger.info("Database location: %s", ONEPOINT_SQL_LITE_DB)
    logger.info("")

    output = sys.stdout
    if file is not None:
        output = open(file, "w")
    logwriter = csv.writer(output, delimiter=",", lineterminator="\n")
    logwriter.writerow([f["name"] for f in TRACKING_FIELD_PROPERTIES])

    for row in list_activity_log():
        logwriter.writerow(row)

    output.close()


if __name__ == "__main__":
    write_log()
