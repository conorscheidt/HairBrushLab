import ast
import json
from itertools import accumulate
from pathlib import Path
from typing import ClassVar

from IPython.display import HTML
from nbconvert.filters.highlight import Highlight2HTML
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
from pygments.style import Style
from pygments.token import Comment, Keyword, Name, Number, Operator, String, Text

from .theme import style_values

_theme = style_values()


class PastelStyle(Style):
    background_color = _theme["report-paper"]
    styles: ClassVar = {
        Text: _theme["report-code-ink"],
        Comment: f"italic {_theme['report-comment']}",
        Keyword: f"bold {_theme['report-keyword']}",
        Name: _theme["report-code-ink"],
        Name.Builtin: _theme["report-number"],
        Name.Function: _theme["report-call"],
        Name.Class: _theme["report-module"],
        Name.Namespace: _theme["report-module"],
        Name.Attribute: _theme["report-attribute"],
        Name.Variable.Parameter: _theme["report-attribute"],
        Number: _theme["report-number"],
        String: _theme["report-string"],
        Operator: _theme["report-code-operator"],
    }


class PythonRoleLexer(PythonLexer):
    """Distinguish calls, attributes, and keyword arguments by their AST roles."""

    def get_tokens_unprocessed(self, text):
        lines = text.splitlines(keepends=True)
        starts = list(accumulate(map(len, lines), initial=0))
        try:
            tree = ast.parse(text)
        except SyntaxError:
            yield from super().get_tokens_unprocessed(text)
            return
        roles, modules = {}, set()

        def position(node, field="col_offset", line="lineno"):
            row = getattr(node, line) - 1
            prefix = lines[row].encode()[: getattr(node, field)].decode()
            return starts[row] + len(prefix)

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                modules.update(a.asname or a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.Attribute):
                end = position(node, "end_col_offset", "end_lineno")
                roles.setdefault(end - len(node.attr), Name.Attribute)
            elif isinstance(node, ast.Call) and isinstance(
                node.func, (ast.Name, ast.Attribute)
            ):
                name = (
                    node.func.id if isinstance(node.func, ast.Name) else node.func.attr
                )
                end = position(node.func, "end_col_offset", "end_lineno")
                roles[end - len(name)] = Name.Function
            elif isinstance(node, ast.keyword) and node.arg:
                roles[position(node)] = Name.Variable.Parameter

        for offset, token, value in super().get_tokens_unprocessed(text):
            fallback = Name.Namespace if token in Name and value in modules else token
            yield offset, roles.get(offset, fallback), value


def code_block(source: str) -> HTML:
    formatter = HtmlFormatter(style=PastelStyle, cssclass="report-code")
    css = formatter.get_style_defs(".report-code")
    return HTML(
        f"<style>{css}</style>" + highlight(source, PythonRoleLexer(), formatter)
    )


class RoleHighlight(Highlight2HTML):
    def __call__(self, source, language=None, metadata=None):
        language = language or self.pygments_lexer
        if language in {"python", "python3", "ipython", "ipython3"}:
            formatter = HtmlFormatter(style=PastelStyle, cssclass="highlight")
            return highlight(source, PythonRoleLexer(), formatter)
        return super().__call__(source, language, metadata)


def code_appendix(notebook: str | Path) -> HTML:
    cells = json.loads(Path(notebook).read_text(encoding="utf-8"))["cells"]
    sources = (
        "".join(cell["source"]).strip()
        for cell in cells
        if "include-code" in cell["metadata"].get("tags", [])
    )
    return code_block("\n\n".join(sources))
