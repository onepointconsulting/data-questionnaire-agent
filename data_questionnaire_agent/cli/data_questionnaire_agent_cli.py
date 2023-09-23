from enum import Enum

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML

from data_questionnaire_agent.service.initial_question_service import (
    chain_factory_initial_question,
    prepare_initial_question,
    prompts,
)
from data_questionnaire_agent.service.similarity_search import (
    init_vector_search,
    similarity_search,
)
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.model.application_schema import (
    QuestionAnswer,
    Questionnaire,
)
from data_questionnaire_agent.model.openai_schema import ResponseQuestions, ResponseTags
from data_questionnaire_agent.service.clarifications_agent import (
    create_clarification_agent,
)
from data_questionnaire_agent.service.tagging_service import (
    prepare_sentiment_input,
    sentiment_chain_factory,
)


# Application state
class WorkflowState(Enum):
    INITIAL = 0
    PROCESS_RESPONSE = 1
    SECONDARY_QUESTION = 2
    ADVICE = 3


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
    logger.info(" Q: %s", question)


if __name__ == "__main__":
    logger.info(
        "Press [Meta+Enter] or [Esc] followed by [Enter] to accept input. Enter 'q' to quit"
    )
    initial_question = prompts["questionnaire"]["initial"]["question"]
    docsearch = init_vector_search()
    initial_question_chain = chain_factory_initial_question()
    has_questions_chain = sentiment_chain_factory()
    clarification_agent = create_clarification_agent()

    workflow_step = WorkflowState.INITIAL
    question_answer = QuestionAnswer.question_answer_factory(initial_question, "")
    questionnaire = Questionnaire(questions=[question_answer])

    response_questions: ResponseQuestions = None

    while True:
        match workflow_step:
            case WorkflowState.INITIAL:
                log_question(initial_question)
                answer = prompt(
                    "(data questionnaire)> ",
                    multiline=True,
                    prompt_continuation=prompt_continuation,
                )
                
                if answer.lower().strip() == "q":
                    break
                questionnaire.questions[-1].answer = answer
                search_res = similarity_search(docsearch, answer, how_many=2)
                logger.info("You said: %s", answer)
                logger.info("Search result: %s", search_res[:100])
                input = prepare_initial_question(
                    question=initial_question,
                    answer=answer,
                    questions_per_batch=cfg.questions_per_batch,
                    knowledge_base=search_res,
                )
                response_questions = initial_question_chain.run(input)
                logger.info("LLM questions: %s", response_questions.questions)
                workflow_step = WorkflowState.PROCESS_RESPONSE

            case WorkflowState.PROCESS_RESPONSE:
                answer = questionnaire.questions[-1].answer
                response_tags: ResponseTags = has_questions_chain.run(prepare_sentiment_input(answer))
                logger.info("Response tags: %s", response_tags)
                if len(response_tags.extracted_questions) > 0:
                    for clarification_question in response_tags.extracted_questions:
                        logger.info("Question: %s", clarification_question)
                        logger.info("Clarifications: %s", clarification_agent.run(clarification_question))
                workflow_step = WorkflowState.SECONDARY_QUESTION
                break
            case WorkflowState.SECONDARY_QUESTION:
                if response_questions:
                    pass
            case _:
                break
