# MATRIX-003 Results: Context-Conditional Regulation

**Date:** 2026-10-10 UTC (GitHub execution).
**Status:** executed synthetic engineering diagnostic; no identity-continuity validation.
**Frozen protocol:** `experiments/PROTOCOL_MATRIX_003.md`.
**Fixture SHA-256:** `28f3bea372bf5c2ebc9eb1519e4b4bf2a4d01ec9756c2faaeeb84d8bf621f749`.
**Executed SHA:** `587421ab45ca5da4f596c1a36cc5c4d0bda91438`.
**Successful CI:** https://github.com/Azimn/The-Noetic-Engine/actions/runs/38028225074
**Raw GitHub artifact:** https://github.com/Azimn/The-Noetic-Engine/actions/runs/38028225074/artifacts/11661146610
**Permanent raw:** `results/matrix_003/cases.json.gz`; aggregate `results/matrix_003/aggregate.json`.

## Summary

62 regression tests passed. The preregistered synthetic matrix comprised four never-before-used author-written scenarios, eight fixed seeds, three control profiles, and five independently restored continuation branches, for **96 profile/scenario/seed cases and 480 forked trajectories**. Each continuation was source-bound, transactional, deterministic given its inputs and started from the same SHA-256-verified checkpoint *within its profile*. Scenarios and conditions were not independently adjudicated; all labels and feedback were synthetic.

## Principal result: environmental source persistence is a distinct control variable

We separated an explicit one-tick external pressure from a continuing source until verified resolution. The result is displayed using mean within-case field L1 at the last cycle divided by deviation at the first active perturbation cycle; these are averages of individual ratios, not ratios of pooled means.

| Controller | Mean transient final/first field difference | Mean final field L1, sustained hazard | Mean final field L1, resolved hazard |
|---|---:|---:|---:|
| Conditional controller (gain 0.12) | 0.000205628 | 0.464205374 | 0.001254665 |
| Source drive without conditional repair (gain 0) | 0.001033275 | 0.445276086 | 0.003662531 |
| Original v0.2 affect-based encoding | 1.386140021 | 1.186961030 | 0.005441191 |

A transient external driver expired after one cognitive tick by construction. The new controller reduced its residual field difference to approximately **0.021%** of the first-cycle difference after the scheduled continuation, compared with approximately **0.103%** for the otherwise source-matched drive-only profile. That is a useful **mechanism-level success**: the new causal representation and bounded repair can produce convergence in deterministic software.

Persistent source pressure produced an enduring field shift. When an independently admitted source event marked the condition resolved, the continuing driver ceased and the difference from a source-free counterpart diminished.

**Causal nuance:** the legacy v0.2 arm encoded the same synthetic hazard as *accumulated affect* rather than an explicit expiring context. Its apparent 138.6% residual for the condition called `transient` cannot be interpreted as its recovery from a truly removed external driver, because the legacy profile never received an equivalent expiry operation. This supports the design motivation for separating causes from residue, not a matched-model superiority claim.

## Secondary result: learned policy selection is still weak

Under a shared forced action, the revised branch received an author-assigned positive reward while the matched resolved branch received zero reward. The conditions shared source events and action eligibility.

| Controller | Mean revision-vs-control developmental target L1 | Mean final action-score L1 | Changed selected actions |
|---|---:|---:|---:|
| Conditional | 0.011626425 | 0.009483439 | **0** |
| Source drive only | 0.013479285 | 0.006956123 | **0** |
| Legacy v0.2 | 0.011928176 | 0.005239277 | **0** |

The controller can persist small changes in slow internal targets and action-score vectors. None of those changes altered selected actions in this assay. The system has **not** demonstrated behaviorally useful learning from outcomes. It may still suffer from overly large policy margins, weak weight learning, insufficient generalization, or arbitrary synthetic choices; the current data cannot isolate those possibilities.

## What was demonstrated and what was not

Demonstrated: deterministic, source-bound transient expiry; persistence of unresolved context; separate admitted resolution; bounded context-conditioned regulation; full transaction and checkpoint integrity; near-convergence of field values after transient input under newly specified mechanisms.

Not demonstrated: general identity restoration, psychological realism, beneficial character decisions, correct response to continuing danger, human-like autobiographical integration, independent judgment of environmental truth, superior open-weight local-model rendering, magic, simulator ontology or consciousness.

The experiment intentionally includes author-created evidence/labels. The controller's source acceptance is only its synthetic typed admission contract. The outcome feedback is `operator_scored`, never a human-blinded verified environmental success.

## Design decisions

1. **Retain** the separate conditional-context architecture on an opt-in research branch for additional investigation. Its source/expiry mechanism is the substantive advance, not Gothic naming.
2. **Do not tune** the current public cases to manufacture changed actions. Preserve the null selected-policy result exactly and test under new, independently authored decision-margin cases.
3. **Do not merge into The-Doctor-Lives.** This is not the production identity authority; the NoeticBrainAdapter remains RFC-only pending explicit review. The EGREGORE-001 semantic-admission weakness remains a separate gate.
4. **Next:** evaluate policy-level consequence generalization, competing durable intentions, independently scored justified target changes, multiple model renderers, true held-out autobiographical paraphrases, and neutral symbols. Study also whether active context inverts maladaptive self-repair when external danger actually persists.

## Conclusion

MATRIX-003 provides a **limited positive engineering result** after the negative MATRIX-002: an explicitly controlled transient environmental cause decays out of the modeled cognitive field while an unresolved cause remains active, and a separate evidence-backed resolution removes its continuing pressure. Nevertheless, the core thesis that identity itself is morphogenetically maintained remains unproven. The next gate must move beyond field-distance recovery into useful decision-level learning and externally adjudicated character continuity.
