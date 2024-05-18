from typing import List


def questionnaire_str_adapter(questions: List[str], answers: List[str]) -> str:
    return "\n\n".join([f"{q}\n{a}" for q, a in zip(questions, answers)])


def provide_data_silo_questionnaire() -> str:
    questions = [
        "Which area of your data ecosystem are you most concerned about?",
        "What steps have you taken so far to address the issue of data silos in your organization?",
        "How are you currently sharing data between different departments, lines of business and subsidiaries in your organization?",
        "Considering the challenges you've faced with data silos and the partial success of your service-driven architecture, have you considered implementing a Data Mesh architecture to decentralize data ownership and accountability, thereby reducing data silos?",
        "You mentioned that not all departments have bought into the idea of using REST services for data sharing, particularly the billing department. What are the specific concerns or challenges they have raised, and how might these be addressed to improve data integration across your organization?",
    ]
    answers = [
        "Data silos",
        "We have been trying to create a service driven architecture to share data across systems using Mulesoft.",
        "We have a series of well documented REST services that allow sharing data between departments. However not all departments have bought into this, specially the billing department.",
        "Yes, but we are facing political issues with some departments not wanting to share their data.",
        "Billing data is related to personal data and money flows and should therefore only be accessed by the department itself or selected controllers. This is the main concern.",
    ]
    return questionnaire_str_adapter(questions, answers)


def provide_incomplete_questionnaire() -> str:
    questions = ["Which area of your data ecosystem are you most concerned about?"]
    answers = ["Data quality"]
    return questionnaire_str_adapter(questions, answers)
