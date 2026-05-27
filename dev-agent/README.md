# my-agent

A local coding agent powered by Gemini. It reads/edits files, runs shell
commands (with your approval), and operates on git - all on your machine.

## Setup

Run these commands from the `dev-agent` directory:

```powershell
python -m pip install -r requirements.txt
$env:GEMINI_API_KEY = "<your-key>"
```

Get a key at https://aistudio.google.com/apikey (free tier is enough).

If you are in the repository root instead, prefix paths with `dev-agent\`:

```powershell
python -m pip install -r dev-agent\requirements.txt
python dev-agent\main.py --list-personas
```

## Run it

**Interactive (REPL):**
```powershell
python main.py
```
Type a message, press Enter. `exit` to quit, `/reset` to clear history.

**One-shot:**
```powershell
python main.py "list the files and summarize what this project does"
```

## Personas

The agent has three built-in personas:

| Persona     | Use it for                                      | Edit/git tools |
| ----------- | ----------------------------------------------- | -------------- |
| `planner`   | Understand the task and propose an execution plan | No             |
| `developer` | Implement changes, run checks, stage, commit, push | Yes            |
| `reviewer`  | Review diffs and run focused verification         | No             |

Recommended flow:

```powershell
python main.py --persona planner "plan the change"
python main.py --persona developer "implement the approved plan"
python main.py --persona reviewer "review the current diff"
```

`tester` is kept as a backwards-compatible alias for `reviewer`.

## Operational Smoke Test

From the repository root:

```powershell
python dev-agent\main.py --list-personas
python dev-agent\main.py --persona planner --cwd . "Inspect the repo and suggest one safe README improvement"
python dev-agent\main.py --persona reviewer --cwd . "Check git status and summarize current changes"
python dev-agent\main.py --persona developer --cwd . "Create a small scratch file named agent-smoke-test.txt with one sentence"
```

The developer persona should show a diff before writing. When you later ask it
to stage or commit, it should ask for approval first.

## Flags

| Flag             | What it does                                    |
| ---------------- | ----------------------------------------------- |
| `--persona NAME` | Load `prompts/<name>.txt` (default: developer)  |
| `--list-personas`| Show available personas and aliases             |
| `--cwd PATH`     | Sandbox the agent to this directory             |
| `--reset`        | Clear chat history before starting              |

That's it. The agent will ask before running any shell command, staging files,
or creating a commit. Pushes can run directly once you ask the agent to push.
