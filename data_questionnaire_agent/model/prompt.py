from pydantic import BaseModel, Field
from datetime import datetime


class PromptCategory(BaseModel):
    id: int | None = Field(default=None, description="The unique identifier")
    name: str = Field(..., description="The name of the prompt category")
    prompt_category_parent_id: int | None = Field(
        default=None, description="The parent prompt category identifier"
    )
    created_at: datetime | None = Field(
        default=None, description="The created timestamp"
    )
    updated_at: datetime | None = Field(
        default=None, description="The updated timestamp"
    )


class DBPrompt(BaseModel):
    id: int | None = Field(default=None, description="The unique identifier")
    prompt_category: PromptCategory = Field(
        ..., description="The prompt category identifier"
    )
    prompt_key: str = Field(..., description="The prompt key")
    prompt: str = Field(..., description="The prompt")
    created_at: datetime | None = Field(
        default=None, description="The created timestamp"
    )
    updated_at: datetime | None = Field(
        default=None, description="The updated timestamp"
    )
