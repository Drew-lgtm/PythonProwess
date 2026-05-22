"""Git operations. All commands run in the sandbox directory."""
import subprocess

from . import _sandbox


def _run_git(args: list) -> str:
    try:
        result = subprocess.run(
            ["git"] + args,
            check=True,
            capture_output=True,
            text=True,
            cwd=str(_sandbox.get_base_dir()),
        )
        return result.stdout.strip() or "(no output)"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}\nOutput: {e.stdout.strip()}"


def get_status() -> str:
    """Show git working tree status (short form)."""
    return _run_git(["status", "--short"])


def get_diff() -> str:
    """Show unstaged changes in the working tree."""
    return _run_git(["diff"])


def add_files(path: str) -> str:
    """Stage files at `path` for the next commit."""
    return _run_git(["add", path])


def commit_changes(message: str) -> str:
    """Commit staged changes with the given message."""
    return _run_git(["commit", "-m", message])


def push_changes(remote: str = "origin", branch: str = "main") -> str:
    """Push commits to a remote branch. Confirm with the user before calling."""
    return _run_git(["push", remote, branch])
