# MATRIX-002: Perturbation recovery versus development, frozen protocol

**Study status:** implementer-authored synthetic diagnostic. The fixture in `fixtures/matrix_002_independent_v01.json` is a new four-scenario data set, not copied from MATRIX-001, and was committed before running this program. Neither correct actions nor human-like identity are adjudicated here. This is NOT a confirmatory human evaluation.

## Distinct, separable questions

1. **Perturbation recovery:** with a byte-identical checkpoint inside each controller profile, compare a transient large perturbation in affect to an unperturbed branch. Measure time-indexed field distance, action-score divergence, and whether the postperturbation deviation decays or persists. Return to the pre-event state is not inherently desirable under genuinely changed conditions.
2. **Adaptation versus rigidity:** from the same checkpoint, give three otherwise identical branches a forced, equal-budget action and repeated labeled consequence (+0.9, -0.9, 0). Compare the learned setpoint and held-out action-score trajectory. Different scores demonstrate responsiveness, **not** justified learning. Correctness must later be assessed by independent behavioral labels.
3. **Model complexity:** compare opt-in full architecture against removal of developmental state, neural field, regulator and a completely disabled learning/regulation control. Each profile gets its own baseline checkpoint. Cross-profile results are descriptive because the prelude generates different internal histories.

## Synthetic scenarios and fixed seeds

Four fresh scenario families: winter station, archive reclassification, hospital dilemma, mechanical inheritance. Fixed seeds: 7, 19, 41, 73, 101, 163, 227, 311. Eight seeds share each scenario's text and synthetic outcome choices; they are not independent people.

Each subject undergoes exactly the same source-admitted prelude *within each profile*, with an intention appropriate to the situation. The study uses only subject-owned synthetic witnessed observations. The checkpoint is created using SQLite's backup API and restored into five independent arms: unperturbed, perturbed, positive, negative and zero. Each restored arm must match the checkpoint SHA-256 and subject/config fingerprint. No renderer receives proprietary memory or tools.

For the recovery pair, the same external event ID and exact event text are observed; only admitted synthetic affect deltas differ. Afterwards, run fourteen matched endogenous wake/sleep cycles with the same phase and seed schedule. Record the full field and all action scores at each tick, not just the final choice.

For the adaptation trio, each arm receives the same four forced `investigate` decisions with otherwise identical permitted actions, observations and origin IDs. The **only difference** is the externally assigned numeric feedback. Immediately afterwards all arms receive four previously unseen cross-topic probes with the same schedule. Their labels do NOT specify a psychologically correct decision. The primary contrast is policy and slowly changing target response to equal information but opposite reward. This is not verified environmental feedback.

## Profiles, measures and expected controls

Profiles: `full`, `no_development`, `no_recurrent`, `no_regulator`, `frozen_control`. The frozen control disables both plastic developmental/recurrent systems and the classic target regulator; it may still have ordinary state response to new observations.

For each profile, scenario and seed, preserve five full case-level trajectories. Primary recovery measures: postshock field L1 versus unperturbed, end/peak ratio, fraction of matched selections changed, recovery curve across fourteen cycles. Primary learning measures: difference between positive and negative setpoints, positive/negative and positive/zero action-score L1 on held-out probes, count of differing selections, and any target change in the zero-control arm. Report zeroes and harmful effects without suppression. No reward source is independently verified.

**Falsification/integrity gates:** all five forked states must load from an identical checkpoint inside profile/case. Equal action eligibility and event order must be verified. No duplicate outcome admissions. Original source event and evidence hashes must remain sound. No Oracle proposal can be written as lived experience. Positive and negative feedback must not change a truly frozen policy branch except for explicitly identified residual channels. If a target or field drifts when zero reward should leave it fixed, report that drift as a weakness, not a success.

## No tuning against this fixture

The previous MATRIX-001 score/choice nulls and donor E4 reproduction gap remain binding. These tests are **diagnostic**, not a replacement for independent behavioral validation. After analyzing these results, any redesigned dynamics must be evaluated on newly frozen and independently adjudicated episodes. Do not tune hyperparameters on this fixture and then present the same fixture as confirmation.

## Reproduction

```bash
python -m unittest discover -s tests -v
python -m experiments.matrix_002 --output evidence/matrix_002_cases.json
```

The workflow should archive full case-level output and input hashes, not just aggregates. Documentation must state executed commit, exact GitHub Actions run, source fixture checksum and all limitations.
