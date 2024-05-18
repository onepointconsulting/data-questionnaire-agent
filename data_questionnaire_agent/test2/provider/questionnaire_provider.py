from data_questionnaire_agent.model.application_schema import (
    Questionnaire,
    QuestionAnswer,
)


def create_questionnaire_initial_question(answer: str) -> Questionnaire:
    question_answer = QuestionAnswer.question_answer_factory(
        "Which area of your data ecosystem are you most concerned about?",
        answer,
    )
    return Questionnaire(questions=[question_answer])


def create_questionnaire_2_questions() -> Questionnaire:
    question_answer = QuestionAnswer.question_answer_factory(
        "Which area of your data ecosystem are you most concerned about?",
        "Data Quality and Duplication",
    )
    question_answer_2 = QuestionAnswer.question_answer_factory(
        "What measures are currently in place to ensure the quality of your data?",
        "We have processes which deduplicate the data in our data warehouse.",
    )
    return Questionnaire(questions=[question_answer, question_answer_2])
