from typing import Optional

from pydantic.v1 import BaseModel, Field


class JWTToken(BaseModel):
    """JWT Token Data"""

    email: str = Field(..., description="The email")
    token: str = Field(..., description="The whole token")


class JWTTokenData(BaseModel):
    name: str = Field(..., description="The subject on the token")
    email: str = Field(..., description="The email")
    time_delta_minutes: Optional[int] = Field(
        ..., description="Determines the expiry date of the token"
    )
