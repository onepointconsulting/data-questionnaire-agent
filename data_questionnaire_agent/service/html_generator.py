from datetime import datetime
from pathlib import Path

import jinja2
import pdfkit

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger

from data_questionnaire_agent.model.report_advice_schema import ReportAdviceData
from data_questionnaire_agent.service.report_enhancement_service import (
    replace_bold_markdown,
)
from data_questionnaire_agent.test.provider.advice_provider import (
    create_deep_research_outputs,
)
from data_questionnaire_agent.translation import t
from data_questionnaire_agent.service.advice_service import (
    combine_advices_and_deep_research_outputs,
)


def generate_html(report_advice_data: ReportAdviceData, language: str = "en") -> str:
    from data_questionnaire_agent.model.application_schema import Questionnaire
    from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
    from data_questionnaire_agent.model.deep_research import DeepResearchOutputs

    questionnaire: Questionnaire = report_advice_data.questionnaire
    advices: ConditionalAdvice = report_advice_data.advices
    deep_research_outputs: DeepResearchOutputs = (
        report_advice_data.deep_research_outputs
    )
    combine_advices_and_deep_research_outputs(advices, deep_research_outputs)
    timestamp = datetime.today().strftime("%A, %b %d %Y")
    context = {
        "title": t("Data Wellness Aggregation Report", locale=language),
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
        "confidence_degree_explanation_title": t(
            "confidence_degree_explanation_title", locale=language
        ),
        "confidence_degree_explanation_intro": t(
            "confidence_degree_explanation_intro", locale=language
        ),
        "confidence_degree_low": t("confidence_degree_low", locale=language),
        "confidence_degree_mediocre": t("confidence_degree_mediocre", locale=language),
        "confidence_degree_medium": t("confidence_degree_medium", locale=language),
        "confidence_degree_high": t("confidence_degree_high", locale=language),
        "confidence_degree_outstanding": t(
            "confidence_degree_outstanding", locale=language
        ),
        "confidence_degree_low_explanation": t(
            "confidence_degree_low_explanation", locale=language
        ),
        "confidence_degree_mediocre_explanation": t(
            "confidence_degree_mediocre_explanation", locale=language
        ),
        "confidence_degree_medium_explanation": t(
            "confidence_degree_medium_explanation", locale=language
        ),
        "confidence_degree_high_explanation": t(
            "confidence_degree_high_explanation", locale=language
        ),
        "confidence_degree_outstanding_explanation": t(
            "confidence_degree_outstanding_explanation", locale=language
        ),
        "confidence_image_location": t("confidence_image_location", locale=language),
    }
    template_loader = jinja2.FileSystemLoader(cfg.template_location)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("results-template.html")
    return template.render(context)


def generate_pdf_from(
    report_advice_data: ReportAdviceData, language: str = "en"
) -> Path | None:
    if report_advice_data.questionnaire is None or report_advice_data.advices is None:
        return None
    html = generate_html(report_advice_data, language)
    file_name = cfg.pdf_folder / f"generated_advice_{generate_iso()}.pdf"
    file_name_html = cfg.pdf_folder / f"generated_advice_{generate_iso()}.html"
    file_name_html.write_text(html, encoding="utf-8")
    logger.info("PDF to be created file name: %s", file_name)
    config = pdfkit.configuration(wkhtmltopdf=cfg.wkhtmltopdf_binary.as_posix())
    pdfkit.from_string(
        html,
        file_name,
        configuration=config,
        verbose=True,
        options={"--enable-local-file-access": True, "--disable-javascript": True},
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
    from data_questionnaire_agent.model.application_schema import Questionnaire
    from data_questionnaire_agent.model.openai_schema import ConditionalAdvice

    questionnaire: Questionnaire = create_questionnaire_2_questions()
    advices: ConditionalAdvice = create_simple_advice()
    logger.info(
        "PDF Path: %s",
        generate_pdf_from(
            ReportAdviceData(
                questionnaire=questionnaire,
                advices=advices,
                deep_research_outputs=create_deep_research_outputs(),
            ),
        ),
        "en",
    )
