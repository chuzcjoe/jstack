# Bug Fix

Every change should follow from evidence about the reported failure. A speculative safeguard is a hypothesis to test, rather than an automatic part of the fix.

The coordinator delegates this playbook's domain work by default. As an executor, read your assignment in the host project's `.cache` in full, follow J Mode's context and result-handoff protocol, and perform only the assigned stages below. Do not spawn agents; return dependencies or needed follow-ups to the coordinator.

## 1. Reproduce the failure

Establish the expected behavior and the actual failure. The assigned executor runs the reproduction on the surface where the bug occurs, such as the browser, CLI, API, or application runtime. Record the command or actions, relevant input and environment, and the observed failure for subsequent implementation and verification workers.

For intermittent bugs, tighten conditions or add temporary instrumentation within your edit permissions until you can observe the trigger. If access, credentials, or an unavailable environment prevents reproduction, report the specific limit and missing input or access to the coordinator. Continue independent investigation within your assignment, but keep the reproduction marked unverified.

## 2. Establish the root cause

Trace the affected path and inspect relevant regression history when available. Write the plausible hypotheses, then choose experiments that eliminate the most candidates. Inspect runtime state or add temporary logging when source inspection alone cannot distinguish them.

Confirm the surviving mechanism with an observation that connects the trigger to the failure. A successful experiment should explain both the incorrect state and how it becomes the reported symptom. When evidence contradicts a hypothesis, remove changes made solely for that hypothesis before trying another fix.

## 3. Make the smallest justified fix

State the mechanism and intended correction before editing. If the fix changes a function boundary, inspect callers, types, and ownership first. Correct the source of the invalid behavior using existing project conventions. Keep unrelated cleanup out of the change.

When a cheap, deterministic local regression test can express the defect, add it before the production fix and observe it fail for the expected reason. Assert behavior visible to the caller, rather than internal implementation details. Then apply the fix. If an automated test would be disproportionate or cannot represent the trigger, record why and retain a repeatable runtime reproduction instead.

## 4. Verify the original behavior

Rerun the same reproduction with the fix, using the same relevant inputs and environment. Confirm that the expected behavior now occurs, rather than merely that an error disappeared. If a regression test was added, run it again and observe it pass.

Run the relevant nearby checks and inspect the final diff for unintended behavior, temporary instrumentation, and speculative changes. Remove temporary debugging code before the final relevant verification. Investigate a failed check before broadening the test run. If review or verification is assigned to a separate worker, provide the reproduction, relevant inputs, and evidence paths needed to repeat it; the coordinator does not run it.

A unit test, build, or different-surface check alone does not close an original runtime reproduction. If the original surface remains inaccessible or inconclusive, report the fix as unverified on that surface and name the remaining check. Do not claim a confirmed runtime fix.

## 5. Report the result

Append the required `Result` section to your context file and send the same essential result to the coordinator, including:

- What was broken and its user-visible impact.
- The root cause and the evidence that established it, or the remaining hypothesis if unconfirmed.
- What changed and why it addresses the mechanism.
- The reproduction and verification results, including a short actual failing-then-passing output excerpt when available.
- Any skipped check, unresolved limitation, or remaining step.

Include the common handoff fields required by J Mode: assignment/context identity, status, files changed, exact actions and actual results, acceptance outcomes, and remaining dependencies. The coordinator uses these reports for the final user response. Never invent output. Do not open a PR or create commits merely because this playbook finished. If delivery was requested and assigned to you, follow that request and the repository's existing workflow.
