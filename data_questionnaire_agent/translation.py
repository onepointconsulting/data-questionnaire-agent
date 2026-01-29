import i18n
from pathlib import Path

translations_path = Path(__file__).resolve().parent.parent / "i18n"
assert translations_path.exists(), f"Cannot find {translations_path}"

i18n.load_path.append(translations_path.as_posix())


def t(key: str, **kwargs):
    return i18n.t(f"messages.{key}", **kwargs)


if __name__ == "__main__":
    from data_questionnaire_agent.config import cfg

    print(
        t(
            "A big thank you for completing a session with",
            name=cfg.product_title,
            locale="de",
        )
    )
    print(t("db_insert_failed", locale="en"))
