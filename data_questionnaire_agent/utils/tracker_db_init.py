from pathlib import Path
from chainlit.onepoint.tracker_db import ONEPOINT_SQL_LITE_DB, create_table

if __name__ == "__main__":
    db_path = Path(ONEPOINT_SQL_LITE_DB)
    if not db_path.exists():
        db_path.mkdir(parents=True)
    assert db_path.exists()
    create_table()