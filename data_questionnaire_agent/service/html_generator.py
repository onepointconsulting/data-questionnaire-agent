import re
from datetime import datetime
from pathlib import Path

import jinja2
import pdfkit

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.report_enhancement_service import (
    replace_bold_markdown,
)
from data_questionnaire_agent.translation import t


def generate_html(
    questionnaire: Questionnaire, advices: ConditionalAdvice, language: str = "en"
) -> str:
    timestamp = datetime.today().strftime("%A, %b %d %Y")
    context = {
        "banner": t("banner_link", locale=language),
        "questionnaire": questionnaire.to_html(),
        "advices": replace_bold_markdown(advices.to_advice_html()),
        "avoids": replace_bold_markdown(advices.to_avoid_html()),
        "title_confidence": t("Confidence Degree", locale=language),
        "confidence": replace_bold_markdown(advices.confidence_html(language)),
        "positive_outcomes": replace_bold_markdown(advices.positive_outcomes_html()),
        "timestamp": timestamp,
        "big_thank_you": t(
            "A big thank you for completing a session with",
            name=cfg.product_title,
            locale=language,
        ),
        "intro_advice": t("intro_advice", locale=language),
        "offering_long": t("offering_long", locale=language),
        "personal_offer": t("A personal offer for you", locale=language),
        "produced_on": t("Produced on", locale=language),
        "love_feedback": t("We would love your feedback", locale=language),
        "for_more_info": t("for_more_info", locale=language),
        "title_potential_outcomes": t("Potential positive outcomes", locale=language),
        "title_transcript": t("Transcript", locale=language),
        "title_what_to_do": t("What you should do", locale=language),
        "title_what_to_avoid": t("What to avoid", locale=language),
    }
    template_loader = jinja2.FileSystemLoader(cfg.template_location)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("results-template.html")
    return template.render(context)


def generate_pdf_from(
    questionnaire: Questionnaire, advices: ConditionalAdvice, language: str = "en"
) -> Path:
    if questionnaire is None:
        return None
    html = generate_html(questionnaire, advices, language)
    logger.info("PDF html: %s", html)
    file_name = cfg.pdf_folder / f"generated_advice_{generate_iso()}.pdf"
    logger.info("PDF to be created file name: %s", file_name)
    config = pdfkit.configuration(wkhtmltopdf=cfg.wkhtmltopdf_binary.as_posix())
    pdfkit.from_string(
        html,
        file_name,
        configuration=config,
        verbose=True,
        options={"--enable-local-file-access": True},
    )
    logger.info("Created PDF: %s", file_name)
    return file_name


def generate_iso() -> str:
    current_time = datetime.now()
    return current_time.isoformat().replace(":", ".")


if __name__ == "__main__":
    from data_questionnaire_agent.test.provider.advice_provider import (
        create_simple_advice,
    )
    from data_questionnaire_agent.test.provider.questionnaire_provider import (
        create_questionnaire_2_questions,
    )

    questionnaire: Questionnaire = create_questionnaire_2_questions()
    advices: ConditionalAdvice = create_simple_advice()
    logger.info("PDF Path: %s", generate_pdf_from(questionnaire, advices))
