import re
from functools import cache
from pathlib import Path

CSS_PATH = Path(__file__).with_name("theme.css")


@cache
def style_values() -> dict[str, str]:
    css = CSS_PATH.read_text(encoding="utf-8")
    return dict(re.findall(r"--(report-[\w-]+):\s*([^;]+);", css))
