# Investigation

Answer a question with evidence. The coordinator delegates this playbook's domain work by default. As an executor, read your assignment in the host project's `.cache` in full, follow J Mode's context and result-handoff protocol, and perform only the assigned stages below. Do not spawn agents; return dependencies or needed follow-ups to the coordinator.

This playbook keeps source code, project data, and external systems read-only. Assignment and result files under the host project's `.cache` are the sole bookkeeping exception. Its result is an explanation, diagnosis, or recommendation.

## 1. Frame the question

Identify the question to answer and the boundary of the investigation. Distinguish questions about current behavior from questions about historical intent or a choice between alternatives. Inspect available context before reporting missing information to the coordinator.

## 2. Gather the relevant evidence

Trace the actual entry points, data flow, state transitions, configuration, and callers involved. Use repository history and available records when the question concerns why a decision was made. A plausible explanation from the current code does not establish historical intent.

Inspect the decisive evidence directly within your assigned scope. A prior worker's conclusion is a lead rather than a substitute for that evidence. The coordinator may assign independent read-only investigations or verification in parallel through separate context files; executors return findings and evidence without dispatching work themselves.

## 3. Test the explanation

List the plausible explanations and look for evidence that distinguishes them. Use read-only inspection and existing diagnostics that preserve project files and application data. Update the explanation when observations contradict it.

Do not edit source, add instrumentation to the project, or mutate external systems as part of an investigation-only request. Write only the permitted `.cache` bookkeeping files. If an experiment requires a project or external-system change, explain what it would establish and identify the remaining uncertainty for the coordinator. Do not present an unrun experiment as evidence.

## 4. Form the answer

Lead with the answer or recommendation, then explain how the evidence supports it. For a subsystem walkthrough, cover the key concepts, execution path, relevant file locations, and important constraints. For a decision, compare the meaningful alternatives and state the tradeoff behind the recommendation.

Separate observed facts, inferences, and unknowns. If the premise is contradicted by the evidence, say so and explain why. Use only file references, links, and results you actually inspected.

## 5. Report and preserve scope

Append the required `Result` section to your context file and send the same essential result to the coordinator, with the answer, concise supporting evidence, and unresolved questions. Include J Mode's common handoff fields: assignment/context identity, status, files changed (normally `none` apart from the result file), exact read-only actions and actual results, acceptance outcomes, and remaining uncertainty or dependencies. The coordinator summarizes the findings for the user and assigns any missing verification; it does not repeat the investigation itself. A finding does not by itself authorize a fix or refactor.

If the original request also asks for implementation, return the findings so the coordinator can assign the appropriate Bug Fix, Feature, or Refactor stages with explicit edit permissions. Otherwise, describe any proposed change as a recommendation and finish the investigation.
