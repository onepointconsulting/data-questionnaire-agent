from pydantic import BaseModel, Field
from data_questionnaire_agent.model.application_schema import Questionnaire


class DeepResearchAdviceInput(BaseModel):
    questionnaire: Questionnaire = Field(..., description="The questionnaire")
    conditional_advice: str = Field(
        ...,
        description="The conditional advice which has been generated and being researched",
    )
