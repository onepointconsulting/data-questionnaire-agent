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


def create_questionnaire_3_questions() -> Questionnaire:
    question_answer = QuestionAnswer.question_answer_factory(
        "Which area of your data ecosystem are you most concerned about?",
        "Poor data quality - Low-quality data can lead to incorrect insights and poor decision-making.",
    )
    question_answer_2 = QuestionAnswer.question_answer_factory(
        "What specific challenges are you facing with data quality in your organisation?",
        """- Our data is often incomplete, making it difficult to perform comprehensive analyses. 
        - We struggle with data consistency across different sources and systems.""",
    )
    question_answer_3 = QuestionAnswer.question_answer_factory(
        "What methods or tools are you currently using to address data completeness and consistency issues in your organisation?",
        """- We have not yet implemented any specific methods or tools to address these issues.""",
    )
    return Questionnaire(
        questions=[question_answer, question_answer_2, question_answer_3]
    )


def create_questionnaire_4_questions() -> Questionnaire:
    previous = create_questionnaire_3_questions()
    question_answer_4 = QuestionAnswer.question_answer_factory(
        "What are the primary sources of data in your organisation, and how are they currently integrated?",
        """- Our data comes from various IoT devices and sensors, and we use a centralised platform for integration.""",
    )
    return Questionnaire(questions=[*previous.questions, question_answer_4])


def create_questionnaire_4_questions_german() -> Questionnaire:
    question_answer = QuestionAnswer.question_answer_factory(
        "Welcher Bereich Ihres Datenökosystems bereitet Ihnen die meisten Sorgen?",
        "Schlechte Datenqualität - Daten von niedriger Qualität können zu falschen Erkenntnissen und schlechten Entscheidungen führen.",
    )
    question_answer_2 = QuestionAnswer.question_answer_factory(
        "Welche spezifischen Herausforderungen haben Sie mit der Datenqualität in Ihrer Organisation?",
        """- Unsere Daten sind oft unvollständig, was es schwierig macht, umfassende Analysen durchzuführen.
        - Wir haben Schwierigkeiten mit der Datenkonsistenz über verschiedene Quellen und Systeme hinweg.""",
    )
    question_answer_3 = QuestionAnswer.question_answer_factory(
        "Welche Methoden oder Werkzeuge verwenden Sie derzeit, um Probleme mit Datenvollständigkeit und -konsistenz in Ihrer Organisation zu lösen?",
        """- Wir haben noch keine spezifischen Methoden oder Werkzeuge implementiert, um diese Probleme zu lösen.""",
    )
    question_answer_4 = QuestionAnswer.question_answer_factory(
        "Was sind die Hauptquellen für Daten in Ihrer Organisation und wie werden sie derzeit integriert?",
        """- Unsere Daten stammen von verschiedenen IoT-Geräten und Sensoren, und wir verwenden eine zentrale Plattform zur Integration.""",
    )
    return Questionnaire(
        questions=[
            question_answer,
            question_answer_2,
            question_answer_3,
            question_answer_4,
        ]
    )


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


def create_questionnaire_7_questions() -> Questionnaire:
    qa_list = [
        {
            "q": "Which area of your data ecosystem are you most concerned about?",
            "a": "Resistance to change - Employees need to adapt to new ways of operating to make data-driven transformation work.",
        },
        {
            "q": "What specific challenges are your employees facing when adapting to new data-driven processes?",
            "a": "There is a lack of motivation to learn and adapt to new data processes.",
        },
        {
            "q": "What strategies have you tried so far to increase employee motivation for learning and adapting to new data processes?",
            "a": "We've tried peer mentoring programmes to encourage knowledge sharing, but participation is inconsistent.",
        },
        {
            "q": "What specific factors do you think are contributing to the lack of motivation among employees to engage with new data processes?",
            "a": "There is a general resistance to change within the organisation's culture.",
        },
        {
            "q": "What measures have you considered to address the cultural resistance to change within your organisation, particularly in relation to data-driven processes?",
            "a": "We have ran some gamification on data population, and highlighted how the benefits tie back to organisational goals.",
        },
        {
            "q": "What kind of support or resources do you think would help your employees overcome their resistance to change and engage more with new data-driven processes?",
            "a": "Introducing incentives for employees who actively participate in learning new data processes could be beneficial.",
        },
        {
            "q": "What are the main reasons your employees resist adapting to new data-driven processes despite the potential benefits?",
            "a": "There is a lack of clear communication about the benefits and goals of data-driven transformation.",
        },
    ]
    questions = [
        QuestionAnswer.question_answer_factory(qa["q"], qa["a"]) for qa in qa_list
    ]
    return Questionnaire(questions=questions)
