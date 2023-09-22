from typing import List

from dataclasses import dataclass
from typing import Union, Optional


@dataclass
class QuestionAnswer:
    question: str
    answer: Union[str, dict]
    clarification: Optional[str]

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


@dataclass
class Questionnaire:
    questions: List[QuestionAnswer]

    def __repr__(self) -> str:
        return "\n\n".join([str(qa) for qa in self.questions])

    def answers_str(self) -> str:
        return "\n\n".join(
            [
                qa.answer["content"] if isinstance(qa.answer, dict) else qa.answer
                for qa in self.questions
            ]
        )
