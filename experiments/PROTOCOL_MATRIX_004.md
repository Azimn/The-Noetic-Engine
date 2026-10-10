# MATRIX-004 preregistration: world-consequence action learning

**Date frozen:** 2026-10-10. **Evidence class:** assistant-authored, deterministic simulated-world objective scoring. This study CAN test which mechanisms learn action values from external software consequence records. It CANNOT meet the independent-human-adjudication requirement in [MATRIX-004 issue #16](https://github.com/Azimn/The-Noetic-Engine/issues/16), prove good fictional character behavior, or close E4 neural donor/fresh-decoder.

## Questions and split

From a frozen fixture of 20 training situations and 10 distinct held-out transfer situations, with six fixed seeds, test whether the Noetic Engine can use correctly sourced reward/outcome information to select better actions than matched nonlearning controllers. No training adjustment may consult held-out gold labels. The world adjudicator is **deterministic, separate from the agent**, and takes world state and action only. It is neither an LLM judge nor a human annotator. All rules and labels are inspectable, and their engineering bias is a critical limitation.

Four observable event factors (binary and bounded) describe hazard, corroboration, distress and evidence gaps. Their authored text changes across train and held-out scenes but structured factor semantics do not. The cognitive controller is explicitly given the same four factor fields through a typed source-bound Observation; results therefore do not validate raw-language semantic parsing or memory understanding. No moral judgment or real-world danger is inferred.

## World rules and matched action intervention

The deterministic world returns the reward for actual policy candidates `investigate`, `comfort`, `protect`, `withdraw`, `defer` via a rule-driven loss table. Hazard with reliable corroboration prioritizes `protect`; uncertain hazard prioritizes `investigate`; distress without hazard prioritizes `comfort`; non-distress evidence gap prioritizes `investigate`; stable scenes prioritize `defer`. This is a deliberately simplified normative toy environment with explicit **ground truth only relative to those coded rules**. The policy may never read that rule or its selected correct action before acting.

Each learning profile receives the exact same (scene, action, consequence) training history by forcing each of five actions once on each of 20 training cases. After every forced action, a separate outcome observation provides a source origin and the environment-computed signed reward, then the cognition engine records the original decision's outcome against that origin. The replay ledger captures the features, selected action, source and reward; no undocumented state injection is permitted. All profiles have equal number of ticks, source records, scheduled action candidates, costs and seed order.

Test stage: 10 source-distinct held-out situations, five eligible actions each. The engine chooses, the external environment records correctness and regret, but feedback is **not** given to the engine until all test decisions are complete. This prevents evaluation-set learning. Also report a no-learning frozen policy, a source-matched non-neural signed learner, a non-neural learner without persistent intention, a full optional neural/developmental learner, a full learner with neural lesion, and a static heuristic baseline that receives the *same structured factors* (do not conceal that heuristic rules can solve the invented environment). A scripted world-rule oracle is listed as a **ceiling**, not an agent baseline.

## Mechanism

The optional `ConsequenceChoiceHead` is a source-associated, action-specific linear value adjustment, with a predeclared fixed feature transform and signed feedback eligibility. Its weights are separate from source memory and it changes only after a new admitted, subject-owned outcome observation referencing the earlier decision. The original recurrent field and controller keep contributing base scores. A non-neural `signed_only` profile isolates this value head from developmental/neural features. `frozen_no_learning` retains the same source history but cannot update values.

The head must be an actual audited part of the selected policy, not solely a prose renderer. The full allowed-action scores, original scores, signed features, intervention source, update magnitude, action margin and weight checksum are recorded. Baseline policy is identical with this feature flag disabled. Verified world-origin evidence in this simulation is **not cryptographic attestation** and cannot authorize autonomous production action.

## Primary measures

Predeclared: per-case correct selection versus the world-rule optimum; total regret/lost reward under the world rule; positive-feedback and negative-feedback causal update counts; held-out correct selection for each profile/seed; action flips relative to the source-matched frozen control; selection margin distributions; same-input deterministic rerun. Report per-category breakdown (confirmed hazard / unconfirmed hazard / distress / epistemic gap / stable), including negative cases. The study's only quality claim is **task performance relative to a fully disclosed toy scoring function**, never human-approved moral or identity quality.

## Confounds and stop rules

- Structured environmental features are supplied by the fixture. The system is NOT learning language understanding.
- The adjudicator's rule and the feature transform come from the same author's world design. Overperformance can be due to handcrafted inductive structure or a rule-aligned static policy.
- The author may not tweak parameters on this frozen fixture and then claim replication on the same fixture. Any fixes for runtime correctness must be distinguished from hyperparameter/design selection.
- An Egregore belief record from hearsay, Oracle speculation, a source-swapped diary or a forged review **cannot** update a consequence value. No world results ever imply actual private mental states or supernatural causation.
- A declined/admitted or zero reward must remain visible. No retrospective relabeling of source observations, reward values or selected actions.
- The test stage must not train on its own answers, use LLM renderer-generated facts, silently skip wrong answers or use a secret action key.
- E4 fresh-decoder donor provenance and official NoeticBrainAdapter reviews remain OPEN.

## Execution

```sh
python -m unittest discover -s tests -v
python -m experiments.matrix_004 --output evidence/matrix_004_cases.json
```

CI archives both an unabridged, compressed per-case experiment ledger and the source/fixture checksum. An independent human-labeled fictional-action battery remains a separately required later stage even if software-world correctness improves.
