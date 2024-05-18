import itertools
import datetime

import chainlit as cl
from chainlit import context

from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.ui.chat_settings_factory import create_chat_settings
from data_questionnaire_agent.ui.model.session_number_container import (
    SessionNumberContainer,
)


@cl.on_chat_start
async def init():
    logger.info("Init")
    cl.user_session.set("session_counter", SessionNumberContainer())
    settings = await create_chat_settings()
    await run_agent(settings, False)


@cl.on_settings_update
async def on_settings_update(settings: cl.ChatSettings):
    await run_agent(settings, True)


async def run_agent(settings: cl.ChatSettings, from_settings: bool):
    session_counter = cl.user_session.get("session_counter")
    my_counter = session_counter.increment_and_get()
    local_context = context.get_context()
    logger.info("start id: %s", local_context.session.id)
    await cl.Message(content=f"Start {local_context.session.id}").send()
    response = None
    while response == None:
        latest_counter = cl.user_session.get("session_counter")
        response = await cl.AskUserMessage(
            content=f"Please reply something {from_settings} {my_counter} {latest_counter} ...",
            timeout=cfg.ui_timeout,
        ).send()


@cl.on_chat_end
async def end():
    local_context = context.get_context()
    logger.info("end id: %s", local_context.session.id)
    cl.user_session.set("session_started", False)