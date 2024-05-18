from data_questionnaire_agent.model.application_schema import QuestionAnswer


def create_question_answer_with_possible_answers() -> QuestionAnswer:
    return QuestionAnswer(
        question="What is the meaning of life?",
        answer="The meaning of life is 42",
        clarification=[],
        possible_answers=["The meaning of life is 43", "The meaning of life is 44"],
    )
