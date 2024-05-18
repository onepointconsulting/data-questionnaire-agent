from pathlib import Path
import pprint
from chainlit.onepoint.tracker_db import ONEPOINT_SQL_LITE_DB, create_table
# ONEPOINT_SQL_LITE_DB = os.getenv("ONEPOINT_SQL_LITE_DB", "/tmp/ONEPOINT_SQL_LITE_DB.db")
if __name__ == "__main__":
    db_path = Path(ONEPOINT_SQL_LITE_DB)
    # db_path._parts = db_path._parts[:-1]
    db_path = db_path.parent
    if not db_path.exists():
        db_path.mkdir(parents=True)
    assert db_path.exists()
    create_table()
