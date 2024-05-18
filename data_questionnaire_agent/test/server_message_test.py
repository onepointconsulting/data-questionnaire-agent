from data_questionnaire_agent.model.server_model import ServerMessage


def test_simple_server_message():
    question = "test"
    session_id = "1231231231231"
    server_message = ServerMessage(question=question, session_id=session_id)
    server_message_str = server_message.json()
    assert question in server_message_str
    assert session_id in server_message_str
