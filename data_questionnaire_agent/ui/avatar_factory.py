import chainlit as cl

AVATAR = {"CHATBOT": "Chatbot", "USER": "User"}


async def setup_avatar():
    await cl.Avatar(
        name=AVATAR["CHATBOT"],
        url="/public/images/natural-language-processing.png",
    ).send()
    await cl.Avatar(
        name=AVATAR["USER"],
        url="/public/images/User_icon_512.png",
    ).send()
