from pydantic import BaseModel, Field


class EntityContextEntry(BaseModel):
    entity_name: str = Field(..., description="The entity name")
    entity_type: str = Field(..., description="The entity type")
    description: str = Field(..., description="The description of the entity")
    source_id: str = Field(..., description="The source identifier of the entity")
    file_path: str = Field(..., description="The file path of the entity")
    created_at: int = Field(..., description="The created timestamp")


class RelationsContextEntry(BaseModel):
    src_id: str = Field(..., description="The relationship name")
    tgt_id: str = Field(..., description="The relationship type")
    description: str = Field(..., description="The description of the relationship")
    keywords: str = Field(..., description="The source identifier of the relationship")
    file_path: str = Field(..., description="The file path of the relationship")
    created_at: int = Field(..., description="The created timestamp")


class TextUnitContextEntry(BaseModel):
    reference_id: str = Field(..., description="The text unit identifier")
    content: str = Field(..., description="The text unit type")
    file_path: str = Field(..., description="The file path of the relationship")
    chunk_id: str = Field(..., description="The file path of the relationship")


class Context(BaseModel):
    entities_context: list[EntityContextEntry] = Field(
        ..., description="The list of entity context entries"
    )
    relations_context: list[RelationsContextEntry] = Field(
        ..., description="The list of relationship context entries"
    )
    text_units_context: list[TextUnitContextEntry] = Field(
        ..., description="The list of text unit context entries"
    )
    context_text: str = Field(..., description="The context text")
