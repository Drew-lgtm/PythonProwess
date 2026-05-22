# my-agent

A local coding agent that uses the Gemini API for reasoning and executes
file, shell, and git operations locally on your machine.

The cloud is only used to call the Gemini API. Code execution, file edits,
and git operations happen entirely on your computer. Shell commands require
interactive `y/n` approval per call.

## Layout

```
my-agent/
  main.py              REPL + one-shot mode, persona loading, history
  requirements.txt     google-genai
  prompts/
    developer.txt      Default persona: writes and edits code
    tester.txt         Persona for writing tests and reporting failures
  tools/
    _sandbox.py        Confines file ops to a base directory
    files.py           read_file, write_file (with diff), edit_file, list_directory
    shell.py           run_command (with user approval)
    git.py             status, diff, add, commit, push
  memory/
    manager.py         Serialize/deserialize/trim chat history
    history.json       Persisted chat history (gitignored)
```

## Setup

```powershell
python -m pip install -r requirements.txt
$env:GEMINI_API_KEY = "<your-key>"
```

## Usage

### REPL mode
```powershell
python main.py
```

Type a message, press Enter. The agent decides which tools to call. Type
`/reset` to clear history, `exit` (or Ctrl+C) to quit.

### One-shot mode
```powershell
python main.py "List the files in the current directory"
```

### Flags
- `--persona developer|tester` — which system prompt to load (default: developer)
- `--cwd <path>` — sandbox the agent to this directory (default: cwd)
- `--reset` — clear history before starting
- `--max-history N` — keep only the last N user turns (default: 10)

### Environment
- `GEMINI_API_KEY` (required)
- `GEMINI_MODEL` (optional, default `gemini-2.5-flash`)

## Tools the agent can call

| Tool             | Purpose                                                  |
| ---------------- | -------------------------------------------------------- |
| read_file        | Read a file's contents                                   |
| write_file       | Create or overwrite a file (prints a diff first)         |
| edit_file        | Surgical find-and-replace (old_string must be unique)    |
| list_directory   | List a directory                                         |
| run_command      | Execute a shell command (requires y/n approval)          |
| get_status       | `git status --short`                                     |
| get_diff         | `git diff`                                               |
| add_files        | `git add <path>`                                         |
| commit_changes   | `git commit -m <message>`                                |
| push_changes     | `git push <remote> <branch>`                             |

All file/git operations are sandboxed to `--cwd` (or the current directory).
Paths outside the sandbox are rejected.

## Cost / billing

`gemini-2.5-flash` is on Gemini's free tier (limits roughly 10 RPM, 250 RPD).
You can only be billed if you've explicitly attached a billing account in
Google Cloud and exceed free quotas. Each turn the agent prints token usage so
you can see what it cost.

Tip: automatic function calling means one task can spawn many API calls (one
per tool round-trip). A 5-step task is ~5+ requests against your daily quota.
