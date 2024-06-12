from data_questionnaire_agent.model.application_schema import (
    QuestionAnswer,
    Questionnaire,
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


def create_questionnaire_2_questions_refugees() -> Questionnaire:
    question_answer = QuestionAnswer.question_answer_factory(
        "What challenges are you currently facing as a refugee?",
        "Document related issues",
    )
    question_answer_2 = QuestionAnswer.question_answer_factory(
        "What kind of problems do you have with your documents?",
        "I have lost my passport.",
    )
    return Questionnaire(questions=[question_answer, question_answer_2])


# Farsi version of create_questionnaire_2_questions
def create_questionnaire_2_questions__refugees_fa() -> Questionnaire:
    question_answer = QuestionAnswer.question_answer_factory(
        "چه چالش‌هایی در حال حاضر به عنوان یک پناهنده دارید؟",
        "مشکلات مربوط به اسناد",
    )
    question_answer_2 = QuestionAnswer.question_answer_factory(
        "با اسناد خود چه مشکلاتی دارید؟",
        "پاسپورت خود را گم کرده‌ام.",
    )
    return Questionnaire(questions=[question_answer, question_answer_2])
