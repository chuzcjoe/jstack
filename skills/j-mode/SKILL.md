---
name: j-mode
description: J's bug-fixing workflow. Use for /j-mode or requests to fix a reported defect in J Mode, from reproduction and root-cause evidence through a minimal fix and verification.
---

# J Mode

J's standalone engineering workflow. The only playbook currently supported is **Bug Fix**.

## Working rules

- Understand the affected path before editing. Identify the caller, the relevant data shape, and the behavior the user expects.
- Prefer the smallest change supported by evidence. Reuse existing project structures and keep unrelated cleanup out of the fix.
- Distinguish observations from hypotheses. Fix the source of incorrect behavior; add a guard only when the state it handles is legitimate.
- Verify observable behavior. Compilation, linting, and another agent's report alone do not establish that the reported problem is solved.
- Work directly by default. Use delegation only when it is available, authorized, and useful, following the Subagents section below.
- Keep work within the user's request and existing authorization. This mode does not itself authorize commits, PRs, merges, deployment, or messages to other people.
- Reply in the user's language. State what changed, why, the actual verification result, and any unresolved limit. Label inference and uncertainty. Cite only artifacts you inspected or produced.

## Subagents

For delegated investigation, implementation, or verification, use the `j-agent` custom agent when it is registered with the host. Its shared instructions are maintained in `agents/j-agent.md` in the J Stack repository. `setup.sh` installs them in `.codex/agents/` with a TOML adapter for Codex, or `.claude/agents/` for Claude Code. The delegate inherits the parent's model settings unless the host configuration or invocation overrides them, and can run in the background.

Each assignment must include the absolute path to this `SKILL.md`, the workspace, the bug and relevant evidence, the specific subtask and acceptance criteria, and whether edits are allowed. Give implementation delegates explicit file ownership. Use a fresh delegate for a new subtask; reuse one only when the assignment depends on its existing work or a process it still runs.

Keep the full playbook, task list, and final response in the parent conversation. Parallelize independent investigations when useful, and serialize edits to overlapping files. Review delegated changes and rerun the original reproduction yourself before reporting a verified fix.

If the host supports generic delegates but no registered `j-agent`, locate the installed `j-agent.md` and pass its absolute path with an instruction to read it before working. If the role file or delegation tools are unavailable, complete the task directly. Delegates must not spawn further agents.

## Bug Fix

For a reported defect, read [playbooks/bug-fix.md](playbooks/bug-fix.md) in full and follow it. Keep one short task list for the playbook, recording an explicit reason when a step cannot be completed.

If invoked without a defect or enough context to start investigating, ask for the failing behavior, expected behavior, and any reproduction details that are missing. Inspect available repository and task context before asking for information already present.

For a request outside bug fixing, explain that J Mode currently supports Bug Fix only. Follow the user's actual request using the working rules above, without inventing additional playbooks or reclassifying a feature as a defect.
