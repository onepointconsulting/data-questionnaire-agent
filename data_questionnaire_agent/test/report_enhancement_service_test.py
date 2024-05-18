from data_questionnaire_agent.service.report_enhancement_service import (
    replace_bold_markdown,
    replace_markdown_bold_with_links,
)


def provider_string():
    return "This is some **bold** content with some **important** message as you can imagine."


def test_replace_bold_markdown():
    test_str = provider_string()
    res = replace_bold_markdown(test_str)
    assert (
        res
        == "This is some <b><a href='https://www.google.com/search?q=bold'>bold</a></b> content with some <b><a href='https://www.google.com/search?q=important'>important</a></b> message as you can imagine."
    ), f"Unexpected output: {res}"


def test_replace_markdown_bold_with_links():
    test_str = provider_string()
    res = replace_markdown_bold_with_links(test_str)
    assert (
        res
        == "This is some **[bold](https://www.google.com/search?q=bold)** content with some **[important](https://www.google.com/search?q=important)** message as you can imagine."
    ), f"Unexpected output: {res}"
