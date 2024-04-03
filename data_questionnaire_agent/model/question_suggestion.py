from typing import Union

from pydantic import BaseModel, Field


class QuestionSuggestion(BaseModel):
    id: Union[int, None] = Field(default=None, description="The unique identifier")
    img_src: str = Field(..., description="The image associated to the suggestion")
    img_alt: str = Field(..., description="The alternative description of the image")
    title: str = Field(..., description="The suggestion title")
    main_text: str = Field(..., description="The suggestion text")
