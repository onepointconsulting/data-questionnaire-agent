import re
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr
from typing import Union

from data_questionnaire_agent.config import cfg, mail_config
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.mail_data import Email
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.model.report_advice_schema import ReportAdviceData
from data_questionnaire_agent.service.advice_service import (
    combine_advices_and_deep_research_outputs,
)
from data_questionnaire_agent.service.report_enhancement_service import (
    replace_bold_markdown,
)
from data_questionnaire_agent.translation import t

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def validate_address(target_email: str) -> bool:
    logger.info("Checking if %s is an email", target_email)
    res = parseaddr(target_email)
    return len(res[1]) > 0 and EMAIL_REGEX.match(target_email)


def init_mail(server: smtplib.SMTP):
    logger.info("Before starttls to %s", mail_config.mail_server)
    ehlo_res = server.ehlo()
    logger.info("ehlo_res %s", ehlo_res)
    tls_reply = server.starttls()
    logger.info("tls_reply %s", tls_reply)
    login_res = server.login(mail_config.mail_user, mail_config.mail_password)
    logger.info("login_res %s", login_res)


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
        init_mail(server)
        logger.info("Message: %s", message)
        send_mail_res = server.sendmail(mail_config.mail_from, target_email, message)
        logger.info("send_mail_res %s", send_mail_res)
        server.quit()


def encode_name_and_mail(name: Union[str, None], email: str) -> str:
    if name is None:
        return email
    return f"{name} <{email}>"


def create_mail_body(
    report_advice_data: ReportAdviceData,
    feedback_email: str = mail_config.feedback_email,
    language: str = "en",
) -> str:
    questionnaire = report_advice_data.questionnaire
    advices = report_advice_data.advices
    deep_research_outputs = report_advice_data.deep_research_outputs
    combine_advices_and_deep_research_outputs(advices, deep_research_outputs)
    mail_template = cfg.template_location / "mail-template.html"
    mail_template_text = mail_template.read_text(encoding="utf-8")
    content = f"""

    <img src="{t("banner_link", locale=language)}" style="width: 100%;" />

    <p>{t("A big thank you for completing a session with", name=cfg.product_title, locale=language)}</p>
    <h2>{t("Transcript", locale=language)}</h2>
    {replace_bold_markdown(questionnaire.to_html())}
    <h2>{t("Advice", locale=language)}</h2>
    {replace_bold_markdown(advices.to_html(language)) if advices is not None else ""}
    <h2>{t("Confidence Degree", locale=language)}</h2>
    {advices.confidence_html(language) if advices is not None else ""}

    <h2 class="personalOffer">{t("A personal offer for you", locale=language)}</h2>
    <p>{t("offering_long", locale=language)}</p>

    <p>{t("We would love your feedback", locale=language)}: <a href="mailto:{feedback_email}">{feedback_email}</a>.</p>
    <p>{t("for_more_info", locale=language)}</p>
    """
    return mail_template_text.format(content, text=content)


def send_mail_with_attachment(email: Email):
    logger.info("Sending email to %s", email.recipient)
    mime_multipart = create_attachment_email(email)
    with smtplib.SMTP(mail_config.mail_server) as server:
        init_mail(server)
        server.send_message(mime_multipart)
        logger.info("Email sent successfully!")


def create_attachment_email(email: Email) -> MIMEMultipart:
    recipient, subject, html_body, files = (
        email.recipient,
        email.subject,
        email.html_body,
        email.files,
    )
    msg = MIMEMultipart()
    msg["From"] = mail_config.mail_from
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    for file in files:
        if file.exists():
            with open(file, "rb") as attachment:
                mime_base = MIMEBase("application", "octet-stream")
                mime_base.set_payload(attachment.read())
                encoders.encode_base64(mime_base)
                mime_base.add_header(
                    "Content-Disposition", f"attachment; filename={file.name}"
                )
                msg.attach(mime_base)
    return msg


if __name__ == "__main__":
    from data_questionnaire_agent.test.provider.multipart_provider import (
        create_dummy_email_2,
    )
    from data_questionnaire_agent.test.provider.questionnaire_provider import (
        create_questionnaire_2_questions,
    )

    def send_test_email():
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

    def send_attachment_email():
        email = create_dummy_email_2()
        send_mail_with_attachment(email)

    send_attachment_email()
