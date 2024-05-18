from typing import List

from dataclasses import dataclass, field
from typing import Union, Optional

from data_questionnaire_agent.model.openai_schema import ResponseQuestions


@dataclass
class QuestionAnswer:
    question: str
    answer: Union[str, dict]
    clarification: Optional[str]
    possible_answers: List[str] = field(default_factory=list)

    def answer_str(self):
        if not self.answer:
            return ""
        elif isinstance(self.answer, str):
            return self.answer
        else:
            return self.answer["content"]

    def __repr__(self) -> str:
        return f"""{self.question}
{self.answer_str()}"""

    @staticmethod
    def question_answer_factory(question: str, answer: dict):
        return QuestionAnswer(question=question, answer=answer, clarification="")

    @staticmethod
    def question_factory(question: str):
        return QuestionAnswer(question=question, answer="", clarification="")


@dataclass
class Questionnaire:
    questions: List[QuestionAnswer]

    def __repr__(self) -> str:
        return "\n\n".join([str(qa) for qa in self.questions])

    def __len__(self):
        return len(self.questions)

    def answers_str(self) -> str:
        return "\n\n".join(
            [
                qa.answer["content"] if isinstance(qa.answer, dict) else qa.answer
                for qa in self.questions
            ]
        )

    def to_html(self) -> str:
        html = """<table>       
"""
        for qa in self.questions:
            answer = qa.answer
            html += f"""
<tr>
    <td class="onepoint-blue">
        <br />
        Q: {qa.question}
    </td>
</tr>
<tr>
    <td class="onepoint-answer">A: {answer}</td>
</tr>
"""
        html += "</table>"
        return html


def convert_to_question_answers(
    response_questions: ResponseQuestions,
) -> List[QuestionAnswer]:
    question_answers = []
    for i, q in enumerate(response_questions.questions):
        question_answer = QuestionAnswer.question_factory(q)
        question_answers.append(question_answer)
        if i == 0:
            question_answer.possible_answers = response_questions.possible_answers
    return question_answers
    #return [QuestionAnswer.question_factory(q) for q in response_questions.questions]
