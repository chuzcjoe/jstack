# J Stack

A minimal engineering workflow adapted from [P Stack](https://github.com/cursor/plugins/tree/main/pstack). J Stack currently includes one skill, **J Mode**, with a single **Bug Fix** playbook.

J Mode works independently and requires no additional P Stack skills or specific models. An optional **J Agent** can handle delegated investigation, implementation, or verification tasks.

## Usage

Copy `skills/j-mode` into your project's skills directory. From the root of this repository, run the following commands, replacing `/path/to/your-project` with your project path:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R skills/j-mode /path/to/your-project/.agents/skills/
```

In an agent that supports `/j-mode`, describe the defect and expected behavior:

```text
/j-mode Fix this bug: deleting the last record leaves stale data in the list.
The list should show an empty state. Reproduce the failure, identify the root
cause, apply the smallest fix, and verify the result.
```

## Optional Subagent

[`agents/j-agent.md`](agents/j-agent.md) defines J Mode's delegate, adapted from P Stack's [Poteto Agent](https://github.com/cursor/plugins/blob/main/pstack/agents/poteto-agent.md). It inherits the parent model and runs in the background. The parent agent coordinates the workflow, reviews delegated work, and performs final verification.

For Cursor, install the agent alongside the skill using its [custom subagent directory](https://cursor.com/docs/subagents#file-locations):

```sh
mkdir -p /path/to/your-project/.cursor/agents
cp agents/j-agent.md /path/to/your-project/.cursor/agents/
```

Copying the skill alone does not register the custom agent. Other hosts may require their own registration. J Mode can use a generic delegate that reads the J Agent instructions, or work directly when delegation is unavailable.

For example:

```text
/j-mode Use j-agent to investigate why deleting the last record leaves stale
data. Review its evidence, apply the fix, and verify the original reproduction.
```

Each delegate receives the exact J Mode skill path, workspace, task boundary, relevant evidence, and acceptance criteria. It reads the skill and Bug Fix playbook, completes its assigned part, and reports results to the parent.

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
  j-agent.md                 # Delegate instructions for J Mode
skills/
  j-mode/
    SKILL.md                 # Entry point and engineering rules
    playbooks/
      bug-fix.md             # The only playbook currently included
README.md
```

## Customize

- Edit [`skills/j-mode/SKILL.md`](skills/j-mode/SKILL.md) to change J Mode's engineering rules.
- Edit [`skills/j-mode/playbooks/bug-fix.md`](skills/j-mode/playbooks/bug-fix.md) to change the Bug Fix workflow.
- Edit [`agents/j-agent.md`](agents/j-agent.md) to change the delegate's instructions.
