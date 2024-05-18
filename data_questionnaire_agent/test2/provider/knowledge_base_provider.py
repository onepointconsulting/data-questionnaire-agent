from data_questionnaire_agent.config import cfg


def read_file(file_name: str) -> str:
    with open(cfg.raw_text_folder / file_name, "r", encoding="utf-8") as f:
        return f.read()


def provide_data_quality() -> str:
    return read_file("data quality.txt")


def provide_data_ops() -> str:
    return read_file("dataops.txt")


def provide_data_quality_ops() -> str:
    return f"{provide_data_quality()}\n\n{provide_data_ops()}"
