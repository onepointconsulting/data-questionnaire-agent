from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from data_questionnaire_agent.log_init import logger

from data_questionnaire_agent.service.initial_question_service import (
    chain_factory_initial_question,
    prepare_initial_question,
    prompts,
)


def prompt_continuation(width, line_number, wrap_count):
    """
    The continuation: display line numbers and '->' before soft wraps.

    Notice that we can return any kind of formatted text from here.

    The prompt continuation doesn't have to be the same width as the prompt
    which is displayed before the first line, but in this example we choose to
    align them. The `width` input that we receive here represents the width of
    the prompt.
    """
    if wrap_count > 0:
        return " " * (width - 3) + "-> "
    else:
        text = ("- %i - " % (line_number + 1)).rjust(width)
        return HTML("<strong>%s</strong>") % text


def log_question(question):
    logger.info(" Q: %s", initial_question)


if __name__ == "__main__":
    logger.info(
        "Press [Meta+Enter] or [Esc] followed by [Enter] to accept input. Enter 'q' to quit"
    )
    initial_question = prompts["questionnaire"]["initial"]["question"]
    log_question(initial_question)
    while True:
        answer = prompt(
            "(data questionnaire)> ",
            multiline=True,
            prompt_continuation=prompt_continuation,
        )
        if answer.lower().strip() == "q":
            break
        logger.info("You said: %s", answer)
