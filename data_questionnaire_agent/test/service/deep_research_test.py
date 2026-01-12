import pytest

from data_questionnaire_agent.model.application_schema import (
    QuestionAnswer,
    Questionnaire,
)
from data_questionnaire_agent.model.deep_research_input import DeepResearchAdviceInput
from data_questionnaire_agent.service.deep_research import (
    DeepResearchCallback,
    deep_research,
)


@pytest.mark.asyncio
async def test_generate_deep_research():
    import json

    deep_research_advice_input = DeepResearchAdviceInput(
        questionnaire=Questionnaire(
            questions=[
                QuestionAnswer(
                    id=1,
                    question="Which area of your data ecosystem are you most concerned about?",
                    answer="Cost and complexity - A robust data analytics infrastructure requires significant investment of resources.",
                    clarification=None,
                ),
                QuestionAnswer(
                    id=2,
                    question="What specific challenges do you face with the cost and complexity of your data analytics infrastructure?",
                    answer="The complexity of our existing systems makes it difficult to scale our data analytics solutions efficiently.",
                    clarification=None,
                ),
                QuestionAnswer(
                    id=3,
                    question="What specific factors contribute to the cost and complexity of your existing data analytics infrastructure?",
                    answer="Frequent updates required for compliance significantly raise operational costs.",
                    clarification=None,
                ),
                QuestionAnswer(
                    id=4,
                    question="What specific technologies or platforms are you currently using in your data analytics infrastructure that might be contributing to the cost and complexity?",
                    answer="We predominantly use open-source technologies to manage costs but it adds complexity.",
                    clarification=None,
                ),
                QuestionAnswer(
                    id=5,
                    question="What are your current data governance strategies and how do they impact the cost and complexity of your data analytics infrastructure?",
                    answer="We have a hybrid data governance strategy which aims to balance control and flexibility, but it sometimes complicates our infrastructure.",
                    clarification=None,
                ),
                QuestionAnswer(
                    id=6,
                    question="How is your organisation approaching the integration and potential upgrade of existing technologies or platforms to address the complexity and cost issues in your data analytics infrastructure?",
                    answer="We are evaluating various proprietary solutions that promise more streamlined integration, but we are hesitant due to the lock-in risks.",
                    clarification=None,
                ),
                QuestionAnswer(
                    id=7,
                    question="What are the potential risks and benefits you associate with moving from open-source technologies to proprietary solutions in your data analytics infrastructure?",
                    answer="Proprietary solutions could offer better support and stability compared to open-source technologies.",
                    clarification=None,
                ),
                QuestionAnswer(
                    id=8,
                    question="Given the concerns around vendor lock-in with proprietary solutions, how do you prioritise long-term flexibility over immediate benefits in your data strategy decisions?",
                    answer="We seek a middle ground by negotiating flexible contract terms with vendors, allowing for future modifications.",
                    clarification=None,
                ),
            ]
        ),
        conditional_advice="Consolidate open-source and proprietary solutions: To manage the balance between cost and complexity, consider integrating both open-source and proprietary solutions. Interoperability frameworks can assist in this, enabling you to choose the best fit for various tasks while managing vendor lock-in risks.",
    )
    output = await deep_research(
        deep_research_advice_input, callback=DeepResearchCallback()
    )

    with open("data/deep_research_output.md", "w", encoding="utf-8") as f:
        f.write(output.deep_research_output)
        for citation in output.citations:
            f.write(citation.to_markdown())

    # Serialize the output to a file
    with open("data/deep_research_output.json", "w", encoding="utf-8") as f:
        json.dump(output.model_dump(), f)
