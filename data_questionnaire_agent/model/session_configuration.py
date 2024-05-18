from typing import Union, List
from pydantic import BaseModel, Field

DEFAULT_SESSION_STEPS = 6

SESSION_STEPS_CONFIG_KEY = "session-steps"


class SessionConfigurationEntry(BaseModel):
    id: Union[int, None] = Field(
        default=None, description="The identifier of this session configuration"
    )
    session_id: str = Field(..., description="The application's source identifier")
    config_key: str = Field(..., description="The configuration key")
    config_value: str = Field(..., description="The configuration value")


class SessionConfiguration(BaseModel):
    configuration_entries: List[SessionConfigurationEntry] = Field(
        ..., description="All session configuration entries"
    )
