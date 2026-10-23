# Refactor

Improve the code's structure while preserving its observable behavior. The coordinator delegates contract discovery, implementation, integration, review, and verification by default. As an executor, read your assignment in the host project's `.cache` in full, follow J Mode's context and result-handoff protocol, and perform only the assigned stages below. Do not spawn agents; return dependencies or needed follow-ups to the coordinator.

## 1. Capture the current contract

Inspect the affected execution path and callers. Identify the behavior that must stay unchanged, including relevant outputs, errors, side effects, and compatibility requirements.

Run a baseline before moving the code. Use existing coverage, a focused characterization test, a snapshot, an equivalence check, or a repeatable runtime exercise that captures the contract. Choose a check that can detect a behavioral difference; compilation and linting alone are insufficient. Record the exact checks, inputs, and outputs for implementation and verification workers. If the contract cannot be checked, report the gap to the coordinator before making a structural change that depends on it.

## 2. Name the structural improvement

State what is difficult to follow today and what the target structure will make simpler. Identify the intended module boundaries, data shapes, and call relationships. Inspect callers before reshaping an interface.

Prefer an improvement that removes unnecessary branching, duplicated assumptions, hidden state, or layers. Keep an already clear structure when a proposed abstraction would only add indirection.

## 3. Plan small, verifiable moves

Break the work into steps that keep the behavior checks passing. Remove code proven to be unused when that simplifies the move. Keep behavioral changes separate from the structural goal; a newly discovered defect is a finding, not automatic permission to fix it.

Return proposed boundaries, prerequisite work, and coupled files or symbols to the coordinator when they affect later assignments. The coordinator sequences workers and serializes overlapping edits through J Mode's context-before-dispatch rules. Stay within your assigned file ownership and preserved contract.

## 4. Reshape and migrate callers

Apply the smallest change that reaches the target structure, checking the contract after each meaningful step. For an internal API change, migrate its in-scope callers together and remove the obsolete entry point when nothing still needs it. Preserve required external compatibility.

Check usages in imports, exports, configuration, strings, documentation, and other references relevant to the move. Confirm renames against actual files rather than assuming a mechanical edit reached every consumer. When assigned integration or review, inspect the relevant changes and dependency reports before combining them, and return any remaining gap to the coordinator.

## 5. Prove equivalence

Rerun the baseline checks against the changed code and exercise the relevant consumer-facing path. For a larger reshape, compare old and new outputs or replay recorded inputs against the new structure. Run nearby checks and review the final diff for accidental behavior changes.

Assess whether the result meets the stated structural goal with a simpler ownership model or execution path. Remove speculative changes that do not contribute to that goal. Name any unverified part of the contract instead of claiming complete equivalence. Return the baseline comparison and actual results for any separately assigned verification; the coordinator does not repeat these checks.

## 6. Report the result

Append the required `Result` section to your context file and send the same essential result to the coordinator. Describe the structural change, what became easier to understand, the contract held constant, and the evidence that it still holds. Include caller migrations, compatibility constraints, and any remaining limitation, together with J Mode's common handoff fields: assignment/context identity, status, files changed, exact actions and actual results, acceptance outcomes, and remaining dependencies. The coordinator summarizes the result for the user. Follow the user's requested delivery workflow only within your assignment.
