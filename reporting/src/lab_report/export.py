from pathlib import Path
from typing import Annotated, Final

import nbformat
import typer
from nbclient import NotebookClient
from nbconvert import WebPDFExporter
from nbconvert.writers.files import FilesWriter
from traitlets.config import Config

from .highlighting import PastelStyle, RoleHighlight
from .theme import CSS_PATH

REPORT_TEMPLATE: Final[str] = r"""
{% extends 'lab/index.html.j2' %}
{% block any_cell %}
{% if 'page-break-before' in cell.metadata.get('tags', []) %}
<div class="report-page-break"></div>
{% endif %}
{{ super() }}
{% endblock any_cell %}
{% block html_head_css %}
{{ super() }}
{% for css in resources.inlining.css %}
<style>{{ css }}</style>
{% endfor %}
<style>
{{ resources.report_css }}
</style>
{% endblock html_head_css %}
"""


def export_notebook(
    notebook: Annotated[Path, typer.Argument(help="Notebook to execute and export.")],
    output: Annotated[
        Path | None, typer.Option("--output", "-o", help="Output PDF path.")
    ] = None,
) -> None:
    notebook = notebook.resolve()
    output = output or notebook.parent / "output" / "pdf" / f"{notebook.stem}.pdf"
    document = nbformat.read(notebook, as_version=4)
    for cell in document.cells:
        cell.metadata.pop("execution", None)
    NotebookClient(
        document,
        timeout=120,
        record_timing=False,
        resources={"metadata": {"path": str(notebook.parent)}},
    ).execute()
    nbformat.write(document, notebook)
    config = Config(
        {
            "CSSHTMLHeaderPreprocessor": {"style": PastelStyle},
            "TagRemovePreprocessor": {
                "enabled": True,
                "remove_cell_tags": {"remove-cell"},
                "remove_input_tags": {"remove-input"},
                "remove_all_outputs_tags": {"remove-output"},
            },
        }
    )
    exporter = WebPDFExporter(
        config=config,
        raw_template=REPORT_TEMPLATE,
        exclude_input_prompt=True,
        exclude_output_prompt=True,
        embed_images=True,
        allow_chromium_download=True,
        page_render_timeout=2_000,
        filters={
            "highlight_code": RoleHighlight(
                pygments_lexer=document.metadata.get("language_info", {}).get(
                    "pygments_lexer", "text"
                )
            )
        },
    )
    pdf, resources = exporter.from_notebook_node(
        document,
        resources={"report_css": CSS_PATH.read_text(encoding="utf-8")},
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    FilesWriter(build_directory=str(output.parent)).write(  # pyright: ignore[reportUnknownMemberType]
        pdf, resources, notebook_name=output.stem
    )
    typer.echo(output.resolve())


def main() -> None:
    typer.run(export_notebook)
