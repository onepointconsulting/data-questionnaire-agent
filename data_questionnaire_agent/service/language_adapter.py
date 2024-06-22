import re

ACCEPTED_LANGUAGES = ["en", "de", "fa"]


def adapt_language(language: str) -> str:
    first_chars = re.sub(r"^([a-z]{2}).*", r"\1", language)
    if first_chars in ACCEPTED_LANGUAGES:
        return first_chars
    return ACCEPTED_LANGUAGES[0]


if __name__ == "__main__":
    assert adapt_language("en-GB") == "en"
    assert adapt_language("en") == "en"
    assert adapt_language("de-DB") == "de"
    assert adapt_language("de-AT") == "de"
    assert adapt_language("pt-PT") == "en"
