import asyncio

from data_questionnaire_agent.service.persistence_service_questions_async import (
    delete_question,
    insert_question,
)

if __name__ == "__main__":

    def test_insert_question():
        question = "Which is the meaning of life?"
        id = asyncio.run(
            insert_question(
                question,
                "en",
                [
                    {
                        "img_src": "",
                        "img_alt": "",
                        "title": "Test Suggestion Title",
                        "main_text": "This is the main text of the suggestion",
                        "svg_image": "",
                    }
                ],
            )
        )
        assert id > 0, "Id should be bigger than 0"
        count = asyncio.run(delete_question(id))
        assert count == 1, "Delete count is expected to be 1"

    test_insert_question()
