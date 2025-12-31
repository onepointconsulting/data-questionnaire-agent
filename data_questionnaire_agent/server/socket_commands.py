from enum import StrEnum

class Commands(StrEnum):
    START_SESSION = "start_session"
    SERVER_MESSAGE = "server_message"
    CLARIFICATION_TOKEN = "clarification_token"
    EXTEND_SESSION = "extend_session"
    ERROR = "error"
    REGENERATE_QUESTION = "regenerate_question"
    ADD_MORE_SUGGESTIONS = "add_more_suggestions"
    DEEP_RESEARCH_UPDATE = "deep_research_update"
    DEEP_RESEARCH_COMPLETE = "deep_research_complete"