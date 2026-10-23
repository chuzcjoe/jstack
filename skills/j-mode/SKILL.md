---
name: j-mode
description: J's engineering workflow for bug fixes, feature development, read-only investigation, and behavior-preserving refactoring. Use for /j-mode or requests to work in J Mode.
---

# J Mode

J's standalone engineering workflow. The main agent coordinates work: it selects and sequences playbooks, prepares assignments, delegates execution, collects results, assigns follow-ups, and summarizes the outcome. Subagents perform investigation, design, reproduction, code changes, tests, review, and verification by default, including for small tasks.

## Working rules

- Assign executors to understand the affected path before editing: the caller, relevant data shape, and expected behavior.
- Require the smallest change supported by evidence. Reuse existing project structures and keep unrelated cleanup out of the task.
- Require observations to be distinguished from hypotheses. For defects, fix the source of incorrect behavior; add a guard only when the state it handles is legitimate.
- Require evidence that establishes the requested outcome. A conclusion without the underlying commands, actions, and actual results is insufficient; compilation and linting alone do not establish runtime behavior.
- The coordinator may inspect workspace metadata and instructions to prepare assignments. Delegate domain work, including review and final checks; do not quietly perform it in the main conversation.
- If delegation is unavailable or explicitly disallowed, report the limitation instead of silently switching to direct execution. The user can explicitly request direct execution.
- Keep work within the user's request and existing authorization. This mode does not itself authorize commits, PRs, merges, deployment, or messages to other people.
- Reply in the user's language. Summarize what changed, why, the actual verification evidence returned by executors, and any unresolved limit. Label inference and uncertainty; cite only evidence identified in the returned reports and do not claim to have run checks yourself.

## Subagents

### Roles and dispatch

Use the `j-agent` custom agent when registered with the host. Its shared instructions are maintained in `agents/j-agent.md` in the J Stack repository. `setup.sh` installs them in `.codex/agents/` with a TOML adapter for Codex, or `.claude/agents/` for Claude Code. If no registered `j-agent` is available, use a generic delegate whose assignment instructs it to read the absolute path to the shared role before working. If the role or delegation tools are unavailable, report the limitation. The delegate inherits the parent's model settings unless the host configuration or invocation overrides them, and can run in the background.

Use a fresh delegate without inherited conversation when supported. All required context must be in its assignment file even when conversation inheritance cannot be disabled. Executors perform only their assigned playbook stages and do not spawn agents or take over the coordinator's workflow.

### Resolve the host project

Resolve the task's project/worktree Git root from the assigned workspace, for example with `git -C <workspace> rev-parse --show-toplevel`. Do not derive it from the installed skill path, which may resolve inside a J Stack submodule or a different checkout. If starting inside the J Stack submodule, identify its owning superproject, for example with `git -C <j-stack-root> rev-parse --show-superproject-working-tree`, and use the host project's root. Standalone development of J Stack uses the J Stack repository root. For a non-Git workspace, use its explicitly assigned project root; resolve uncertainty before writing context.

All assignment and result bookkeeping belongs in `<project-root>/.cache/`. When J Stack is installed as a submodule, never place host task context in the submodule's `.cache`.

### Prepare context before every delegation

Use [references/subagent-context.md](references/subagent-context.md) as the assignment and result template. Before spawning each delegate, exclusively create a unique file at `<project-root>/.cache/j-mode-<run-id>-<agent-id>.md`; never overwrite an existing assignment. Distinct delegates, retries, and verification tasks each require a new file, even when reusing an existing worker. If a name collides, choose a new identifier.

Write all substantive instructions before dispatch, including:

- The original request and later constraints; absolute project, workspace, skill, shared-role, and selected-playbook paths.
- The full bounded task and assigned stages; relevant observed state and evidence separated from hypotheses; source and artifact pointers; dependency reports and decisions. Record unknowns honestly and assign discovery instead of guessing.
- Allowed actions, permitted edits, explicit file ownership, environment and reproduction/check instructions, acceptance criteria, and the required return format.

File references may carry source code and artifacts, but the assignment must be understandable without hidden conversation state. The spawn message only points to the absolute context-file path and instructs the delegate to read it fully before working. Treat the assignment portion as immutable after dispatch. Follow-ups receive new complete files with updated evidence and dependency reports.

For investigation-only requests, source code, project data, and external systems remain read-only for every worker. Explicitly allow assignment/result files under the host project's `.cache` as the sole bookkeeping exception.

### Collect results and coordinate follow-ups

Each executor appends a `Result` section to its own context file and sends the same essential result to the coordinator:

- Context path and assignment ID; status `completed`, `blocked`, or `inconclusive`.
- Findings and decisions; files changed, or `none`.
- Exact commands/actions and actual results, with evidence/artifact paths.
- Acceptance-criteria outcomes; remaining uncertainty and dependencies.

Check reports for the required evidence and coverage of the assigned criteria. Assign missing investigation, integration work, review, reproduction, or verification to workers through new context files. Delegate final checks too; the coordinator does not rerun tests, reproduce issues, or review code itself. Assign an independent review/verification worker when needed, especially when an implementation report leaves a consequential claim unconfirmed.

Parallelize read-only work and edits with disjoint ownership when useful. Serialize overlapping edits, and pass completed dependency reports to later workers. Keep the overall task list, playbook sequence, and final user response in the main conversation. Summarize only what the returned evidence supports, including any check that remains blocked or inconclusive.

## Playbooks

| Playbook | Use when | Instructions |
| --- | --- | --- |
| Bug Fix | Existing behavior is broken and needs to be reproduced, explained, and corrected. | [playbooks/bug-fix.md](playbooks/bug-fix.md) |
| Feature | The request adds or intentionally changes behavior. | [playbooks/feature.md](playbooks/feature.md) |
| Investigation | The requested result is a read-only explanation, diagnosis, or recommendation. | [playbooks/investigate.md](playbooks/investigate.md) |
| Refactor | The structure should change while observable behavior stays the same. | [playbooks/refactor.md](playbooks/refactor.md) |

Read the selected playbook in full before preparing assignments, and require executors to read it before performing their assigned stages. For multi-step work, keep a short task list and record the reason for any step that cannot be completed. Load additional playbooks only when the requested work needs them.

For mixed requests, sequence the relevant playbooks within the authorized scope. An investigation-only request does not authorize implementation. A request that already includes a change can proceed from investigation into that change without asking for the same authorization again.

If the request is too vague to select a playbook or begin useful work, inspect available metadata and instructions, delegate domain discovery where useful, and then ask only for the missing goal or expected behavior. For work outside these playbooks, follow the user's actual request using the same coordinator/executor split and context protocol.
