import chainlit as cl

from asyncer import asyncify

from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.ui.avatar_factory import AVATAR

from data_questionnaire_agent.service.mail_sender import (
    send_email,
    validate_address,
)

from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.config import cfg


async def process_send_email(questionnaire: Questionnaire, advices: ConditionalAdvice):
    response = await cl.AskUserMessage(
        content="Would you like to receive an email with the recommendations? If so, please enter your email address in the chat.",
        timeout=cfg.ui_timeout,
        author=AVATAR["CHATBOT"],
    ).send()
    has_replied = False
    if response and "content" in response:
        has_replied = True
        response_content = response["content"]
        if validate_address(response_content):
            logger.info("Sending email to %s", response_content)
            await asyncify(send_email)(
                "Dear customer",
                response_content,
                "Onepoint Data Integration Questionnaire",
                f"""
    <p>Big thank you for completing the <b>Onepoint's Data Integration Assessment Quiz</b>.</p>

    <h2>Questionnaire</h2>
    {questionnaire.to_html()}

    <h2>Advice</h2>
    {advices.to_html()}

    For more information, please visit our <a href="https://onepointltd.com">webpage</a>.

    """,
            )
            await cl.Message(
                content=f"Thank you for submitting the query. We really appreciate that you have taken time to do this.",
                author=AVATAR["CHATBOT"],
            ).send()
        else:
            logger.warn("%s is not a valid email", response_content)
            await cl.ErrorMessage(
                content=f"Sorry, '{response_content}' does not seem to be an email address",
                author=AVATAR["CHATBOT"],
            ).send()

    extra_message = "" if has_replied else "We did not hear from you... "
    await cl.Message(
        content=f"{extra_message}The session is complete. Please press the 'New Chat' button to restart.",
        author=AVATAR["CHATBOT"],
    ).send()
