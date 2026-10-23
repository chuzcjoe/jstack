# Feature

Build the requested behavior from a clear contract and verify it where its users will experience it. The coordinator delegates design, implementation, integration, review, and verification by default. As an executor, read your assignment in the host project's `.cache` in full, follow J Mode's context and result-handoff protocol, and perform only the assigned stages below. Do not spawn agents; return dependencies or needed follow-ups to the coordinator.

## 1. Define the outcome

Identify who uses the feature, what they can do afterward, and the observable acceptance criteria. Inspect the affected entry points, callers, existing behavior, and relevant project conventions before choosing an implementation.

Resolve factual uncertainty from the code or a focused experiment. Report a missing product decision to the coordinator only when the intended behavior cannot be inferred from the request or available context. Keep optional ideas outside the agreed scope.

## 2. Choose the shape

Name the inputs, outputs, state, and responsibilities before writing logic. Prefer the project's existing structures. When a change crosses module or function boundaries, inspect the callers and settle the ownership and interface first.

Compare alternatives when they have a meaningful effect on behavior, complexity, or maintenance. Use a small experiment when it can settle the choice, and record the reason for the chosen design. Scale this work to the feature rather than adding a design exercise to a straightforward edit.

## 3. Sequence the work

Propose units that can each be checked. Identify prerequisites, independent workstreams, shared mutable state, and ownership needed for coupled changes. Return the proposal and interface decisions to the coordinator when they affect later assignments. Within your bounded assignment, complete blocking work first.

The coordinator sequences workers using these reports and the main skill's context-before-dispatch rules. Execute only your assigned work and file ownership; report any need to expand them before making overlapping edits.

## 4. Implement and integrate

Make the smallest complete change that meets the acceptance criteria. Update the affected callers and configuration, and follow the repository's established error-handling and compatibility requirements. Keep speculative abstractions and unrelated cleanup out of the change.

Add behavior-level coverage when there is a practical test path. Assert what the consumer observes, including meaningful failure cases. When assigned integration or review, inspect the relevant changes and dependency reports before combining the feature, and record any remaining gap for the coordinator.

## 5. Verify the result

Exercise the feature on the relevant interface or runtime using representative inputs. Check the acceptance criteria and nearby behavior that the change could affect. Run the relevant project checks and inspect the final diff.

A successful build alone does not demonstrate that the feature works. If runtime access is unavailable or a check is inconclusive, distinguish what was verified from what remains unverified. Return commands, representative inputs, actual outputs, and evidence paths so another assigned worker can verify the result; the coordinator does not rerun checks.

## 6. Report the result

Append the required `Result` section to your context file and send the same essential result to the coordinator. Explain what the user can now do, the main design choice and its tradeoffs, and the actual verification results. Include J Mode's common handoff fields: assignment/context identity, status, files changed, exact actions and actual results, acceptance outcomes, and remaining uncertainty or dependencies. The coordinator summarizes the result for the user. Follow the user's requested delivery workflow only within your assignment.
