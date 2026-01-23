from pydantic import BaseModel, Field


class ContextDocument(BaseModel):
    id: int | None = Field(default=None, description="The identifier of the document")
    document_path: str = Field(..., description="The path to the document")
    document_name: str = Field(..., description="The name of the document")
    count: int = Field(..., description="The count of the document")
    document_extracts: list[str] | None = Field(
        default=None, description="The extract of the document"
    )


class ContextDocuments(BaseModel):
    questionnaire_status_id: int | None = Field(
        default=None, description="The identifier of the questionnaire status"
    )
    documents: list[ContextDocument] = Field(
        ..., description="The list of context documents"
    )
