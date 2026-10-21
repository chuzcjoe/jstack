# J Stack

A minimal engineering workflow adapted from [P Stack](https://github.com/cursor/plugins/tree/main/pstack). J Stack currently includes one skill, **J Mode**, with a single **Bug Fix** playbook.

J Mode works independently and requires no additional P Stack skills or specific models. An optional **J Agent** can handle delegated investigation, implementation, or verification tasks.

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

## Optional Delegation

[`agents/j-agent.md`](agents/j-agent.md) defines J Mode's shared delegate instructions, adapted from P Stack's [Poteto Agent](https://github.com/cursor/plugins/blob/main/pstack/agents/poteto-agent.md). Claude Code loads that Markdown definition directly. Codex loads [`agents/j-agent.toml`](agents/j-agent.toml), which tells the delegate to read the shared instructions. Model selection follows the host's inherited settings and any explicit overrides.

Ask J Mode to use `j-agent` for a focused investigation, implementation, or verification task when useful. Each delegate receives the exact J Mode skill path, workspace, task boundary, relevant evidence, and acceptance criteria. It reads the skill and Bug Fix playbook, completes its assigned part, and returns evidence. The parent agent coordinates the workflow, reviews delegated work, and performs final verification.

Setup registers the custom agent without changing the host's delegation permissions or settings. J Mode can work directly when delegation is unavailable.

## Bug Fix Workflow

1. **Reproduce.** Observe the failure in the affected interface or runtime. Record the expected and actual behavior.
2. **Find the root cause.** Test hypotheses against runtime evidence until the failure mechanism is established.
3. **Apply a minimal fix.** Make only the changes supported by the evidence. When a cheap regression test is available, observe it fail before applying the fix.
4. **Verify.** Repeat the original reproduction in the same environment, run relevant checks, and review the final diff.
5. **Report.** Explain the defect, root cause, fix, verification results, and any unresolved limitations.

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
      bug-fix.md             # The only playbook currently included
README.md
setup.sh                     # Configure the host project
tests/
  test_setup.py              # Submodule installation integration tests
```

## Customize

- Edit [`skills/j-mode/SKILL.md`](skills/j-mode/SKILL.md) to change J Mode's engineering rules.
- Edit [`skills/j-mode/playbooks/bug-fix.md`](skills/j-mode/playbooks/bug-fix.md) to change the Bug Fix workflow.
- Edit [`agents/j-agent.md`](agents/j-agent.md) to change the delegate's instructions.

## Test Setup

With Python 3.11 or later and Git installed:

```sh
python3 -B -m unittest discover -s tests -v
```

The tests create temporary local Git repositories and real submodules. They cover tool selection, root detection, relative links, submodule updates, repeated setup, and preservation of existing project files. No network access is needed.
