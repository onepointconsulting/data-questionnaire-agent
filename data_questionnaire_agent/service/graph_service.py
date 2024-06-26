from typing import Dict, List, Tuple

import networkx as nx

from data_questionnaire_agent.model.ontology_schema import AnalyzedOntology, Ontology


def generate_analyzed_ontology(ontology_data: Ontology) -> AnalyzedOntology:
    relationships = ontology_data.relationships
    if relationships is None:
        return AnalyzedOntology(relationships=[])
    name_id_dict, id_name_dict = extract_nodes(relationships)
    edges = extract_edges(relationships, name_id_dict)

    G = nx.Graph()
    for name, id in name_id_dict.items():
        G.add_node(id, name=name)
    G.add_edges_from(edges)

    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

    degree_centrality_: Dict[str, float] = {
        id_name_dict[id]: centrality for id, centrality in degree_centrality.items()
    }
    betweenness_centrality_: Dict[str, float] = {
        id_name_dict[id]: centrality
        for id, centrality in betweenness_centrality.items()
    }
    return AnalyzedOntology(
        relationships=relationships,
        degree_centrality=degree_centrality_,
        betweenness_centrality=betweenness_centrality_,
    )


def extract_nodes(
    relationships: List[Dict[str, str]]
) -> Tuple[Dict[str, int], Dict[int, str]]:
    node_set = set()
    for r in relationships:
        node_set.add(r.source)
        node_set.add(r.target)
    name_id_dict = {r: i for i, r in enumerate(node_set)}
    id_name_dict = {i: r for i, r in enumerate(node_set)}
    return (name_id_dict, id_name_dict)


def extract_edges(
    relationships: List[Dict[str, str]], node_map: Dict[int, str]
) -> List[Tuple[int, int]]:
    edges = []
    for rel in relationships:
        source_id = node_map[rel.source]
        target_id = node_map[rel.target]
        edges.append((source_id, target_id))
    return edges
