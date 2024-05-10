from data_questionnaire_agent.config import cfg


def read_file(file_name: str) -> str:
    with open(cfg.raw_text_folder / file_name, "r", encoding="utf-8") as f:
        return f.read()


# provide_data_quality throw an error if the file does not exist
def provide_data_quality() -> str:
    # Check if "data quality.txt" exists in the raw_text_folder, if not, check if "AboutRefugees.txt" exists
    # return read_file("data quality.txt" if not "refugee" in str(cfg.raw_text_folder) else "AboutRefugees.txt")

    if "data quality.txt" in str(cfg.raw_text_folder):
        return read_file("data quality.txt")
    else:
        return read_file("AboutRefugees.txt")


def provide_data_ops() -> str:
    # return read_file("dataops.txt" if not "refugee" in str(cfg.raw_text_folder) else "AsylumInAustria.txt")
    if "dataops.txt" in str(cfg.raw_text_folder):
        return read_file("dataops.txt")
    else:
        return read_file("AsylumInAustria.txt")


def provide_knowledge_base() -> str:
    return f"{provide_data_quality()}\n\n{provide_data_ops()}"
