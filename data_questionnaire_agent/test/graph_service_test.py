from data_questionnaire_agent.service.graph_service import generate_analyzed_ontology
from data_questionnaire_agent.test.provider.ontology_provider import create_ontology


def test_generate_analyzed_ontology():
    ontology = create_ontology()
    analyzed_ontology = generate_analyzed_ontology(ontology)
    assert analyzed_ontology is not None
    assert analyzed_ontology.relationships is not None
    assert analyzed_ontology.degree_centrality is not None
    assert analyzed_ontology.betweenness_centrality is not None
    assert len(analyzed_ontology.degree_centrality) == len(
        analyzed_ontology.betweenness_centrality
    )
