import chainlit as cl
from chainlit.input_widget import Slider, TextInput

from data_questionnaire_agent.toml_support import prompts

MINIMUM_NUMBER_OF_QUESTIONS = "Minimum number of questions"
QUESTION_PER_BATCH = "Questions per batch"
INITIAL_QUESTION = "Initial question"


async def create_chat_settings() -> cl.ChatSettings:
    questions_per_batch = prompts["general_settings"]["questions_per_batch"]
    minimum_number_of_questions = prompts["general_settings"][
        "minimum_number_of_questions"
    ]
    initial_question = prompts["questionnaire"]["initial"]["question"]
    settings = await cl.ChatSettings(
        [
            TextInput(
                id=INITIAL_QUESTION, label=INITIAL_QUESTION, initial=initial_question
            ),
            Slider(
                id=MINIMUM_NUMBER_OF_QUESTIONS,
                label="Minimum number of questions",
                initial=minimum_number_of_questions,
                min=0,
                max=5,
                step=1,
            ),
            Slider(
                id=QUESTION_PER_BATCH,
                label="Number of question per batch",
                initial=questions_per_batch,
                min=0,
                max=5,
                step=1,
            ),
        ]
    ).send()
    return settings
