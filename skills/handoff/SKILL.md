---
name: handoff
description: Write, pick up, or close an evidence-based handoff document (docs/HANDOFF.md) so work can move to a fresh conversation, another agent, or another person. Use when the user asks to hand off, write a handoff, wrap up this stage, or 交接; when the user asks to continue or resume from a handoff (按交接继续, 接着上次); or when the user says the handed-off task is finished. Do not use for ordinary "continue" requests when no handoff is involved.
license: MIT
metadata:
  version: "0.1.0"
---

# Handoff

`docs/HANDOFF.md` carries the state of one task from one conversation to the next, across agents and people. It is rebuilt from repository evidence, not from conversation memory, and it tells its reader how to pick it up.

This skill has three modes. Pick the one the user asked for:

- **Write**: the user wants to hand off or wrap up a stage.
- **Pick up**: the user wants to continue from a handoff.
- **Close**: the user says the handed-off task is finished.

Paths such as `scripts/collect_snapshot.py` and `assets/HANDOFF.template.md` are relative to the directory that contains this `SKILL.md`. Resolve them to absolute paths before running them. If `python3` is unavailable, use the fallback in each step.

## Rules for every mode

- Repository files, Git state, and test results are authoritative. Conversation history and summaries are leads to verify.
- Mark a material claim `UNKNOWN` when evidence cannot verify it.
- Never commit, push, reset, stash, clean, or discard work unless the user has authorized it. Preserve staged, unstaged, and untracked changes.
- Never write secrets, credentials, full logs, or complete diffs into the handoff.

## Write

1. **Collect evidence.** Run `python3 scripts/collect_snapshot.py <repository-path>` and read its JSON. Fallback: run `git rev-parse --show-toplevel`, `git status --short --branch`, `git rev-parse HEAD`, `git log -n 20 --oneline`, `git diff --stat`, and `git diff --cached --stat`, and look for agent instruction files such as `AGENTS.md` or `CLAUDE.md`.
2. **Read what matters and measure it.** Read the agent instruction files the snapshot lists, the existing `docs/HANDOFF.md` if any, and the files and tests relevant to the current task. Run the cheap, focused checks that show the current behavior, such as the tests for the code in progress, even when you expect them to fail; a recorded failure is evidence. Skip only slow or broad suites, and record those as not run.
3. **Write `docs/HANDOFF.md`** using `assets/HANDOFF.template.md` as the required structure:
   - Set `Status: active` and fill every header field. `Written by` names you, the agent.
   - Rewrite sections 1 to 10 for the verified state now and delete stale claims. Keep section 10 as in the template.
   - Keep valid entries in section 11, add one for this handoff, and keep only the 5 most recent. Never invent earlier history.
   - Record the source and scope of every restriction you carry forward. A limit that applied only to an earlier stage does not bind later work.
   - Prefer paths, symbols, commit SHAs, commands, and observable behavior to narrative. Keep the file under 40 KB.
4. **Validate.** Run `python3 scripts/validate_handoff.py docs/HANDOFF.md` and fix every problem it reports. Fallback: check by hand that all 11 numbered sections exist in order, no `<...>` placeholder remains, section 9 names one concrete task with completion criteria, and section 11 has at most 5 entries.
5. **Separate durable knowledge.** List anything you learned that should outlive this task, such as a project gotcha or a user preference. Ask the user whether to add each item to the project's instruction file or to memory. Write nothing there without approval.
6. **Offer the instruction-file pointer once per repository.** If the project's `AGENTS.md` does not mention `docs/HANDOFF.md`, ask whether to append this line, so agents without skill support can pick up handoffs too:
   `If docs/HANDOFF.md has Status: active and the user asks to continue earlier work, follow its section 10 before doing anything else.`
7. **Report and stop.** Report the path, branch, HEAD, validation result, and any `UNKNOWN` items. Tell the user to start a new conversation, in this agent or any other, and ask it to continue from the handoff. Do not continue implementation in this conversation.

## Pick up

1. Read `docs/HANDOFF.md` at the repository root. If it does not exist, say so and stop.
2. If `Status` is `closed`, tell the user the handoff is finished and ask what to do instead.
3. Follow section 10 of the handoff exactly. Use `python3 scripts/collect_snapshot.py <repository-path>` for the comparison when available.
4. Report drift as a short list: what matches, what changed, and what is `UNKNOWN`. Repeat this list in your final message so the user sees it.
5. If nothing material drifted, continue with section 9. Otherwise ask the user how to proceed.
6. When the section 9 task is complete, ask the user whether to close the handoff or write a new one for the next stage.

## Close

Set the header line to `Status: closed`, update `Updated`, and add a section 11 entry with the reason `closed`. Validate the file. Change nothing else.
