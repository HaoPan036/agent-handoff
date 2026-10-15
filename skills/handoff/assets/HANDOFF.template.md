# Handoff

Status: `active`
Updated: `<ISO-8601 local timestamp>`
Workspace: `<absolute workspace path>`
Branch: `<branch or N/A>`
HEAD: `<full or short commit SHA or N/A>`
Handoff reason: `<milestone boundary, long session, switching agents, manual request, or other>`
Written by: `<agent or person>`

> **Picking this up?** Follow section 10 before doing anything else. Repository evidence wins over this document.

## 1. Objective and scope

### Objective

`<Current outcome being pursued>`

### In scope

`<Exact work included>`

### Out of scope

`<Explicit non-goals>`

## 2. Verified current state

### Completed

`<Observable completed work with paths, symbols, behavior, and commit SHAs>`

### In progress

`<Partially completed work and exact current boundary>`

### Remaining

`<Work that has not been completed>`

## 3. Architecture and data flow

`<Current components, control flow, data flow, interfaces, schemas, and key dependencies>`

## 4. Decisions, constraints, and rejected approaches

### Decisions and reasons

`<Decision, reason, and evidence>`

### Invariants and constraints

`<Rules that future work must preserve, with source and applicable task/stage; distinguish enduring user/project rules from temporary handoff limits and historical outcomes>`

### Rejected approaches

`<Approach and reason it was rejected>`

## 5. Relevant files and symbols

`<Path, symbol, role, and current status>`

## 6. Verification

### Commands run

`<Exact command and result>`

### Checks not run

`<Important check not run and reason>`

## 7. Working tree

### Staged changes

`<Summary or none>`

### Unstaged changes

`<Summary or none>`

### Untracked files

`<Summary or none>`

## 8. Known issues, risks, and unknowns

`<Failure, risk, edge case, or UNKNOWN claim with evidence needed>`

## 9. Next concrete task

`<One bounded, executable task with expected files and completion criteria>`

## 10. New-session startup checklist

1. If `Status` is `closed`, stop and tell the user this handoff is finished.
2. Read the project's agent instruction files, such as `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or `.cursor/rules/`.
3. Read this handoff completely.
4. Compare branch, HEAD, and working tree with the header and section 7. Rerun the cheap, focused checks from section 6.
5. Report drift to the user: what still matches, what changed, and what is `UNKNOWN`. Resolve conflicts in favor of repository evidence.
6. If nothing material drifted, continue with section 9. Otherwise ask the user how to proceed.

## 11. Handoff history

### `<ISO-8601 local timestamp>`

- Reason: `<why this handoff was created>`
- Branch / HEAD: `<branch> / <SHA>`
- Key progress since previous handoff: `<1 to 4 concise verified items>`
- Next task: `<one concise task>`
