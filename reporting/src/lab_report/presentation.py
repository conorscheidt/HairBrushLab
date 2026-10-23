from itertools import count

import matplotlib.pyplot as plt
import pandas as pd
from cycler import cycler
from matplotlib.axes import Axes
from matplotlib_inline.backend_inline import (
    set_matplotlib_formats,  # pyright: ignore[reportUnknownVariableType]
)
from pandas.io.formats.style import Styler

from .theme import style_values

_table_ids = count()


class ReportTable(Styler):
    """Styler with a stable text repr, so re-exported notebooks only diff on content."""

    def __repr__(self) -> str:
        return f"<ReportTable {self.uuid}>"


def use_report_style() -> None:
    theme = style_values()
    font = theme["report-font"].strip("'\"")
    set_matplotlib_formats("svg", metadata={"Date": None})
    plt.rcParams.update(  # pyright: ignore[reportUnknownMemberType]
        {
            "svg.fonttype": "none",
            "svg.hashsalt": "lab-report",
            "font.family": font,
            "font.size": 10,
            "text.color": theme["report-ink"],
            "axes.labelcolor": theme["report-ink"],
            "xtick.color": theme["report-ink"],
            "ytick.color": theme["report-ink"],
            "mathtext.fontset": "custom",
            "mathtext.rm": font,
            "mathtext.it": f"{font}:italic",
            "mathtext.bf": f"{font}:bold",
            "mathtext.cal": f"{font}:italic",
            "figure.figsize": (7.2, 6.5),
            "figure.constrained_layout.use": True,
            "figure.titlesize": 12,
            "axes.titlesize": 11,
            "axes.prop_cycle": cycler(
                color=[
                    theme["report-accent"],
                    theme["report-muted"],
                    theme["report-rust"],
                    theme["report-green"],
                ]
            ),
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.grid.axis": "y",
            "grid.alpha": 0.15,
            "grid.color": theme["report-grid"],
            "lines.linewidth": 1.7,
            "lines.solid_joinstyle": "round",
            "lines.solid_capstyle": "round",
        }
    )


def plot_reference(
    ax: Axes, value: float, *, label: str | None = None, vertical: bool = False
) -> None:
    line = ax.axvline if vertical else ax.axhline
    line(value, color=style_values()["report-reference"], ls="--", lw=0.8, label=label)


def styled_table(table: pd.DataFrame, *, precision: int = 3) -> ReportTable:
    font = style_values()["report-font"]
    styled = ReportTable(table, uuid=f"report{next(_table_ids)}")
    styled.hide(axis="index")
    styled.format(precision=precision)
    styled.set_properties(
        subset=None, **{"text-align": "right", "font-variant-numeric": "tabular-nums"}
    )
    styled.set_table_styles(
        [
            {"selector": "", "props": f"font-family: {font}, serif;"},
            {
                "selector": "thead th",
                "props": "text-align: right; border-bottom: 1px solid currentColor;",
            },
        ]
    )
    return styled
