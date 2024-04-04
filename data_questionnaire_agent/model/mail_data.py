from pydantic import BaseModel, Field


class MailData(BaseModel):
    person_name: str = Field(..., description="The name of the person")
    email: str = Field(..., description="The actual name of the person")


if __name__ == "__main__":
    mail_data = MailData(person_name="John Doe", email="john@gmail.com")
    json_data = mail_data.json()
    print(json_data)
    copy = MailData.parse_raw(json_data)
    print(copy)
    assert mail_data == copy
