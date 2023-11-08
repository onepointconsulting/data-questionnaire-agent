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
