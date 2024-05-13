from typing import Union
import re
import smtplib

from email.utils import parseaddr

from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.config import mail_config
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.config import mail_config

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.service.report_enhancement_service import (
    replace_bold_markdown,
)

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
) -> str:
    mail_template = cfg.template_location / "mail-template.html"
    mail_template_text = mail_template.read_text(encoding="utf-8")
    content = f"""

    <img src="https://healthcheck.onepointltd.ai/banner/Hero_Image_with_Logo_and_Titles.jpg" style="width: 100%;" />

    <p>A big thank you for completing a session with the <b>{cfg.product_title}</b>.</p>
    <h2>Transcript</h2>
    {replace_bold_markdown(questionnaire.to_html())}
    <h2>Advice</h2>
    {replace_bold_markdown(advices.to_html()) if advices is not None else ""}

    <h2 class="personalOffer">A personal offer for you</h2>
    <p>We are offering a free results interpretation call to talk through the Companion's recommendations and suggested courses of action with a real human expert. 
        If you are open to that, please email us at <a href="mailto:datawellness@onepointltd.com">datawellness@onepointltd.com</a> from your business email address with your request to schedule a call.</p>

    <p>We would love your feedback: <a href="mailto:{feedback_email}">{feedback_email}</a>.</p>
    <p>For more information, please visit us at <a href="https://www.onepointltd.com/data-wellness/">Onepoint Data Wellness</a>.</p>
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
