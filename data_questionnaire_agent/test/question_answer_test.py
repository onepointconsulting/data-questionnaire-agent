from data_questionnaire_agent.model.application_schema import QuestionAnswer


def test_validate_simple_question_answer():
    question_answer = QuestionAnswer(
        question="What is the meaning of life?", answer="42", clarification=""
    )
    assert question_answer.possible_answers is not None
    assert len(question_answer.possible_answers) == 0
