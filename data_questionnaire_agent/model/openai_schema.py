from typing import Any, Dict, List, Optional, Union

import mistune
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field

from data_questionnaire_agent.model.confidence_schema import ConfidenceRating
from data_questionnaire_agent.model.deep_research import DeepResearchOutputs
from data_questionnaire_agent.translation import t
from data_questionnaire_agent.utils.url_functions import get_url_text


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


class ResponseQuestions(BaseModel):
    """Contains the questions used to gather information to be able to give a customer advice"""

    questions: List[str] = Field(
        ...,
        description="The list of questions given used to gather information to be able to give a customer advice.",
    )

    possible_answers: List[str] = Field(
        ...,
        description="The list of possible answers to the generated questions.",
    )

    def __str__(self) -> str:
        questions_str = "\n".join(self.questions)
        possible_answers_str = "\n".join(self.possible_answers)

        return f"""
Questions: {questions_str}

Possible Answwers: {possible_answers_str}
"""


class ResponseTags(BaseModel):
    """Contains information about the answer given by the user"""

    has_questions: bool = Field(
        ...,
        description="Whether the text with the answers contains embedded questions or not.",
    )
    sounds_confused: bool = Field(
        ...,
        description="Whether the text with the answers suggests that the user is confused.",
    )
    extracted_questions: Union[List[str], None] = Field(
        ...,
        description="If the text with the answers contains questions, these are the questions.",
    )
    questions_related_to_data_analytics: bool = Field(
        ...,
        description="True only if any questions are related to data analytics, data governance or data systems.",
    )


class ConditionalAdvice(PydanticBaseModel):
    """If there is enough information to give advice then advice will be available here."""

    has_advice: bool = Field(
        ...,
        description="Whether there is advice here or not",
    )
    advices: Optional[List[str]] = Field(
        ...,
        description="In case there is enough information to give advice, this list will contain advice to give to the user",
    )
    what_you_should_avoid: Optional[List[str]] = Field(
        default=[],
        description="A list of advice about what you should not do and avoid.",
    )
    positive_outcomes: Optional[List[str]] = Field(
        default=[],
        description="A list of potential positive outcomes in case the user follows the advice.",
    )
    confidence: Optional[ConfidenceRating] = Field(
        default=None, description="The confidence rating at the time of the report."
    )
    advices_with_deep_research: list[tuple[str, DeepResearchOutputs]] = Field(
        default=[],
        description="A list of advices with the corresponding deep research outputs.",
    )

    @classmethod
    def model_json_schema(
        cls, by_alias: bool = True, ref_template: str = "#/$defs/{model}", **kwargs
    ) -> Dict[str, Any]:
        """Override to exclude advices_with_deep_research from JSON schema."""
        schema = super().model_json_schema(
            by_alias=by_alias, ref_template=ref_template, **kwargs
        )
        # Remove the field from properties if it exists
        if (
            "properties" in schema
            and "advices_with_deep_research" in schema["properties"]
        ):
            del schema["properties"]["advices_with_deep_research"]
            # Also remove from required if present
            if (
                "required" in schema
                and "advices_with_deep_research" in schema["required"]
            ):
                schema["required"].remove("advices_with_deep_research")
        return schema

    def to_html(self, language: str = "en") -> str:
        return f"""{self.to_advice_html()}

<h2>{t("What to avoid", locale=language)}</h2>
{self.to_avoid_html()}

<h2>{t("Potential positive outcomes", locale=language)}</h2>
{self.positive_outcomes_html()}
"""

    def to_advice_html(self) -> str:
        return self.html_convert(self.advices)

    def to_avoid_html(self) -> str:
        return self.html_convert(self.what_you_should_avoid)

    def positive_outcomes_html(self) -> str:
        return self.html_convert(self.positive_outcomes)

    def html_convert(self, list: List[str]) -> str:
        html = "<div>"
        for advice in list:
            html += f'<li class="onepoint-blue onepoint-advice">{advice}</li>'
            for deep_research_output in self.advices_with_deep_research:
                if deep_research_output[0] == advice:
                    html += f"""<div class="onepoint-deep-research" style="background-color: #ececec; padding: 2px 8px 20px 8px;">
<h4>Deep Research</h4>
{mistune.markdown(deep_research_output[1].deep_research_output)}
<h4>Citations</h4>
<ul>
"""
                    citations_dict = {}
                    for citation in deep_research_output[1].citations:
                        if citation.title not in citations_dict:
                            citations_dict[citation.title] = []
                        citations_dict[citation.title].append(citation)
                    for title, citations in citations_dict.items():
                        from collections import Counter

                        citations_counter = Counter(citations)
                        citations_html_snippets = []
                        for citation in citations:
                            citation_text = get_url_text(citation.url)
                            citations_counter[citation_text] += 1
                            if citations_counter[citation_text] == 1:
                                citations_html_snippets.append(
                                    f"""<li class="onepoint-deep-research-citation-item">
    <a href="{citation.url}" target="_blank" rel="noopener noreferrer">{citation_text if len(citation_text) > 1 else citation.url}</a>
    </li>
    """
                                )
                        html += f"""<h4>{title}</h4>
<ul>
{"\n".join(sorted(citations_html_snippets))}
</ul>
"""
                    html += "</ul>"
                    html += "</div>"
        html += "</div>"
        return html

    def confidence_html(self, language: str = "en") -> str:
        return self.confidence.to_html(language) if self.confidence is not None else ""

    def to_markdown(self, language: str = "en") -> str:
        def convert_to_text(text_list: List[str], title: str):
            md = f"# {title}\n\n"
            if text_list is not None:
                for text in text_list:
                    md += f"- {text}\n\n"
            return md

        markdown = convert_to_text(
            self.advices, t("What you should do", locale=language)
        )
        markdown += convert_to_text(
            self.what_you_should_avoid, t("What you should avoid", locale=language)
        )
        markdown += convert_to_text(
            self.positive_outcomes,
            t(
                "Positive outcomes (if you follow the actions to review)",
                locale=language,
            ),
        )

        if self.confidence is not None and isinstance(
            self.confidence, ConfidenceRating
        ):
            markdown += self.confidence.to_markdown(locale=language)

        return markdown

    def __str__(self) -> str:
        def join_items(items):
            return "\n\n".join(items) if items is not None else ""

        return f"""{join_items(self.advices)}


{join_items(self.what_you_should_avoid)}


{join_items(self.positive_outcomes)}
"""
