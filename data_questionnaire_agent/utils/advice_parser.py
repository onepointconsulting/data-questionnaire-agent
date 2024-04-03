from data_questionnaire_agent.model.openai_schema import ConditionalAdvice


def parse_advice(advice: str) -> ConditionalAdvice:
    sections = {}
    current_section = None
    section_count = 0
    consume_item = False
    current_item = ""
    for i, c in enumerate(advice):
        if c == "#" and advice[i + 1] == " ":
            section_count += 1
            if section_count == 1:
                current_section = "advice"
            else:
                current_section = "avoid"
            sections[current_section] = []
            current_item = ""
        elif c == "-" and advice[i + 1] == " ":
            consume_item = True
            current_item = ""
        elif (
            c == "\n"
            and i < len(advice) - 1
            and advice[i + 1] == "\n"
            and len(current_item) > 0
        ):
            consume_item = False
            sections[current_section].append(current_item.strip())
            current_item = ""
        elif consume_item:
            current_item += c
    return ConditionalAdvice(
        has_advice=True,
        advices=sections["advice"],
        what_you_should_avoid=sections["avoid"],
    )

    return None


if __name__ == "__main__":
    text = """# What you should do ...

- Given your concerns about data quality, specifically the issue of duplicate customer records, it would be beneficial to invest in machine learning (ML) capabilities. ML algorithms can significantly enhance the efficiency and accuracy of duplicate detection. However, as you've mentioned, maintaining human oversight is crucial. Therefore, a hybrid approach that combines automated ML tools with human review could be an optimal solution.

- Investing in training or hiring ML expertise could be a valuable step forward. This would not only help in addressing your current data quality issues but also equip your organisation with the skills needed to leverage ML for other data-related challenges in the future.

- Consider implementing a data governance policy if you haven't already. This would provide clear guidelines on data management practices within your organisation, promoting uniformity and improving overall data quality.

- Regular monitoring of data quality metrics can help you identify and address issues promptly. This could involve setting up alerts for key metrics or datasets and implementing a systematic process for resolving identified issues.

- Lastly, consider investing in data quality training for your employees. This would equip them with the necessary skills to handle data responsibly, thereby contributing to the overall quality of your data.

# What you should avoid ... 

- Avoid relying solely on manual processes for data quality management. While human oversight is important, manual processes can be time-consuming and prone to errors. Leveraging automated tools, where appropriate, can enhance efficiency and accuracy.

- Avoid neglecting the importance of data governance. Without clear policies and procedures in place, data management can become chaotic and inconsistent, leading to poor data quality.

- Avoid ignoring the potential of dark data. While it may seem challenging to integrate dark data into your data ecosystem, it can provide valuable insights when properly managed and analysed.


"""

    conditional_advice = parse_advice(text)
    assert len(conditional_advice.advices) == 5
    assert len(conditional_advice.what_you_should_avoid) == 3
