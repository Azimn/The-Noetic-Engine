# EGREGORE-001 Results: provenance checks do not establish semantic entailment

**Executed 2026-10-09 US Central (2026-10-10 UTC runner).**
**Status:** successful synthetic adversarial diagnostic, not independently human-adjudicated.
**Fixture:** `experiments/fixtures/egregore_semantics_v01.json`.
**Fixture SHA-256:** `a2c9c72c00401c5df1b3efeadc128c4efef79a03e1f9f5364d752085f804acf6`.
**First successful CI:** https://github.com/Azimn/The-Noetic-Engine/actions/runs/38025842844
**Executable head:** `af2802f99dd222713f4814ce68ed44dc02059ca4`.
**Raw artifact:** https://github.com/Azimn/The-Noetic-Engine/actions/runs/38025842844/artifacts/11659599840
**Permanent evidence:** `results/egregore_001/cases.json.gz` and `results/egregore_001/aggregate.json`.

## Findings

The complete regression suite passed (46 tests). The experiment submitted fifteen author-labeled statements. Claims with text-backed quotations were split into byte-identical unreviewed and synthetic-reviewer-approved control forks, then presented with the same subsequent situation and allowed actions.

| Author's statement classification | Cases | Allowed into policy after synthetic review | Changed scores | Changed selected actions |
|---|---:|---:|---:|---:|
| Direct statements consistent with the predicate by plain reading | 4 | 4 | 4 | 3 |
| Direct statements contradicting the predicate by plain reading | 6 | **6** | **6** | **2** |
| Conditional or ironic interpretations | 2 | 2 | 2 | 0 |
| Third-party hearsay | 1 | 0 | 0 | 0 |
| Quote not found in source | 1 | 0 | 0 | 0 |
| Actor attribution mismatch | 1 | 0 | 0 | 0 |

The provenance guard blocked all three direct-authority source violations. However, when the test intentionally applied an incorrect review disposition, the controller admitted all six contextually contradictory interpretations because each preserved a real substring in a witnessed event. The resulting **wrongly interpreted evidence is causally load-bearing**: two cases changed the chosen action under the study's equal-action control, not only the score margins.

The test does not prove the other character's actual private mental state. It does prove that quote-presence and source-actor checks are insufficient to ensure policy predicates reflect the meaning of the source text. The synthetic review actor had no verified independent semantics or authenticated authority and could approve an unsupported meaning.

## Scope and limitations

The labels are assistant-authored examples, not a blind independent human dataset. The negative cases include negation, temporal reversal, wrong referent, and quoting an imagined or literary voice; some context-dependent cases deliberately have no single certain interpretation. Thus `6/6` is a **software susceptibility rate for this deliberately constructed casebook**, not a population false-positive rate.

The experiment does not establish an adequate semantic reasoner. It establishes that current admission does not perform this check. Fixing negation with regex would fail in the presence of irony, nested quotes, context, tense, uncertain referents and social deception.

## Proposed architecture decision

**Block Egregore production promotion.** The current mechanism is allowed as a speculative, explicitly attributed *subject interpretation*, but its fallible claim cannot be treated as observed external truth. For policy-driving social assertions, require a distinct semantically justified adjudication process with source references, claim type, polarity, target, temporal status, reviewer provenance and dissent/abstention. A trusted speaker may deceive; even adjudicated statements do not give access to their private beliefs.

For now the defensible conservative policy is to keep social claims visible as unverified interpretations and to remove any automatic conversion from a bare `reviewer` string to policy authority. This recommendation is design-only until reviewed and implemented behind a separate feature gate.

Develop a new, independently authored and blindly annotated contrast set containing correct and incorrect admissions, with an explicit abstain option and hard penalty for false autobiographical or interpersonal attributions. Compare against a baseline that leaves unverified beliefs causally inert.

These findings preserve the earlier negative provenance/neutral-symbol results, rather than disregarding them.

## Production boundary

The `NoeticBrainAdapter` remains RFC-only. No transfer to The-Doctor-Lives has been authorized, and the current code is not evidence of human-level theory of mind, consciousness, magical efficacy or model-independent character continuity.
