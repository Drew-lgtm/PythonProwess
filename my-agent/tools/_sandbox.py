"""Path sandbox: confine file operations to a base directory."""
from pathlib import Path

_BASE_DIR: Path = Path.cwd().resolve()


def set_base_dir(path: str | None = None) -> None:
    """Set the sandbox root. Pass None to use the current working directory."""
    global _BASE_DIR
    _BASE_DIR = Path(path).resolve() if path else Path.cwd().resolve()


def get_base_dir() -> Path:
    return _BASE_DIR


def resolve_in_sandbox(filepath: str) -> Path:
    """Resolve filepath relative to the sandbox root.

    Raises PermissionError if the resolved path escapes the sandbox.
    """
    p = Path(filepath)
    if not p.is_absolute():
        p = _BASE_DIR / p
    p = p.resolve()
    try:
        p.relative_to(_BASE_DIR)
    except ValueError as exc:
        raise PermissionError(
            f"Path {p} is outside the sandbox ({_BASE_DIR})."
        ) from exc
    return p
