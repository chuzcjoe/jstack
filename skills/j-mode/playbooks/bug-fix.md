# Bug Fix

Adapted from P Stack's Bug Fix playbook for a standalone workflow.

Every change should follow from evidence about the reported failure. A speculative safeguard is a hypothesis to test, rather than an automatic part of the fix.

## 1. Reproduce the failure

Establish the expected behavior and the actual failure. Run the reproduction yourself on the surface where the bug occurs, such as the browser, CLI, API, or application runtime. Record the command or actions, relevant input and environment, and the observed failure.

For intermittent bugs, tighten conditions or add temporary instrumentation until you can observe the trigger. If access, credentials, or an unavailable environment prevents reproduction, state the specific limit and request only the missing information or access. Continue independent investigation, but keep the reproduction marked unverified.

## 2. Establish the root cause

Trace the affected path and inspect relevant regression history when available. Write the plausible hypotheses, then choose experiments that eliminate the most candidates. Inspect runtime state or add temporary logging when source inspection alone cannot distinguish them.

Confirm the surviving mechanism with an observation that connects the trigger to the failure. A successful experiment should explain both the incorrect state and how it becomes the reported symptom. When evidence contradicts a hypothesis, remove changes made solely for that hypothesis before trying another fix.

## 3. Make the smallest justified fix

State the mechanism and intended correction before editing. If the fix changes a function boundary, inspect callers, types, and ownership first. Correct the source of the invalid behavior using existing project conventions. Keep unrelated cleanup out of the change.

When a cheap, deterministic local regression test can express the defect, add it before the production fix and observe it fail for the expected reason. Assert behavior visible to the caller, rather than internal implementation details. Then apply the fix. If an automated test would be disproportionate or cannot represent the trigger, record why and retain a repeatable runtime reproduction instead.

## 4. Verify the original behavior

Rerun the same reproduction with the fix, using the same relevant inputs and environment. Confirm that the expected behavior now occurs, rather than merely that an error disappeared. If a regression test was added, run it again and observe it pass.

Run the relevant nearby checks and inspect the final diff for unintended behavior, temporary instrumentation, and speculative changes. Remove temporary debugging code before the final relevant verification. Investigate a failed check before broadening the test run.

A unit test, build, or different-surface check alone does not close an original runtime reproduction. If the original surface remains inaccessible or inconclusive, report the fix as unverified on that surface and name the remaining check. Do not claim a confirmed runtime fix.

## 5. Report the result

Reply concisely in the user's language with:

- What was broken and its user-visible impact.
- The root cause and the evidence that established it, or the remaining hypothesis if unconfirmed.
- What changed and why it addresses the mechanism.
- The reproduction and verification results, including a short actual failing-then-passing output excerpt when available.
- Any skipped check, unresolved limitation, or remaining step.

Never invent output. Do not open a PR or create commits merely because this playbook finished. If delivery was requested, follow that request and the repository's existing workflow.
