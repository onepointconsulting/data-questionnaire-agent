import chainlit as cl

from data_questionnaire_agent.log_init import logger

from asyncer import asyncify
from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.service.html_generator import generate_pdf_from
from data_questionnaire_agent.ui.avatar_factory import AVATAR


async def generate_display_pdf(
    advices: ConditionalAdvice, questionnaire: Questionnaire
):
    pdf_path = await asyncify(generate_pdf_from)(questionnaire, advices)
    logger.info("PDF path: %s", pdf_path)
    elements = [
        cl.File(
            name=pdf_path.name,
            path=pdf_path.as_posix(),
            display="inline",
        ),
    ]
    await cl.Message(
        content="So you can download a copy, here’s a PDF with the recommendations:", 
        elements=elements,
        author=AVATAR["CHATBOT"]
    ).send()
