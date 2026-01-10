from pydantic import BaseModel, Field

from data_questionnaire_agent.model.application_schema import Questionnaire
from data_questionnaire_agent.model.deep_research import DeepResearchOutputs
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice


class ReportAdviceData(BaseModel):
    questionnaire: Questionnaire | None = Field(..., description="The questionnaire")
    advices: ConditionalAdvice | None = Field(..., description="The advices")
    deep_research_outputs: DeepResearchOutputs | None = Field(..., description="The deep research outputs")