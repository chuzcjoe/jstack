# J Stack

A minimal engineering workflow built around **J Mode**, with playbooks for **Bug Fix**, **Feature**, **Investigation**, and **Refactor**.

J Mode requires no additional workflow skills or specific models. By default, the main agent coordinates the work: it assigns bounded tasks to subagents, collects their results, and summarizes the outcome. Subagents perform investigation, design, implementation, testing, review, and verification.

## Install as a Submodule

From the root of the project that will use J Mode:

```sh
git submodule add git@github.com:chuzcjoe/jstack.git vendor/jstack
./vendor/jstack/setup.sh
```

The submodule can live at any path. `setup.sh` detects its Git superproject and configures that project's root, regardless of the directory you run it from. By default, it installs both **Codex** and **Claude Code** support.

Select one tool if needed:

```sh
./vendor/jstack/setup.sh --codex
./vendor/jstack/setup.sh --claude
```

For a standalone J Stack checkout, specify an existing target Git project:

```sh
./setup.sh --target /path/to/project
```

Setup requires Bash and Git. It creates relative symlinks to the submodule, so updating its contents updates the installed skill and agent instructions. It can be rerun safely. If a destination contains a different file, directory, or symlink, setup reports the conflict before creating any links.

| Tool | Entry in the host project | Submodule source |
| --- | --- | --- |
| Codex | `.agents/skills/j-mode` | `skills/j-mode/` |
| Codex | `.codex/agents/j-agent.toml` | `agents/j-agent.toml` |
| Codex | `.codex/agents/j-agent.md` | `agents/j-agent.md` |
| Claude Code | `.claude/skills/j-mode` | `skills/j-mode/` |
| Claude Code | `.claude/agents/j-agent.md` | `agents/j-agent.md` |

