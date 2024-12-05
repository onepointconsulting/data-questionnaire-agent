from email.mime.multipart import MIMEMultipart

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.mail_data import Email
from data_questionnaire_agent.service.mail_sender import create_attachment_email


def create_dummy_email() -> Email:
    return Email(
        recipient="john.smith@gmail.com",
        subject="Test",
        html_body="<p>Testing</p>",
        files=[cfg.project_root / "README.md"],
    )


def create_dummy_email_2() -> Email:
    return Email(
        recipient="gil.fernandes@gmail.com",
        subject="Test",
        html_body="<p>Testing</p>",
        files=[cfg.project_root / "README.md"],
    )


def create_dummy_multipart() -> MIMEMultipart:
    return create_attachment_email(create_dummy_email())
