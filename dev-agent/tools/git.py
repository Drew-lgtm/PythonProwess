"""Git operations. All commands run in the sandbox directory."""
import subprocess

from . import _sandbox


def _run_git(args: list, check: bool = True) -> str:
    try:
        result = subprocess.run(
            ["git"] + args,
            check=check,
            capture_output=True,
            text=True,
            cwd=str(_sandbox.get_base_dir()),
        )
        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}\nOutput: {result.stdout.strip()}"
        return result.stdout.strip() or "(no output)"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}\nOutput: {e.stdout.strip()}"


def _ask_approval(prompt: str) -> bool:
    answer = input(f"{prompt} (y/n): ").strip().lower()
    return answer == "y"


def get_status() -> str:
    """Show git working tree status (short form)."""
    return _run_git(["status", "--short"])


def get_diff() -> str:
    """Show unstaged changes in the working tree."""
    return _run_git(["diff"])


def add_files(path: str) -> str:
    """Stage files at `path` after user approval."""
    print("\n[ACTION REQUIRED] Agent wants to stage files:")
    print(f"  git add {path}")
    if not _ask_approval("Allow staging these files for commit review?"):
        return "Error: Staging denied by user."
    return _run_git(["add", path])


def commit_changes(message: str) -> str:
    """Commit staged changes after the user reviews and approves them."""
    print("\n[COMMIT REVIEW] Staged changes:")
    print(_run_git(["diff", "--cached"], check=False))
    print("\n[COMMIT REVIEW] Status:")
    print(_run_git(["status", "--short"], check=False))
    print(f"\n[COMMIT REVIEW] Proposed message: {message}")
    if not _ask_approval("Commit these staged changes?"):
        return "Error: Commit denied by user."
    return _run_git(["commit", "-m", message])


def push_changes(remote: str = "origin", branch: str = "main") -> str:
    """Push commits to a remote branch."""
    return _run_git(["push", remote, branch])
