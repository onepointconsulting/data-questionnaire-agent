from pydantic.v1 import BaseModel, Field


class GlobalConfigurationProperty(BaseModel):
    config_key: str = Field(..., description="The configuration key")
    config_value: str = Field(..., description="The configuration value")


class GlobalConfiguration(BaseModel):
    properties: list[GlobalConfigurationProperty] = Field(
        ..., description="The list of properties in the configuration"
    )
