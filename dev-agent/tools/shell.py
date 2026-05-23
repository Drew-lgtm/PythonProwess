"""Shell command execution. Every command requires interactive user approval."""
import subprocess

from . import _sandbox


def run_command(command: str) -> str:
    """Execute a shell command in the sandbox directory after user approval."""
    cwd = str(_sandbox.get_base_dir())
    print(f"\n[ACTION REQUIRED] Agent wants to run (in {cwd}):")
    print(f"  $ {command}")
    user_approval = input("Allow execution? (y/n): ").strip().lower()
    if user_approval != "y":
        return "Error: Command execution denied by user."
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        return result.stdout.strip() or "(no output)"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}\nOutput: {e.stdout.strip()}"
