from typing import Dict, Optional

from ulid import ULID


class AgentSession:
    def __init__(
        self,
        # Id from the session cookie
        socket_id: str,
        session_id: Optional[str],
    ):
        self.socket_id = socket_id
        self.session_id = (
            session_id
            if session_id is not None and len(session_id) > 0
            else str(ULID())
        )
        agent_sessions[self.session_id] = self


agent_sessions: Dict[str, AgentSession] = {}
