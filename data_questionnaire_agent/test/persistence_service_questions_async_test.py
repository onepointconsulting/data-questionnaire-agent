import asyncio

from data_questionnaire_agent.service.persistence_service_questions_async import (
    delete_question,
    insert_question,
)


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
    print("Inserted question id", id)
    assert id > 0, "Id should be bigger than 0"
    return id

# I created seperate functions, so i can test them separately if needed.


def test_delete_question(id: int):
    count = asyncio.run(delete_question(id))
    assert count == 1, "Delete count is expected to be 1"
    print("Delete count", count)


if __name__ == "__main__":
    question_id = test_insert_question()
    # You can also pass id manually to test_delete_question function
    test_delete_question(question_id)
