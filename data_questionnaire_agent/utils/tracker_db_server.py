import mimetypes

from fastapi import Request, HTTPException
from chainlit.server import app
from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.utils.tracker_db_lister import write_log
from fastapi.responses import FileResponse

PARAM_SECURITY_KEY = "security_key"


@app.get("/onepoint/logs")
async def get_report(request: Request):
    params = request.query_params
    security_key = params.get(PARAM_SECURITY_KEY)

    if security_key != cfg.tracker_db_logs_password:
        raise HTTPException(
            status_code=403,
            detail=f"Please add the {PARAM_SECURITY_KEY} query parameter with the correct security key",
        )
        # raise HTTPException(status_code=403, detail=f"Please add the {PARAM_SECURITY_KEY} query parameter with the correct security key")
    # XXX : csv_file = cfg.project_root / "report.csv"
    csv_file = cfg.project_root / "report.csv"
    write_log(csv_file)

    media_type, _ = mimetypes.guess_type(csv_file)

    return FileResponse(csv_file, media_type=media_type, filename=csv_file.name)
