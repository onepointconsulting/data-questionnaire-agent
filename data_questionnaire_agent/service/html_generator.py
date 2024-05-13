from pathlib import Path
from datetime import datetime

from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.report_enhancement_service import (
    replace_bold_markdown,
)

import jinja2
import pdfkit

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger


def generate_html(questionnaire: Questionnaire, advices: ConditionalAdvice) -> str:
    timestamp = datetime.today().strftime("%A, %b %d %Y")
    context = {
        "questionnaire": questionnaire.to_html(),
        "advices": replace_bold_markdown(advices.to_advice_html()),
        "avoids": replace_bold_markdown(advices.to_avoid_html()),
        "positive_outcomes": replace_bold_markdown(advices.positive_outcomes_html()),
        "timestamp": timestamp,
    }
    template_loader = jinja2.FileSystemLoader(cfg.template_location)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("results-template.html")
    return template.render(context)


def generate_pdf_from(questionnaire: Questionnaire, advices: ConditionalAdvice) -> Path:
    if questionnaire is None:
        return None
    html = generate_html(questionnaire, advices)
    logger.info("PDF html: %s", html)
    file_name = (
        cfg.pdf_folder / f"Advice from the {cfg.product_title}_{generate_iso()}.pdf"
    )
    logger.info("PDF to be created file name: %s", file_name)
    config = pdfkit.configuration(wkhtmltopdf=cfg.wkhtmltopdf_binary.as_posix())
    pdfkit.from_string(html, file_name, configuration=config)
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
