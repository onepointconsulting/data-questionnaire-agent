from pathlib import Path

from pydantic import BaseModel, Field


class MailData(BaseModel):
    person_name: str = Field(..., description="The name of the person")
    email: str = Field(..., description="The actual name of the person")


class Email(BaseModel):
    recipient: str = Field(..., description="The recipient email")
    subject: str = Field(..., description="The email subject")
    html_body: str = Field(..., description="The html email body")
    files: list[Path] = Field(..., description="The attachment files")
