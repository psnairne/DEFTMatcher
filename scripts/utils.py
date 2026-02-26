from pathlib import Path


def get_project_root_str() -> str:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            return str(parent)
    raise RuntimeError("Project root not found")
