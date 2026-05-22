"""File operations: all paths are resolved inside the sandbox."""
import difflib

from . import _sandbox


def read_file(filepath: str) -> str:
    """Read the contents of a file."""
    try:
        path = _sandbox.resolve_in_sandbox(filepath)
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {e}"


def _show_diff(old: str, new: str, label: str) -> None:
    diff = difflib.unified_diff(
        old.splitlines(keepends=True),
        new.splitlines(keepends=True),
        fromfile=f"{label} (before)",
        tofile=f"{label} (after)",
        n=2,
    )
    diff_text = "".join(diff)
    if diff_text:
        print("\n--- diff preview ---")
        print(diff_text, end="" if diff_text.endswith("\n") else "\n")
        print("--- end diff ---")


def write_file(filepath: str, content: str) -> str:
    """Create or overwrite a file. Prints a unified diff before writing."""
    try:
        path = _sandbox.resolve_in_sandbox(filepath)
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        _show_diff(old, content, str(path))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {e}"


def edit_file(filepath: str, old_string: str, new_string: str) -> str:
    """Surgical edit: replace old_string with new_string in filepath.

    old_string must appear exactly once. Prints a unified diff before writing.
    """
    try:
        path = _sandbox.resolve_in_sandbox(filepath)
        if not path.exists():
            return f"Error: {path} does not exist."
        original = path.read_text(encoding="utf-8")
        count = original.count(old_string)
        if count == 0:
            return (
                f"Error: old_string not found in {path}. "
                "Read the file first and copy the exact text to replace."
            )
        if count > 1:
            return (
                f"Error: old_string occurs {count} times in {path}. "
                "Include more surrounding context to make it unique."
            )
        updated = original.replace(old_string, new_string, 1)
        _show_diff(original, updated, str(path))
        path.write_text(updated, encoding="utf-8")
        return f"Successfully edited {path}"
    except Exception as e:
        return f"Error editing file: {e}"


def list_directory(path: str = ".") -> str:
    """List the contents of a directory (sorted by name)."""
    try:
        resolved = _sandbox.resolve_in_sandbox(path)
        if not resolved.is_dir():
            return f"Error: {resolved} is not a directory."
        return "\n".join(sorted(p.name for p in resolved.iterdir()))
    except Exception as e:
        return f"Error listing directory: {e}"
