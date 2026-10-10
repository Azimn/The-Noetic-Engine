# Empirical appendix B: Outcome-Driven Decision Learning (MATRIX-004)

**Status:** executed synthetic environment diagnostic, 2026-10-10. **Not independently peer reviewed.**
**Source:** `experiments/PROTOCOL_MATRIX_004.md`, `results/MATRIX_004_RESULTS.md`, `results/matrix_004/cases.json.gz`.
**First successful execution:** SHA `16c1ce27c8e3c5ee0989e95e8fbc73cdce875dff`, [GitHub Actions 38058384913](https://github.com/Azimn/The-Noetic-Engine/actions/runs/38058384913). Frozen fixture SHA-256 `d691a6e66d2f22d71b53d7151e264669b3e0cbfa091c943fd68f049113fc1b0e`.

## Research problem and method

The prior three matrices established measurable policy effects from intentions and regulation, and source-dependent field recovery after explicitly expiring environmental pressure, but not consequence-dependent correct action change. MATRIX-004 introduced a feature-gated, source-associated **linear action-value head** receiving four structured fictional-world facts and a deterministic external world-rule outcome. This is engineering evidence that a derived policy can incorporate past consequences; it is NOT a trained general-intelligence faculty or model of personal values.

The test contains twenty training and ten held-out author-generated world states. The five admissible actions are investigate, comfort, protect, withdraw and defer. Each tested profile receives the same hundred forced (world state, action, reward) training interventions, followed by ten independently scored withheld cases. Six seeds yield 36 arm executions across six profiles. The environmental scoring rule is disclosed and authored within this repository; no human or outside benchmark labels were involved.

## Results

| Condition | Correct held-out | Accuracy | Mean regret |
|---|---:|---:|---:|
| Scripted rule-known heuristic ceiling | 60/60 | 100% | 0.0 |
| Full Noetic with choice-value learning | 36/60 | 60% | 0.8 |
| No recurrent field | 36/60 | 60% | 0.8 |
| Signed non-neural value head | 36/60 | 60% | 0.8 |
| Value head without intentions | 30/60 | 50% | 1.0 |
| Frozen no-learning policy | 24/60 | 40% | 1.2 |

The full trained profile was correct on all repeated stable, uncertain alarm and evidence-gap cases and on **zero** of the confirmed-hazard and distress cases. Compared with the frozen policy, all of its twelve additional correct decisions came from the stable category. This is a meaningful but narrow task-level improvement. The recurrent field and developmental layer added **no observed advantage** over the non-neural signed learner in this battery, and the simple prewritten rule reliably outperformed the learned agents.

Six runs across identical ten test cases are not sixty independent episodes; no population inference follows from the table. The feature transform was designed by the implementer and receives validated structured facts directly, not language-derived semantics. Training interventions force every action to equalize exposure and thus do not test autonomous exploration. The outcome is recorded with `operator_scored` provenance; the system has no real external attestation authority. Blind human evaluations of behavior and character continuity are still absent.

## Consequences for the Noetic identity thesis

The outcome-loop now demonstrates genuine **decision-level leverage**: unlike MATRIX-002/003, selected decisions differ in a way that improves the scripted environment's objective. But it is the simpler contextual signed-value mechanism, not the unusual morphogenetic or recurrent structure, that currently accounts for the gain. The hypothesis that developmental organization itself improves persistent identity remains unverified.

Do not retune the archived fixed fixture to manufacture protection/comfort successes and reuse that same set as a confirmatory test. The rigorous next gate is [MATRIX-005 external benchmark](https://github.com/Azimn/The-Noetic-Engine/issues/17), using established independently authored text-world games and environmentally owned transition rules, plus the separate [independent character adjudication gate](https://github.com/Azimn/The-Noetic-Engine/issues/16).

This appendix is designed to accompany the v0.2 conceptual manuscript and the MATRIX-001–003 methods appendix. It does not support any extraordinary claims about consciousness, magical influence, cosmological simulation, or validation of the permanent Pretorius identity.
