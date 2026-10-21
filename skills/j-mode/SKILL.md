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
- Work directly by default. Use delegation only when it is available, authorized, and useful. No specific model or agent type is required.
- Keep work within the user's request and existing authorization. This mode does not itself authorize commits, PRs, merges, deployment, or messages to other people.
- Reply in the user's language. State what changed, why, the actual verification result, and any unresolved limit. Label inference and uncertainty. Cite only artifacts you inspected or produced.

## Bug Fix

For a reported defect, read [playbooks/bug-fix.md](playbooks/bug-fix.md) in full and follow it. Keep one short task list for the playbook, recording an explicit reason when a step cannot be completed.

If invoked without a defect or enough context to start investigating, ask for the failing behavior, expected behavior, and any reproduction details that are missing. Inspect available repository and task context before asking for information already present.

For a request outside bug fixing, explain that J Mode currently supports Bug Fix only. Follow the user's actual request using the working rules above, without inventing additional playbooks or reclassifying a feature as a defect.
