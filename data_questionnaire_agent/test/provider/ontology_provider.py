from data_questionnaire_agent.model.ontology_schema import Ontology


def create_ontology():
    ontology_json = {
        "relationships": [
            {
                "source": "Poor data quality",
                "relationship": "leads to",
                "target": "incorrect insights",
            },
            {
                "source": "Poor data quality",
                "relationship": "leads to",
                "target": "poor decision-making",
            },
            {
                "source": "Customer duplicates",
                "relationship": "is a challenge in",
                "target": "data quality",
            },
            {
                "source": "Manual checks",
                "relationship": "used for",
                "target": "identifying duplicates",
            },
            {
                "source": "Manual checks",
                "relationship": "leads to",
                "target": "time-consuming process",
            },
            {"source": "Manual checks", "relationship": "leads to", "target": "errors"},
            {
                "source": "CRM systems",
                "relationship": "contributes to",
                "target": "duplicate customer records",
            },
            {
                "source": "E-commerce platforms",
                "relationship": "contributes to",
                "target": "duplicate customer records",
            },
            {
                "source": "Customer service databases",
                "relationship": "contributes to",
                "target": "duplicate customer records",
            },
            {
                "source": "Different systems",
                "relationship": "have",
                "target": "varying data formats and standards",
            },
            {
                "source": "Automated Deduplication Tools",
                "relationship": "improves",
                "target": "data quality",
            },
            {
                "source": "Automated Deduplication Tools",
                "relationship": "improves",
                "target": "operational efficiency",
            },
            {
                "source": "Standardised Data Formats and Naming Conventions",
                "relationship": "reduces",
                "target": "duplicates",
            },
            {
                "source": "Data Governance Policies",
                "relationship": "manages",
                "target": "data quality",
            },
            {
                "source": "Data Profiling and Cleansing Tools",
                "relationship": "identifies and corrects",
                "target": "inconsistencies, inaccuracies, and duplicates",
            },
            {
                "source": "Data Quality Metrics",
                "relationship": "detects and addresses",
                "target": "data quality issues",
            },
            {
                "source": "Manual Processes",
                "relationship": "leads to",
                "target": "data quality problems",
            },
            {
                "source": "Ignoring Data Governance",
                "relationship": "results in",
                "target": "poor data quality",
            },
            {
                "source": "Overlooking Data Standardisation",
                "relationship": "leads to",
                "target": "data quality issues",
            },
            {
                "source": "Automating deduplication and standardising data formats",
                "relationship": "leads to",
                "target": "improved operational efficiency",
            },
            {
                "source": "High-quality, consistent data",
                "relationship": "enables",
                "target": "better-informed decision-making",
            },
            {
                "source": "Accurate and up-to-date customer records",
                "relationship": "leads to",
                "target": "increased customer satisfaction",
            },
        ]
    }
    ontology = Ontology.parse_obj(ontology_json)
    return ontology
