from urllib.parse import urlencode

def create_download_url(file_path: str, cfg: object) -> str:
    query_params = urlencode({
        "engine": cfg.graphrag_engine,
        "project": cfg.graphrag_project,
        "file": file_path,
        "original_file": "true",
        "token": cfg.graphrag_jwt,
    })
    return f"{cfg.graphrag_base_url}/download/single_file?{query_params}"