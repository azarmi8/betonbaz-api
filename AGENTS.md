# Agent Protocol

This repository follows MR Project OS v1.

## Mandatory startup
1. Read `PROJECT_STATE.md`.
2. Read `ACTIVE_TASK.md`.
3. Read `DECISIONS.md`.
4. Read `VERIFICATION.md`.
5. Inspect git status, branch and recent commits.
6. Inspect existing implementation before adding new code.

## Rules
- GitHub is the source of truth; local workspaces are disposable.
- Do not code before understanding the current state and active task.
- Reuse mature existing code/libraries before inventing replacements.
- Never claim DONE from an agent report alone; require reproducible evidence.
- Preserve existing behavior unless the active task explicitly changes it.
- Never invent missing data, credentials, tests, standards or production state.
- Record material decisions in DECISIONS.md.
- Record verification evidence in VERIFICATION.md.
- Update PROJECT_STATE.md and ACTIVE_TASK.md when the project state changes.
- Never commit secrets or credentials.

## Multi-device rule
A new device/agent must pull/fetch first and trust repository state files over local memory.

## Project
betonbaz-api
