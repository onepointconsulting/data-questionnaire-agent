from data_questionnaire_agent.utils.url_functions import get_url_text


def test_get_url_text():
    assert (
        get_url_text(
            "https://raykhira.com/ai-red-teaming-breaking-your-models-before-attackers-do/#:~:text=2.%20Threat%20Modeling%20%2528ML,team%20exercises%252C%20automated%20fuzzers"
        )
        == "2. Threat Modeling (ML,team exercises, automated fuzzers"
    )