These paths follow the official [Codex skill](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills), [Codex subagent](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents), [Claude Code skill](https://code.claude.com/docs/en/skills#choose-where-skills-load), and [Claude Code subagent](https://code.claude.com/docs/en/sub-agents#choose-the-subagent-scope) configuration formats. Existing project settings and instruction files are preserved.

Commit `.gitmodules`, the submodule entry, and the generated symlinks in the host repository so other contributors receive the same setup. After cloning that repository, initialize its submodules:

```sh
git submodule update --init --recursive
```

Start a new Codex or Claude Code session in the host project after setup.

## Use J Mode

In Codex:

```text
$j-mode Fix this bug: deleting the last record leaves stale data in the list.
The list should show an empty state. Reproduce the failure, identify the root
cause, apply the smallest fix, and verify the result.
```

In Claude Code:

```text
/j-mode Fix this bug: deleting the last record leaves stale data in the list.
The list should show an empty state. Reproduce the failure, identify the root
cause, apply the smallest fix, and verify the result.
```

J Mode selects a playbook from the requested outcome. You can also name one explicitly:

```text
$j-mode Feature: add filtering by status to the records list.
$j-mode Investigate: explain how login sessions expire, without changing code.
$j-mode Refactor: simplify the session store while preserving its behavior.
```

For Claude Code, use `/j-mode` with the same requests.

## Coordinator and Delegates

[`agents/j-agent.md`](agents/j-agent.md) defines J Mode's shared delegate instructions. Claude Code loads that Markdown definition directly. Codex loads [`agents/j-agent.toml`](agents/j-agent.toml), which tells the delegate to read the shared instructions. Model selection follows the host's inherited settings and any explicit overrides.

The main agent selects and sequences the playbooks, prepares assignments, dispatches delegates, checks their reports for the required evidence, and assigns follow-ups for gaps. It may inspect workspace metadata and instructions to prepare those assignments; domain work and final verification are delegated.

Before **every** delegation, the main agent creates a complete, unique Markdown context file at `<project-root>/.cache/j-mode-<run-id>-<agent-id>.md`, using [`skills/j-mode/references/subagent-context.md`](skills/j-mode/references/subagent-context.md). Each worker, retry, and verification task gets its own file, created without overwriting an existing assignment. The assignment contains the original request and later constraints; absolute project, workspace, skill, shared-role, and playbook paths; the bounded task; observed evidence and open hypotheses; source and artifact pointers; dependency reports and decisions; file ownership and edit permissions; environment and check instructions; acceptance criteria; and the required return format. Unknown facts are assigned for discovery rather than guessed.

Resolve the host Git or worktree root from the assigned workspace, not the installed skill's path. If the workspace is inside the J Stack submodule, use its owning superproject. For example, with a host at `/path/to/Core` and J Stack installed at `/path/to/Core/jstack`, assignments belong in `/path/to/Core/.cache/`, such as `/path/to/Core/.cache/j-mode-20261023T040955Z-review.md`. Host task context must not go in `/path/to/Core/jstack/.cache/`. Standalone development of J Stack uses the J Stack repository's own `.cache/`.

Dispatch the registered `j-agent` when available, otherwise a generic delegate that reads the shared role. Use a fresh delegate without inherited conversation when supported. The spawn message only points to the context file's absolute path and tells the delegate to read it fully before working; all substantive instructions must already be in that file. Keep the assignment immutable after dispatch. Delegates execute only their assigned stages and do not spawn further agents. Independent tasks with disjoint ownership may run in parallel; overlapping edits are serialized.

Each delegate appends a **Result** section to its own context file and returns the same essential report to the main agent: context path and assignment ID; completed, blocked, or inconclusive status; findings and decisions; files changed; exact commands or actions and actual results with evidence paths; acceptance criteria outcomes; and remaining uncertainty or dependencies. The main agent collects these reports and delegates review, verification, and any follow-up work through new context files before summarizing the result to the user. An independent verification delegate is assigned when needed; the main agent does not rerun checks itself.

Investigation-only requests keep source code, project data, and external systems read-only. The `.cache/` assignment and result files are the sole bookkeeping exception.

Setup registers the custom agent without changing the host's delegation permissions or settings. If delegation is unavailable or explicitly disallowed, J Mode reports that limitation instead of silently switching to direct execution. The user can explicitly request direct execution.

## Playbooks

| Playbook | Workflow |
| --- | --- |
| [Bug Fix](skills/j-mode/playbooks/bug-fix.md) | Reproduce the failure, establish its cause, apply a minimal fix, and verify the original behavior. |
| [Feature](skills/j-mode/playbooks/feature.md) | Define the outcome, choose the data and interface shape, implement in verifiable units, and check the user-visible result. |
| [Investigation](skills/j-mode/playbooks/investigate.md) | Trace evidence and answer a question or recommend an approach without changing source code, project data, or external state. |
| [Refactor](skills/j-mode/playbooks/refactor.md) | Capture the current contract, improve the structure in small steps, and prove behavior is preserved. |

Commits, pull requests, and other delivery actions follow the user's request and the project's existing workflow.

## Structure

```text
agents/
  j-agent.md                 # Shared instructions and Claude Code agent
  j-agent.toml               # Codex agent adapter
skills/
  j-mode/
    SKILL.md                 # Entry point and engineering rules
    playbooks/
      bug-fix.md             # Reproduce and fix a defect
      feature.md             # Build new or changed behavior
      investigate.md         # Answer a question with evidence
      refactor.md            # Improve structure while preserving behavior
    references/
      subagent-context.md    # Per-delegate assignment and result template
README.md
setup.sh                     # Configure the host project
tests/
  test_setup.py              # Submodule installation integration tests
```

## Customize

- Edit [`skills/j-mode/SKILL.md`](skills/j-mode/SKILL.md) to change J Mode's engineering rules.
- Edit the files under `skills/j-mode/playbooks/` to change an individual workflow.
- Edit [`agents/j-agent.md`](agents/j-agent.md) to change the delegate's instructions.
- Edit [`skills/j-mode/references/subagent-context.md`](skills/j-mode/references/subagent-context.md) to change the complete assignment and result template used before each delegation.

## Test Setup

With Python 3.11 or later and Git installed:

```sh
python3 -B -m unittest discover -s tests -v
```

The tests create temporary local Git repositories and real submodules. They cover tool selection, root detection, relative links, submodule updates, repeated setup, and preservation of existing project files. No network access is needed.
