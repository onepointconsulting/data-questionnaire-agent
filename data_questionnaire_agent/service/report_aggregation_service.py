from typing import List

from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.model.questionnaire_status import QuestionnaireStatus


def create_bullet_list(items: List[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def convert_to_str(questionnaire_statuses: List[QuestionnaireStatus]) -> List[str]:
    questionnaires = []
    questionnaire = []
    for qs in questionnaire_statuses:
        question, answer, final_report = qs.question, qs.answer, qs.final_report
        if not final_report:
            questionnaire.append(
                f"""
Q: {question}
A: {answer}
"""
            )
        else:
            conditional_advice: ConditionalAdvice = ConditionalAdvice.parse_raw(
                question
            )
            advices, what_you_should_avoid, positive_outcomes = (
                conditional_advice.advices,
                conditional_advice.what_you_should_avoid,
                conditional_advice.positive_outcomes,
            )
            advice_str = create_bullet_list(advices)
            what_you_should_avoid_str = create_bullet_list(what_you_should_avoid)
            positive_outcomes_str = create_bullet_list(positive_outcomes)
            questionnaire.append(
                f"""
# Recommendations

{advice_str}

# What to avoid

{what_you_should_avoid_str}

# Positive outcomes

{positive_outcomes_str}
"""
            )
            questionnaire.insert(0, "# Questionnaire")
            questionnaires.append("\n".join(questionnaire))
            questionnaire.clear()
    return questionnaires
