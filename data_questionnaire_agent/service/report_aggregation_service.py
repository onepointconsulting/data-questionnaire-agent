from typing import List

from data_questionnaire_agent.model.openai_schema import ConditionalAdvice
from data_questionnaire_agent.model.questionnaire_status import QuestionnaireStatus


def create_bullet_list(items: List[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def convert_to_str(questionnaire_statuses: List[QuestionnaireStatus]) -> List[str]:
    questionnaires = []
    questionnaire = []
    for i, qs in enumerate(questionnaire_statuses):
        question, answer, final_report = qs.question, qs.answer, qs.final_report
        if not final_report:
            if (i+1 != len(questionnaire_statuses) and qs.session_id != questionnaire_statuses[i+1].session_id):
                # There is a missing final report in this case
                # Flush the report to the output list
                questionnaire.insert(0, "# Questionnaire")
                questionnaire.append(f"""
Q: {question}
A: {answer}
""")
                questionnaires.append("\n".join(questionnaire))
                questionnaire.clear()
                continue
            questionnaire.append(
                f"""
Q: {question}
A: {answer}
"""
            )
            if i+1 == len(questionnaire_statuses):
                # Last questions of last questionnaire
                questionnaire.insert(0, "# Questionnaire")
                questionnaires.append("\n".join(questionnaire))
                questionnaire.clear()
        elif final_report:
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
