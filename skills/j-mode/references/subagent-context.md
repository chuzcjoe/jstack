# Subagent context template

The coordinator completes the assignment below before every dispatch, including retries, reviews, and verification. Resolve the task's host/worktree Git root from its assigned workspace, never from the installed skill's location. If starting inside the J Stack submodule, identify its owning superproject and use that host project's root. Standalone J Stack development uses this repository's root. Record the root-resolution evidence in the assignment.

Create `<project-root>/.cache/` if needed, then exclusively create a unique `j-mode-<run-id>-<agent-id>.md` inside it; fail on an existing file instead of overwriting it. Every delegate gets a separate file, even when retrying a related task. Never put host-project context in the J Stack submodule. The template is guidance, not a new executable helper or a request to change a host project's ignore rules.

Replace the placeholders and include every substantive instruction before dispatch. State unknown facts honestly and assign discovery when appropriate. Source and artifact pointers may refer to files, but required task instructions must not depend on inherited conversation. Use a fresh delegate without inherited conversation when supported. Dispatch to registered `j-agent`, or a generic delegate that reads the shared role; the spawn message only points to the absolute context path and tells the delegate to read it in full. If delegation is unavailable or explicitly disallowed, report the limitation rather than silently executing the task as coordinator. The user may explicitly request direct execution.

The assignment is immutable after dispatch. The delegate executes the bounded task directly, appends its own `## Result`, and returns the same essential report to the coordinator. Pass new decisions and dependency reports to follow-up workers through a new complete context file. Serialize overlapping edit ownership; read-only tasks and disjoint edits may run in parallel. Delegate review and verification too; the coordinator checks reports for completeness and assigns independent verification when needed.

## Assignment template

```markdown
# J Mode delegate assignment

## Identity and paths
- Assignment ID: <run-id>-<agent-id>
- Context file: <absolute project-root/.cache/j-mode-run-id-agent-id.md>
- Host/worktree project root: <absolute path>
- Assigned workspace: <absolute path>
- Root-resolution evidence: <workspace Git root and owning superproject, or standalone root; commands/observations used>
- J Mode skill: <absolute path to SKILL.md>
- Shared delegate role: <absolute path to agents/j-agent.md or its installed link>
- Selected playbook(s): <absolute paths, in order>

## Original request and constraints
<Original user request, later corrections and constraints, and authorization relevant to this task. Include investigation-only restrictions and explicit direct-execution exceptions when applicable.>

## Roles and startup
Read this entire file before doing any task work. Then read the shared delegate role, J Mode skill, selected playbooks, and applicable repository instructions at the supplied paths.

You are the executor for this bounded assignment. The parent selects and sequences playbooks, writes context, dispatches workers, collects evidence, assigns follow-ups, and summarizes results. Execute the assigned stages directly; do not recursively dispatch, spawn further agents, or run the parent's whole workflow.

If required context or a supplied instruction path is absent, unreadable, or insufficient to begin safely, report blocked. Do not guess or recover instructions from inherited chat. Explicitly unknown facts below are discovery work only within the assigned scope.

## Bounded task
<Concrete outcome, assigned playbook stages, deliverables, exclusions, and conditions requiring a report to the parent before expanding scope.>

## Observed state and evidence
<Relevant existing behavior, workspace state, prior edits to preserve, reproduction evidence, and confirmed facts with source locations. Separate observations from hypotheses and identify unknown facts.>

## Source and artifact pointers
<Absolute paths and relevant locations for source, instructions, logs, inputs, fixtures, designs, or artifacts. State what each pointer establishes and which still need inspection. Include relevant evidence itself when access to a pointer is uncertain.>

## Dependencies and decisions
<Upstream report paths and their essential findings, interfaces/contracts already decided, prerequisites, parallel work, and unresolved dependencies. Use "none" where applicable.>

## Permissions and file ownership
<Whether edits are allowed; exact files/directories owned by this delegate; read-only boundaries; other agents' ownership; preservation requirements; external-action restrictions. Serialize overlapping edits.>

For investigation-only requests, source code, project data, and external systems remain read-only. Creating assignment context files and appending delegate results under the host project's .cache are the sole orchestration bookkeeping exception. Do not modify another delegate's context file or the assignment portion of this file.

## Environment, reproduction, and checks
<Relevant OS/runtime/tool versions or honest unknowns, working directory, setup already completed, concrete reproduction and verification actions, required project checks, evidence output locations, and unavailable access. Distinguish requested checks from checks already run with their actual results.>

## Acceptance criteria
1. <Observable criterion and the evidence required to assess it.>
2. <Additional criterion, including scope and preservation constraints.>

## Required return
Append a new `## Result` section to this file, preserving all assignment text above it. Send the same essential result to the parent. Include all of the following:

- Context file's absolute path and assignment ID.
- Status: completed, blocked, or inconclusive.
- Findings and decisions, distinguishing observations from hypotheses.
- Files changed, or explicitly none.
- Exact commands/actions actually performed, actual results, and evidence/artifact paths. Do not fabricate output or claim unrun checks.
- Outcome for each acceptance criterion, including skipped or inconclusive checks.
- Remaining uncertainty, missing access, dependencies, and required follow-up.

If appending fails, report that limitation and send the complete result to the parent directly. Stop after the assigned result; the parent issues any follow-up through a new context file.
```
