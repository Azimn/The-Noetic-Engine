# MATRIX-002 Results: field restoration and signed feedback

**Executed diagnostic, not a validated identity result**
**Experimental date:** 2026-10-09 US Central, GitHub runner recorded 2026-10-10 UTC.
**Frozen protocol:** `experiments/PROTOCOL_MATRIX_002.md`.
**Fixture SHA-256:** `2c20b59ed3f461a50c67724d8897745dc689250ad5413b1508fd2777ff43da69`.
**First successful executable head:** `c5ae92e116fe2346bc645df011efc77f85eb0125`.
**CI:** https://github.com/Azimn/The-Noetic-Engine/actions/runs/38025608142
**Raw GitHub artifact:** https://github.com/Azimn/The-Noetic-Engine/actions/runs/38025608142/artifacts/11659964299
**Permanent case-level archive:** `results/matrix_002/cases.json.gz`.
**Permanent executable summary:** `results/matrix_002/aggregate.json`.

## Executed cohort

52 regression tests passed. The run executed 160 fixed profile/scenario/seed cases (5 profiles x 4 novel synthetic scenarios x 8 prespecified seeds), each with five independent branches restored from the same SHA-256-verified SQLite checkpoint: 800 individual forked continuations. All case-level traces, score vectors, intermediate fields, outcome interventions, checkpoint hashes and final state projections were emitted. This cohort contains no independently correct behavioral labels, human adjudication or actual language-model renderer use.

## Results: no tested profile demonstrated return toward the control

The ratio is the mean within-case final field L1 separation after fourteen endogenous cycles divided by the field separation immediately after a shock event. A value below one would indicate a reduction in separation; a value above one means the intervention's field effect widened instead of closing.

| Profile | Initial shock field L1 | Final field L1 | Mean end/initial ratio |
|---|---:|---:|---:|
| Full v0.2 research profile | 0.528200 | 1.064637 | **1.9929** |
| No developmental field | 0.533654 | 1.135886 | 2.1417 |
| No recurrent field | 0.533681 | 0.976586 | 1.8170 |
| No target regulator | 0.480730 | 1.129141 | 2.3643 |
| Frozen-control policy | 0.494125 | 1.165259 | 2.3877 |

These are within-profile counterfactual comparisons, not identical cross-profile baseline states. The full configuration had lower mean divergence than the frozen control by this descriptive measure but was still divergent. The recurrent-ablated profile happened to have a lower ratio than full. That is not a general demonstration that removing neural dynamics improves identity.

**Critical design qualification:** the shock was a one-time *injection into retained affect state*, not a guaranteed short-lived disturbance of the full system. In the current engine, waking cycles do not decay the `threat` and `fatigue` affect channels, and scheduled sleep cycles reduce them only by a factor of 0.93 on each sleep event. Therefore the perturbation's influence remains causally present during much of the measured recovery period. Failure to approach the unperturbed arm is a reliable result **under this protocol**, but does not isolate whether the regulator can restore identity after the exogenous disturbance truly ends. Follow-up tests must differentiate short-pulse input, decaying affect memory and persistent legitimate threat.

## Results: consequence-dependent parameters move, selected policy does not

All feedback arms shared an exact pretraining checkpoint, identical text, same four forced `investigate` actions and matching held-out probes. The only reward variation was operator-assigned +0.9, -0.9 or 0.0; it was not independently verified against a fictional environment.

| Profile | Mean positive vs negative held-out score L1 | Mean developmental target L1, +/- | Changed held-out actions |
|---|---:|---:|---:|
| Full | 0.013921 | 0.099969 | **0** |
| No development | 0.011181 | 0.000000 | 0 |
| No recurrent | 0.010566 | 0.098085 | 0 |
| No regulator | 0.009226 | 0.103842 | 0 |
| Frozen control | 0.000000 | 0.000000 | 0 |

The frozen *policy* control is insensitive to reward sign as intended, even if some inactive internal bookkeeping state can still be written. Full Noetic feedback changes developmental targets and score values but never alters the chosen actions on these probes. That is evidence of **weak or non-decisive learned policy leverage** in this finite case battery, not of meaningful autobiographical development.

## Interpretation and next action

MATRIX-001 already showed that intentions change action selection more frequently than the neural field. MATRIX-002 deepens this finding: even with four repetitions of opposite feedback, the full learning pipeline did not change a single subsequent selected action in these scenarios. Meanwhile the current field did not visibly return to the unperturbed baseline after a shock whose affect trace persisted.

The next genuine mechanistic question is whether the field can recover after a disturbance that is explicitly removed, while retaining *justified* changes after a durable consequence. A new independent protocol needs **three** distinguishable conditions: a one-time external impulse with explicit termination; a continuing threat that legitimately requires adaptation; and contradictory high-authority evidence that warrants revising the old identity target. The slow target and affect time constants must be treated as separately measured components, not hidden engineering choices. Keep a frozen v0.2 control and independently authored cases, and compare action outcomes rather than rewarding movement toward a fixed original attractor.

A second separate requirement is a policy-margin study. The present chosen actions may remain unchanged despite real score shifts because all cases are too far from decision boundaries. Measure margin distributions and test alternative authorized actions and delayed consequences on newly written episodes. Do not tune the weights on this public case set, then reuse it as a confirmatory holdout.

**Scientific status:** Negative, mixed diagnostic findings. No claim of recovered identity, superior artificial personality, consciousness, or occult mechanism. Independent E4 donor fresh-decoder and human-judged long-run character tests remain open. No mechanism is eligible for automatic production transplant.
