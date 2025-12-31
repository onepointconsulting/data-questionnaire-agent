from typing import Union

from pydantic.v1 import BaseModel, Field


class QuestionSuggestion(BaseModel):
    id: Union[int, None] = Field(default=None, description="The unique identifier")
    img_src: str = Field(..., description="The image associated to the suggestion")
    img_alt: str = Field(..., description="The alternative description of the image")
    title: str = Field(..., description="The suggestion title")
    main_text: str = Field(..., description="The suggestion text")
    svg_image: str = Field(..., description="The SVG image")


class QuestionAndSuggestions(BaseModel):
    id: Union[int, None] = Field(default=None, description="The unique identifier")
    question: str = Field(default=None, description="The actual question")
    suggestions: list[QuestionSuggestion] = Field(
        ..., description="The list of suggested question suggestions"
    )


class QuestionInfo(BaseModel):
    question_and_suggestions: list[QuestionAndSuggestions] = Field(
        ..., description="Theh list of question and suggestions"
    )


class PossibleAnswer(BaseModel):
    title: str = Field(..., description="The title of the possible answer")
    main_text: str = Field(..., description="The text of the possible answer")


class PossibleAnswers(BaseModel):
    possible_answers: list[PossibleAnswer] = Field(
        ..., description="The list of possible answers to the generated questions"
    )
