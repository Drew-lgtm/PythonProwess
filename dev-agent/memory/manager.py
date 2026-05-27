"""Persist and reload chat history across runs."""
import json
from pathlib import Path

MEMORY_FILE = Path(__file__).parent / "history.json"


def _serialize_part(part) -> dict | None:
    """Convert one Content.part to a JSON-safe dict."""
    if getattr(part, "text", None):
        return {"text": part.text}
    fc = getattr(part, "function_call", None)
    if fc and getattr(fc, "name", None):
        return {
            "function_call": {
                "name": fc.name,
                "args": dict(fc.args) if fc.args else {},
            }
        }
    fr = getattr(part, "function_response", None)
    if fr and getattr(fr, "name", None):
        return {
            "function_response": {
                "name": fr.name,
                "response": dict(fr.response) if fr.response else {},
            }
        }
    return None


def serialize_history(history) -> list[dict]:
    """Convert SDK chat history into JSON-safe dicts."""
    out = []
    for content in history:
        parts = []
        for p in (content.parts or []):
            sp = _serialize_part(p)
            if sp is not None:
                parts.append(sp)
        out.append({"role": content.role, "parts": parts})
    return out


def deserialize_history(data: list[dict]):
    """Rehydrate JSON dicts into SDK Content objects."""
    from google.genai import types

    out = []
    for item in data:
        parts = []
        for p in item.get("parts", []):
            if "text" in p:
                parts.append(types.Part(text=p["text"]))
            elif "function_call" in p:
                fc = p["function_call"]
                parts.append(
                    types.Part(
                        function_call=types.FunctionCall(
                            name=fc["name"],
                            args=fc.get("args", {}),
                        )
                    )
                )
            elif "function_response" in p:
                fr = p["function_response"]
                parts.append(
                    types.Part(
                        function_response=types.FunctionResponse(
                            name=fr["name"],
                            response=fr.get("response", {}),
                        )
                    )
                )
        out.append(types.Content(role=item["role"], parts=parts))
    return out


def save_history(history) -> None:
    """Persist history. Accepts SDK objects or already-serialized dicts."""
    try:
        if history and not isinstance(history[0], dict):
            history = serialize_history(history)
    except Exception as e:
        print(f"[memory] failed to serialize history: {e}")
        return
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def load_history() -> list[dict]:
    if not MEMORY_FILE.exists():
        return []
    try:
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def clear_history() -> None:
    if MEMORY_FILE.exists():
        MEMORY_FILE.unlink()


def _history_role(item) -> str | None:
    """Read a role from serialized history dicts or SDK Content objects."""
    role = item.get("role") if isinstance(item, dict) else getattr(item, "role", None)
    return getattr(role, "value", role)


def trim_history(history, max_user_turns: int = 10):
    """Keep only the last `max_user_turns` user messages (and what follows)."""
    if not history:
        return history
    user_indices = [i for i, h in enumerate(history) if _history_role(h) == "user"]
    if len(user_indices) <= max_user_turns:
        return history
    cutoff = user_indices[-max_user_turns]
    return history[cutoff:]
