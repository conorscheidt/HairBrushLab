from functools import cache
from pathlib import Path

from tinycss2 import parse_blocks_contents, parse_stylesheet, serialize
from tinycss2.ast import Declaration, QualifiedRule

CSS_PATH = Path(__file__).with_name("theme.css")


@cache
def style_values() -> dict[str, str]:
    css = CSS_PATH.read_text(encoding="utf-8")
    rules = parse_stylesheet(css, skip_comments=True, skip_whitespace=True)
    return {
        declaration.name.removeprefix("--"): serialize(declaration.value).strip()
        for rule in rules
        if isinstance(rule, QualifiedRule)
        and serialize(rule.prelude).strip() == ":root"
        for declaration in parse_blocks_contents(
            rule.content, skip_comments=True, skip_whitespace=True
        )
        if isinstance(declaration, Declaration)
        and declaration.name.startswith("--report-")
    }
