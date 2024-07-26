import re
import smtplib
from email.utils import parseaddr
from typing import Union

from data_questionnaire_agent.config import cfg, mail_config
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.report_enhancement_service import (
    replace_bold_markdown,
)
from data_questionnaire_agent.translation import t

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def validate_address(target_email: str) -> bool:
    logger.info("Checking if %s is an email", target_email)
    res = parseaddr(target_email)
    return len(res[1]) > 0 and EMAIL_REGEX.match(target_email)


def send_email(
    person_name: Union[str, None],
    target_email: str,
    quizz_title: str,
    questionnaire_summary: str,
):
    # Create the base text message.
    mail_from = mail_config.mail_from
    message = f"""From: {encode_name_and_mail(mail_config.mail_from_person, mail_from)}
To: {encode_name_and_mail(person_name, target_email)}
Return-Path: <{mail_from}>
MIME-Version: 1.0
Content-type: text/html
Subject: {quizz_title}

{questionnaire_summary}

""".encode(
        "utf-8"
    )
    # Send the message via local SMTP server.
    with smtplib.SMTP(mail_config.mail_server) as server:
        logger.info("Before starttls to %s", mail_config.mail_server)
        ehlo_res = server.ehlo()
        logger.info("ehlo_res %s", ehlo_res)
        tls_reply = server.starttls()
        logger.info("tls_reply %s", tls_reply)
        login_res = server.login(mail_config.mail_user, mail_config.mail_password)
        logger.info("login_res %s", login_res)
        logger.info("Message: %s", message)
        send_mail_res = server.sendmail(mail_config.mail_from, target_email, message)
        logger.info("send_mail_res %s", send_mail_res)
        server.quit()


def encode_name_and_mail(name: Union[str, None], email: str) -> str:
    if name is None:
        return email
    return f"{name} <{email}>"


def create_mail_body(
    questionnaire: Questionnaire,
    advices: ConditionalAdvice,
    feedback_email: str = mail_config.feedback_email,
    language: str = "en",
) -> str:
    mail_template = cfg.template_location / "mail-template.html"
    mail_template_text = mail_template.read_text(encoding="utf-8")
    confidence = advices.confidence
    content = f"""

    <img src="https://healthcheck.onepointltd.ai/banner/Hero_Image_with_Logo_and_Titles.jpg" style="width: 100%;" />

    <p>{t("A big thank you for completing a session with", name=cfg.product_title, locale=language)}</p>
    <h2>{t("Transcript", locale=language)}</h2>
    {replace_bold_markdown(questionnaire.to_html())}
    <h2>{t("Advice", locale=language)}</h2>
    {replace_bold_markdown(advices.to_html(language)) if advices is not None else ""}
    <h2>{t("Confidence Degree", locale=language)}</h2>
    {advices.confidence_html(language)}

    <h2 class="personalOffer">{t("A personal offer for you", locale=language)}</h2>
    <p>{t("offering_long", locale=language)}</p>

    <p>{t("We would love your feedback", locale=language)}: <a href="mailto:{feedback_email}">{feedback_email}</a>.</p>
    <p>{t("for_more_info", locale=language)}</p>
    """
    return mail_template_text.format(content, text=content)


if __name__ == "__main__":
    from data_questionnaire_agent.test.provider.questionnaire_provider import (
        create_questionnaire_2_questions,
    )

    recipient = "gil.fernandes@gmail.com"
    assert validate_address(recipient)
    questionnaire = create_questionnaire_2_questions()
    send_email(
        "Gil Fernandeds",
        recipient,
        mail_config.mail_subject,
        f"""
{create_mail_body(questionnaire, None, mail_config.feedback_email)}
""",
    )
