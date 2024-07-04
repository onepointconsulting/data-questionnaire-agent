import i18n
from data_questionnaire_agent.config import cfg

i18n.load_path.append(cfg.translation_path)


def t(key: str, **kwargs):
    return i18n.t(f"messages.{key}", **kwargs)


if __name__ == "__main__":
    print(
        t(
            "A big thank you for completing a session with",
            name=cfg.product_title,
            locale="de",
        )
    )
    print(t("db_insert_failed", locale="en"))
