from pydantic.v1 import BaseModel, Field

from data_questionnaire_agent.log_init import logger


class GlobalConfigurationProperty(BaseModel):
    config_key: str = Field(..., description="The configuration key")
    config_value: str = Field(..., description="The configuration value")


class GlobalConfiguration(BaseModel):
    properties: list[GlobalConfigurationProperty] = Field(
        ..., description="The list of properties in the configuration"
    )

    def get_default_session_steps(self, default_steps: int):
        for p in self.properties:
            if p.config_key == "MESSAGE_LOWER_LIMIT":
                try:
                    return int(p.config_value)
                except ValueError as e:
                    logger.warn(
                        f"Could not extract default steps from configuration: {e}"
                    )
                    return default_steps
        return default_steps
