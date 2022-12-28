import json

default_locale = "en-gb"
cached_strings = {}


def refresh() -> None:
    global cached_strings
    with open(f"app/strings/{default_locale}.json") as f:
        cached_strings = json.load(f)


def get_text(name) -> str:
    return cached_strings[name]


refresh()
