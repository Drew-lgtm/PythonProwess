"""Local Gemini coding agent: REPL + one-shot mode, sandboxed, history-aware."""
import argparse
import os
import sys
from pathlib import Path

from tools import _sandbox, files, git, shell
from memory import manager


MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
DEFAULT_MAX_TOOL_CALLS = 20
PROMPT_DIR = Path(__file__).parent / "prompts"
PERSONA_ALIASES = {"tester": "reviewer"}


def available_personas() -> list[str]:
    """Return persona names backed by prompts/<name>.txt files."""
    return sorted(p.stem for p in PROMPT_DIR.glob("*.txt"))


def resolve_persona(name: str) -> str:
    """Resolve backwards-compatible persona aliases."""
    return PERSONA_ALIASES.get(name, name)


def load_persona(name: str) -> tuple[str, str]:
    """Load a persona system prompt (e.g. 'planner', 'developer', 'reviewer')."""
    persona = resolve_persona(name)
    path = PROMPT_DIR / f"{persona}.txt"
    if not path.exists():
        available = ", ".join(available_personas())
        aliases = ", ".join(f"{k}->{v}" for k, v in sorted(PERSONA_ALIASES.items()))
        if aliases:
            available = f"{available} (aliases: {aliases})"
        raise FileNotFoundError(
            f"Unknown persona '{name}'. Available: {available or '(none)'}"
        )
    return persona, path.read_text(encoding="utf-8")


def tools_for_persona(persona: str) -> list:
    """Return the tool set for a persona.

    New personas default to inspection tools until explicitly granted edit/git writes.
    """
    inspection_tools = [
        files.read_file,
        files.list_directory,
        shell.run_command,
        git.get_status,
        git.get_diff,
    ]
    if persona != "developer":
        return inspection_tools
    return inspection_tools + [
        files.write_file,
        files.edit_file,
        git.add_files,
        git.commit_changes,
        git.push_changes,
    ]


def build_chat(
    client,
    system_prompt: str,
    history_dicts: list[dict],
    persona: str,
):
    from google.genai import types

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=tools_for_persona(persona),
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            maximum_remote_calls=DEFAULT_MAX_TOOL_CALLS,
        ),
    )
    history = manager.deserialize_history(history_dicts) if history_dicts else None
    return client.chats.create(model=MODEL_NAME, config=config, history=history)


def send_and_report(chat, message: str) -> None:
    try:
        response = chat.send_message(message)
    except Exception as e:
        print(f"[error] {e}")
        return

    print("\nAgent:")
    print(response.text or "(no text response)")

    usage = getattr(response, "usage_metadata", None)
    if usage:
        prompt = getattr(usage, "prompt_token_count", "?")
        out = getattr(usage, "candidates_token_count", "?")
        total = getattr(usage, "total_token_count", "?")
        print(f"\n[tokens] prompt={prompt} response={out} total={total}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Local Gemini coding agent.")
    parser.add_argument(
        "task", nargs="*",
        help="One-shot task. If omitted, opens an interactive REPL."
    )
    parser.add_argument(
        "--persona", default="developer",
        help="Which prompts/<name>.txt to load (default: developer).",
    )
    parser.add_argument(
        "--list-personas", action="store_true",
        help="List available personas and exit.",
    )
    parser.add_argument(
        "--reset", action="store_true",
        help="Clear chat history before starting.",
    )
    parser.add_argument(
        "--cwd", default=None,
        help="Sandbox directory (default: current working directory).",
    )
    parser.add_argument(
        "--max-history", type=int, default=10,
        help="Max user turns retained in history (default: 10).",
    )
    args = parser.parse_args()

    if args.list_personas:
        print("Available personas:")
        for persona in available_personas():
            print(f"- {persona}")
        if PERSONA_ALIASES:
            print("Aliases:")
            for alias, persona in sorted(PERSONA_ALIASES.items()):
                print(f"- {alias} -> {persona}")
        return

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)

    _sandbox.set_base_dir(args.cwd)
    print(f"[sandbox] {_sandbox.get_base_dir()}")

    try:
        persona, system_prompt = load_persona(args.persona)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    persona_label = persona if persona == args.persona else f"{args.persona} -> {persona}"
    print(f"[persona] {persona_label}")
    print(f"[model]   {MODEL_NAME}")

    if args.reset:
        manager.clear_history()
        print("[memory] history cleared")

    history_dicts = manager.trim_history(manager.load_history(), args.max_history)
    from google import genai

    client = genai.Client(api_key=api_key)
    chat = build_chat(client, system_prompt, history_dicts, persona)

    if args.task:
        task = " ".join(args.task)
        print(f"[task] {task}")
        send_and_report(chat, task)
        manager.save_history(
            manager.trim_history(chat.get_history(), args.max_history)
        )
        return

    print("[repl] type 'exit' (or Ctrl+C) to quit, '/reset' to clear history")
    while True:
        try:
            user_input = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            break
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            break
        if user_input == "/reset":
            manager.clear_history()
            chat = build_chat(client, system_prompt, [], persona)
            print("[memory] history cleared")
            continue
        send_and_report(chat, user_input)
        manager.save_history(
            manager.trim_history(chat.get_history(), args.max_history)
        )


if __name__ == "__main__":
    main()
