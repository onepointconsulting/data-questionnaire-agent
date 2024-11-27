import asyncio
from enum import Enum

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML

from data_questionnaire_agent.config import cfg
from data_questionnaire_agent.log_init import logger
from data_questionnaire_agent.model.application_schema import (
    QuestionAnswer,
    Questionnaire,
)
from data_questionnaire_agent.model.openai_schema import (
    ConditionalAdvice,
    ResponseQuestions,
    ResponseTags,
)
from data_questionnaire_agent.model.session_configuration import (
    ChatType,
    SessionProperties,
)
from data_questionnaire_agent.service.advice_service import (
    chain_factory_advice,
    prepare_conditional_advice,
)
from data_questionnaire_agent.service.clarifications_agent import (
    create_clarification_agent,
)
from data_questionnaire_agent.service.initial_question_service import (
    chain_factory_initial_question,
    prepare_initial_question,
    prompts,
)
from data_questionnaire_agent.service.knowledge_base_service import fetch_context
from data_questionnaire_agent.service.question_generation_service import (
    chain_factory_secondary_question,
    prepare_secondary_question,
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


def ask_question(question) -> str:
    logger.info(" Q: %s", question)
    return prompt(
        "(data questionnaire)> ",
        multiline=True,
        prompt_continuation=prompt_continuation,
    )


def process_clarifications(has_questions_chain, clarification_agent, content):
    response_tags: ResponseTags = has_questions_chain.run(
        prepare_sentiment_input(content)
    )
    logger.info("Response tags: %s", response_tags)
    if len(response_tags.extracted_questions) > 0:
        for clarification_question in response_tags.extracted_questions:
            logger.info("Question: %s", clarification_question)
            logger.info(
                "Clarifications: %s",
                clarification_agent.run(clarification_question),
            )


if __name__ == "__main__":
    logger.info(
        "Press [Meta+Enter] or [Esc] followed by [Enter] to accept input. Enter 'q' to quit"
    )
    initial_question = prompts["questionnaire"]["initial"]["question"]
    initial_question_chain = chain_factory_initial_question()
    has_questions_chain = sentiment_chain_factory()
    clarification_agent = create_clarification_agent()
    session_properties = SessionProperties(
        session_steps=6, session_language="en", chat_type=ChatType.DIVERGING
    )
    secondary_question_chain = chain_factory_secondary_question(session_properties)
    advice_chain = chain_factory_advice()

    workflow_step = WorkflowState.INITIAL
    question_answer = QuestionAnswer.question_answer_factory(initial_question, "")
    questionnaire = Questionnaire(questions=[question_answer])

    response_questions: ResponseQuestions = None

    while True:
        match workflow_step:
            case WorkflowState.INITIAL:
                answer = ask_question(initial_question)
                if answer.lower().strip() == "q":
                    break
                questionnaire.questions[-1].answer = {"content": answer}
                knowledge_base = asyncio.run(fetch_context(answer))
                logger.info("You said: %s", answer)
                logger.info("Search result: %s", knowledge_base[:100])
                input = prepare_initial_question(
                    question=initial_question,
                    answer=answer,
                    questions_per_batch=cfg.questions_per_batch,
                    knowledge_base=knowledge_base,
                )
                response_questions = initial_question_chain.run(input)
                logger.info("LLM questions: %s", response_questions.questions)

                workflow_step = WorkflowState.PROCESS_RESPONSE

            case WorkflowState.PROCESS_RESPONSE:
                answer = questionnaire.questions[-1].answer
                content = answer["content"]
                process_clarifications(
                    has_questions_chain, clarification_agent, content
                )

                workflow_step = WorkflowState.SECONDARY_QUESTION

            case WorkflowState.SECONDARY_QUESTION:
                quit = False
                if response_questions:
                    answers = []
                    for question in response_questions.questions:
                        answer = ask_question(question)
                        if answer.lower().strip() == "q":
                            quit = True
                            break
                        questionnaire.questions.append(
                            QuestionAnswer.question_answer_factory(
                                question, {"content": answer}
                            )
                        )
                        answers.append(answer)
                    process_clarifications(
                        has_questions_chain, clarification_agent, "\n".join(answers)
                    )
                if quit:
                    break
                workflow_step = WorkflowState.ADVICE

            case WorkflowState.ADVICE:
                questionnaire_str = str(questionnaire)
                knowledge_base = asyncio.run(fetch_context(questionnaire_str))
                logger.info("Search result: %s", knowledge_base[:100])
                advice_input = prepare_conditional_advice(
                    knowledge_base=knowledge_base, questions_answers=questionnaire_str
                )
                conditional_advice: ConditionalAdvice = advice_chain.run(advice_input)
                if (
                    conditional_advice.has_advice
                    and len(questionnaire) >= cfg.minimum_questionnaire_size
                ):
                    # We have advice
                    for i, advice in enumerate(conditional_advice.advices):
                        logger.info("%d. %s", i + 1, advice)
                    break
                # Generate more questions
                secondary_question_input = prepare_secondary_question(
                    questionnaire, knowledge_base
                )
                response_questions: ResponseQuestions = secondary_question_chain.run(
                    secondary_question_input
                )
                workflow_step = WorkflowState.SECONDARY_QUESTION

            case _:
                break
