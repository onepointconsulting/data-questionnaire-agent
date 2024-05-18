import re
from urllib.parse import quote


PATTERN_MARKDOWN_BOLD = re.compile(r"\*\*(?P<content>.+?)\*\*")


def replace_bold_markdown(
    html: str,
    format_str="<b><a href='https://www.google.com/search?q={quoted_content}'>{content}</a></b>",
) -> str:
    # Output string initialization
    output = []
    last_end = 0  # This keeps track of the end of the last match
    for match in PATTERN_MARKDOWN_BOLD.finditer(html):
        start, end = match.span()
        content = match.group("content")
        quoted_content = quote(content)
        output.append(html[last_end:start])
        replacement = format_str.format(quoted_content=quoted_content, content=content)
        output.append(replacement)
        last_end = end
    output.append(html[last_end:])

    return "".join(output)


def replace_markdown_bold_with_links(text: str) -> str:
    return replace_bold_markdown(
        text, "**[{content}](https://www.google.com/search?q={quoted_content})**"
    )
