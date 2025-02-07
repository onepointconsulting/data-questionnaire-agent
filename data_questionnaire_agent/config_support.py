import os

def create_db_conn_str() -> str:
    db_name = os.getenv("DB_NAME")
    assert db_name is not None
    db_user = os.getenv("DB_USER")
    assert db_user is not None
    db_host = os.getenv("DB_HOST")
    assert db_host is not None
    db_port = os.getenv("DB_PORT")
    assert db_port is not None
    db_port = int(db_port)
    db_password = os.getenv("DB_PASSWORD")
    assert db_password is not None
    
    return f"dbname={db_name} user={db_user} password={db_password} host={db_host} port={db_port}"