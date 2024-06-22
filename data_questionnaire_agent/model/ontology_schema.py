from typing import Dict, List

from pydantic.v1 import BaseModel, Field


class Edge(BaseModel):
    """Represents single triplet with source, target and relationship names"""

    source: str = Field(..., description="The source node")
    relationship: str = Field(
        ..., description="The relationship between the source and the target node"
    )
    target: str = Field(..., description="The target node")


class Ontology(BaseModel):
    """Represents a container with a list of source, target and relationship names"""

    relationships: List[Edge] = Field(
        ...,
        description="The list of all edges in the questionnaire",
    )


class AnalyzedOntology(BaseModel):
    """Represents a container with a list of source, target and relationship names with extended measurements"""

    relationships: List[Edge] = Field(
        ...,
        description="The list of all edges with extended information in the questionnaire",
    )
    degree_centrality: Dict[str, float] = Field(
        ...,
        description="The dictionary of node to degree centrality",
    )
    betweenness_centrality: Dict[str, float] = Field(
        ...,
        description="The dictionary of node to degree betweenness",
    )
