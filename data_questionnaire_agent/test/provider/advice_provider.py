from typing import Tuple

from data_questionnaire_agent.model.application_schema import (
    QuestionAnswer,
    Questionnaire,
)
from data_questionnaire_agent.model.openai_schema import ConditionalAdvice


def create_simple_advice() -> ConditionalAdvice:
    return ConditionalAdvice(
        has_advice=True,
        advices=[
            """Consider implementing data governance policies to ensure uniformity in handling and managing data throughout your organization. \
These policies should outline roles, responsibilities, standards, and processes related to data management. \
Implementing clear guidelines on collecting, storing, processing, and sharing information within the company can, over time, significantly improve overall data quality.""",
            """You may want to consider using data cleansing tools. These tools are designed to automatically identify errors in datasets \
by comparing them against predefined rules or patterns. They can also be used for tasks like removing duplicates from records \
or normalizing values according to specific criteria. Regularly using these tools ensures that your systems store only high-quality information.""",
            """Consider implementing data validation techniques beyond fuzzy matching lookups. \
Introducing checks like format validation, range constraints, or referential integrity rules \
helps prevent incorrect or inconsistent values from entering your databases.""",
            """Consider implementing feedback loops. Feedback loops involve gathering input from end-users \
regarding potential inaccuracies in datasets or reporting outputs. \
Fostering a culture of open communication around possible errors allows organizations to identify problems quickly and proactively implement necessary changes.""",
            """Monitor data quality metrics. Measuring data quality metrics, such as completeness, accuracy, consistency, timeliness, or uniqueness, \
is crucial for identifying areas where improvements can be made. Regularly monitoring these metrics \
enables you to detect issues early on and take corrective actions before they affect business operations.
""",
        ],
        what_you_should_avoid=[],
        positive_outcomes=[],
        confidence=None,
    )


def create_advice_2() -> ConditionalAdvice:
    return ConditionalAdvice(
        has_advice=True,
        advices=[
            """Given your concerns about invalid and duplicate data, it's crucial to enhance your data validation and deduplication processes. \
Consider implementing more sophisticated data validation techniques, such as using advanced data profiling tools that can automatically detect and correct invalid entries.""",
            """Your current method of using a simple rule engine for deduplication might not be sufficient for handling complex or large datasets. \
Consider using automated deduplication tools that can identify and eliminate redundant records more efficiently and accurately.""",
            """Your ETL jobs seem to be doing a good job at checking the validity of certain fields. \
However, to improve the overall data quality, consider expanding these checks to other important fields as well.""",
            """You mentioned that you are using a data warehouse with a single source of truth for customers. To ensure the consistency and accuracy of this data, \
consider implementing a robust data governance policy. This policy should outline roles, responsibilities, standards, and processes related to data management.""",
            """Lastly, consider implementing data observability practices. This involves continuously monitoring, tracking, and analyzing your data \
as it flows through various stages of processing, storage, and transformation. This can help you maintain data integrity, detect anomalies, and troubleshoot issues in real-time or near-real-time.
""",
        ],
    )


def create_advice_with_questionnaire() -> Tuple[ConditionalAdvice, Questionnaire]:
    conditional_advice = ConditionalAdvice(
        has_advice=True,
        advices=[
            "**Implement Automated Deduplication Tools**: Given that manual checks for duplicates are time-consuming and error-prone, consider implementing automated deduplication tools. These tools can identify and merge duplicate records across your CRM systems, e-commerce platforms, and customer service databases, significantly improving data quality and operational efficiency.",
            "**Standardise Data Formats and Naming Conventions**: To address the issue of varying data formats and standards across different systems, establish and enforce standardised data formats and naming conventions. This will help ensure consistency and reduce the likelihood of duplicates and other data quality issues.",
            "**Introduce Data Governance Policies**: Establishing data governance policies can help manage data quality more effectively. These policies should outline roles, responsibilities, standards, and processes related to data management, ensuring that all stakeholders are accountable for maintaining high data quality.",
            "**Utilise Data Profiling and Cleansing Tools**: Before data is integrated into your systems, use data profiling and cleansing tools to verify its quality. These tools can help identify and correct inconsistencies, inaccuracies, and duplicates, ensuring that only high-quality data enters your systems.",
            "**Monitor Data Quality Metrics**: Regularly monitor data quality metrics such as completeness, accuracy, consistency, timeliness, and uniqueness. This will enable you to detect and address data quality issues early, preventing them from affecting business operations.",
        ],
        what_you_should_avoid=[
            "**Avoid Relying Solely on Manual Processes**: Manual checks for duplicates and data quality issues are prone to errors and inefficiencies. Relying solely on these processes can lead to significant data quality problems.",
            "**Avoid Ignoring Data Governance**: Without clear data governance policies, it is challenging to maintain high data quality. Ignoring data governance can result in inconsistent data management practices and poor data quality.",
            "**Avoid Overlooking Data Standardisation**: Failing to standardise data formats and naming conventions across systems can lead to inconsistencies and duplicates. Overlooking this aspect can exacerbate data quality issues.",
        ],
        positive_outcomes=[
            "**Improved Operational Efficiency**: By automating deduplication and standardising data formats, you can significantly reduce the time and effort required to manage data quality, leading to improved operational efficiency.",
            "**Enhanced Decision-Making**: High-quality, consistent data enables more accurate analyses and better-informed decision-making, ultimately driving business growth and profitability.",
            "**Increased Customer Satisfaction**: By maintaining accurate and up-to-date customer records, you can provide better service to your customers, leading to increased satisfaction and loyalty.",
        ],
    )
    questionnaire = Questionnaire(
        questions=[
            QuestionAnswer(
                id=None,
                question="Which area of your data ecosystem are you most concerned about?",
                answer="Poor data quality - Low-quality data can lead to incorrect insights and poor decision-making.",
                clarification=None,
            ),
            QuestionAnswer(
                id=None,
                question="What specific challenges or pain points are you experiencing with data quality in your organisation?",
                answer="We have too many customer duplicates.\n",
                clarification=None,
            ),
            QuestionAnswer(
                id=None,
                question="How do you currently identify and manage duplicate customer records in your data systems?",
                answer=" - We use manual checks to identify duplicates, which is time-consuming and prone to errors.",
                clarification=None,
            ),
            QuestionAnswer(
                id=None,
                question="What are the main sources of data in your organisation, and how do they contribute to the issue of duplicate customer records?",
                answer=" - Our main sources of data include CRM systems, e-commerce platforms, and customer service databases. Each system often has its own way of recording customer information, leading to inconsistencies and duplicates.",
                clarification=None,
            ),
            QuestionAnswer(
                id=None,
                question="What are the key challenges you face in maintaining data consistency across different systems in your organisation?",
                answer=" - Different systems have varying data formats and standards, making it difficult to ensure consistency.",
                clarification=None,
            ),
        ]
    )
    return conditional_advice, questionnaire
