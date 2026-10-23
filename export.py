from pathlib import Path
from shutil import rmtree

from lab_report.export import export_notebook

if __name__ == "__main__":
    root = Path(__file__).parent
    rmtree(root / "output/postlab", ignore_errors=True)
    export_notebook(root / "Hair_Brush_Post_Lab.ipynb")
