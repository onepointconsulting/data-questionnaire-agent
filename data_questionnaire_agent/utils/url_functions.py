import urllib
import re


def get_url_text(url: str) -> str:
    splits = url.split("#:~:text=")
    if len(splits) == 1:
        return ""
    # Decode the url encoded text
    text = splits[1]
    text = urllib.parse.unquote(text)
    if re.search(r'%[0-9A-Fa-f]{2}', text):
        text = urllib.parse.unquote(text)
    return text