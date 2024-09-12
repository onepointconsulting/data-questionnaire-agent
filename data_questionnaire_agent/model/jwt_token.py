from pydantic.v1 import BaseModel, Field


class JWTToken(BaseModel):
    """JWT Token Data"""

    email: str = Field(..., description="The email")
    token: str = Field(..., description="The whole token")
