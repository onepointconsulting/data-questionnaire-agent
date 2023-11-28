import re
import smtplib

from email.utils import parseaddr

from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.config import mail_config

from data_questionnaire_agent.config import cfg

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def validate_address(target_email: str) -> bool:
    logger.info("Checking if %s is an email", target_email)
    res = parseaddr(target_email)
    return len(res[1]) > 0 and EMAIL_REGEX.match(target_email)


def send_email(
    person_name: str, target_email: str, quizz_title: str, questionnaire_summary: str
):
    # Create the base text message.

    message = f"""From: {mail_config.mail_from_person} <{mail_config.mail_user}>
To: {person_name} <{target_email}>
MIME-Version: 1.0
Content-type: text/html
Subject: {quizz_title}

<img src="https://healthcheck.onepointltd.ai/public/images/Hero_Image_with_Logo_and_Titles.jpg" style="width: 100%;" />

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


def create_mail_body(questionnaire, advices, feedback_email):
    return f"""
    <p>A big thank you for completing the <b>{cfg.product_title}</b>.</p>
    <h2>Transcript</h2>
    {questionnaire.to_html()}
    <h2>Advice</h2>
    {advices.to_html() if advices is not None else ""}
    <p>We would love your feedback: <a href="mailto:{feedback_email}">{feedback_email}</a>.</p>
    <p>For more information, please visit us at <a href="https://www.onepointltd.com/data-wellness/">Onepoint Data Wellness</a>.</p>
    """


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
        cfg.product_title,
        f"""
{create_mail_body(questionnaire, None, "feedback@onepointltd.com")}
""",
    )
