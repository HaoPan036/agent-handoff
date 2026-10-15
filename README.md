# agent-handoff

Hand a coding task from one conversation to the next — across Claude Code, Codex, Cursor, or any agent that can read a file — without losing what matters.

Say "hand off" (or 交接). The agent rebuilds the task's state from the repository — Git, the files and tests that matter, your project's agent instructions — and writes `docs/HANDOFF.md`. Open a new conversation in any agent and say "continue from the handoff". The new agent checks the document against the repository, reports what changed, and continues with the one next task.

```text
agent A ── "hand off" ──▶ docs/HANDOFF.md ── new conversation, any agent ── "continue" ──▶ verified pickup
```

## Why not just compact?

Compaction summarizes a conversation so the same agent can keep going. A handoff is different:

| | Compaction | Handoff |
| --- | --- | --- |
| Built from | The conversation | Repository evidence; the conversation is only a lead |
| Lives in | The agent's session | A Markdown file you can read, edit, diff, and commit |
| Works across | One session in one tool | Sessions, machines, agents, and people |
| On pickup | Nothing is rechecked | Branch, HEAD, working tree, and focused tests are compared first |

Use compaction to keep going inside one task. Use a handoff at a boundary: a finished stage, a cluttered context, an overnight pause, or a switch to another agent.

## Three levels of support

1. **Any agent, no install.** The handoff file explains how to pick it up. Ask any agent to "read docs/HANDOFF.md and continue".
2. **Agents that support [Agent Skills](https://agentskills.io).** Install the `handoff` skill and use plain language to write, pick up, or close a handoff.
3. **Session-start hooks** (planned). Agents with hooks will mention an active handoff automatically in each new conversation.

## Install

Requires `git` and `python3` 3.9 or later. Python is optional at use time; without it the skill falls back to plain Git commands and a manual checklist.

```bash
git clone https://github.com/HaoPan036/agent-handoff.git
cd agent-handoff
python3 install.py
```

The installer symlinks the skill into `~/.agents/skills/` (read by Codex, Cursor, Gemini CLI, and other Agent Skills clients) and into `~/.claude/skills/` when Claude Code is installed. `git pull` then updates every agent at once. It never overwrites a skill it did not create. Remove the links with `python3 install.py --uninstall`.

For an agent that reads skills from another folder, symlink `skills/handoff` there yourself.

### Tested with

| Agent | Status |
| --- | --- |
| Codex CLI 0.160.1 | Write, pick up (with drift), and close, end to end |
| Claude Code | Skill discovery verified; full flow not yet run in a fresh session |
| Cursor and other Agent Skills clients | Expected to work per the standard; not tested |

Reports from other agents are welcome.

## Use

| Say | What happens |
| --- | --- |
| "hand off" / "交接" | Writes and validates `docs/HANDOFF.md`, asks about durable lessons, then tells you to start a new conversation |
| "continue from the handoff" / "按交接继续" | Checks the handoff against the repository, reports drift, continues with its next task |
| "the handoff task is done" | Marks the handoff `Status: closed` |

The first time you hand off in a repository, the skill offers to add one line to `AGENTS.md`, so agents without skill support can pick up handoffs too.

## The handoff document

Eleven fixed sections: objective and scope, verified state, architecture, decisions and rejected approaches, relevant files, verification commands and results, working tree, risks and unknowns, **one next concrete task**, the pickup checklist, and the last five handoffs. See [the example](examples/HANDOFF.example.md).

The validator rejects a missing status, missing or reordered sections, leftover placeholders, a vague next task, more than five history entries, and files over 40 KB.

## Safety

While writing a handoff the agent changes only `docs/HANDOFF.md`, plus `AGENTS.md`, memory, or instruction files when you approve. It never commits, pushes, resets, stashes, or discards your work. Facts it cannot verify are marked `UNKNOWN`.

## Development

```bash
python3 -m unittest discover -s tests
```

## License

MIT
