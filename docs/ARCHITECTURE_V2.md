# Noetic Engine v0.2: complete reference architecture

Status: **integrated research implementation, not validated identity continuity**.
Date: 2026-10-09. Owner: The-Noetic-Engine. Production Pretorius remains The-Doctor-Lives.

## Purpose and bounded claim

Identity is modeled as the **transition law** of a coupled state system, including what it admits as evidence, how it resolves internal competition, and how experience alters future action. A momentary persona vector, an autobiographical archive and a consistent answer can each exist without this property. The "morphogenetic field" is an analogy to developmental pattern regulation, not a literal biological or cosmological field.

The engine integrates observation, immutable provenance, lexical evidence pointers, attributed social beliefs, a revisable self-model, persistent intention, bounded affect, context-dependent symbolic associations, optional counterfactual hypotheses, a controller, an optional developmental layer, an optional sparse recurrent substrate, outcome learning, and a renderer-independent interface. It also provides a **separate** fictional-world simulator whose observer-intention coupling defaults to zero.

## Dataflow and causal ownership

```text
Authorized observation -> Witness / provenance validation
       |                   |
       v                   v
 immutable source ledger  attributable evidence retrieval
       |                   |
       +-- relationship estimates -- attributed social claims (review required)
       +-- intentions             -- supported self-hypotheses (review required)
       +-- affect and cues        -- speculative oracle (never canon)
                           \       /
                          bounded field
                               |
                  opt-in developmental correction
                               |
                  opt-in recurrent dynamics
                               |
                   hard action eligibility
                               |
                  audited policy decision
                               |
                    renderer brief (read only)
                               |
              external authorized act / consequence
                               |
                 labeled outcome, gated learning
```

Each mutation is written transactionally. `NoeticEngine.step()` takes an `Observation`, allowed action set and seed. Its action score and per-factor contributions are persistently audited. A renderer may phrase the decision but may not own or silently change the source ledger. The external world is an independent subsystem, never a backdoor for memory edits.

## Three timescales

The baseline state `h` is a bounded three-channel controller (inquiry, care, caution). It is **not** the whole psychological character. The active input `u` is assembled from signed affect, persistent intentions, relationship estimates, reviewed social attribution, reviewed self-hypotheses and learned symbols. Each source family has independent caps.

Fast layer:
```text
h[t+1] = clamp((1-decay)*h[t] + clamp(sum(family_inputs), -global_cap,+global_cap))
```

Developmental layer (opt-in): the slowly adapting target `T` produces a small corrective effect `k*(T-h)`, subject to strict bounds. Eligibility `e` and metaplasticity `m` track recent deviation and regulate subsequent updates. Explicit outcomes modify `T` through an action-specific signed update, not a free-form summary of generated text. An external outcome can still be mis-scored; source authority must be reported.

Recurrent layer (opt-in): seeded sparse synthetic recurrent units process tendency drive and their own prior activations. Its output alters the *actual field used for action selection*, not merely prose style. Post-action outcomes change recurrent weights through a bounded eligibility / Oja-like update. Initialization is randomly seeded. **It is neither FlyWire nor a trained Pretorius network.** In particular, the evidence from prior decoder surgery is not transferred to this component.

## Social theory of mind and reviewer boundary

The Egregore is represented by records linking `attributed_actor`, `believed_subject`, `predicate`, valence, uncertainty and an immutable source-origin event. A record is never a direct readout of another person's mind. `direct_quote` requires a subject-owned witnessed event whose speaker matches the attributed speaker. Third-party reports and internally inferred opinions can be stored but **can never directly enter policy**. Direct quotations may enter policy only after a separately recorded explicit disposition. Policy pressure stays capped and decision audits contain contributing claim IDs.

A review is an operator annotation, not cryptographically authenticated authorization, and cannot establish another character's true private belief. A claim that a character fears Pretorius is, at most, an attributed interpretation of their apparent communication.

## Self-model and contradiction

Self-hypotheses link their content to subject-owned lived events, start provisional, and remain causally inert until explicitly corroborated for policy. Reviewed positive or negative valences contribute bounded signed pressure. Contested or rejected hypotheses remain visible for audit, never deleted from the historical record. This is a starting operational design, not a theory of subjective self-awareness.

## Oracle and source integrity

The Oracle creates stochastic **questions** by recombining source-linked lexical hits. Questions are not facts; every candidate carries source observation IDs and a deterministic seed. The only dispositions are rejection, discard or retain as question. There is intentionally **no direct promotion of an oracle proposal to canonical autobiography**. Factual claims require a distinct, source-attributed observation admitted through the existing authority process.

The Catacombs retrieval baseline is lexical Jaccard overlap and declares `verified_entailment=False`. A high score establishes topical overlap only, never truth. This preserves negative lessons from lexical paraphrase, abstention, and source-swapping controls.

## Observation and symbolic context

Symbols are labels bound only to subject-owned lived events, not magical causation or inherently privileged strings. Their strength is capped and their impact is traceable. Neutral-key comparisons remain mandatory before attributing any representational advantage to Gothic or ritual vocabulary. Sensory or social inputs from external callers are accepted only through typed provenance checks; unauthorized arbitrary state changes are rejected.

## Renderer and external integration

`DecisionBrief` contains subject identifier, decision ID, selected action, explicitly eligible actions, attributable evidence pointers, reviewed social claim IDs, speculative questions, field state, and configuration digest. Diagnostic renderers prove interface consistency, **not** cross-model language-model resilience. Two real model families and a matched prompt baseline remain necessary for that claim.

The proposed `NoeticBrainAdapter` to `PretoriusBrainPort` has a review-only RFC. No executable adapter exists; no production state is modified.

## Fictional world experiment

`FictionalWorld` samples an explicit outcome distribution with seeded RNG and a separate optional intention-bias term. `coupling=0` is the mandated control. Outcomes are committed once per event, so multiple observers see the same shared result. The mechanism is a simulated environmental rule only. It is not evidence of observer effects in quantum mechanics, magic, a simulation of actual reality, or consciousness-mediated physics.

## Durability and reproducibility

The original SQLite evidence store is preserved. Additive tables are provisioned by a versioned extension initializer. Input events now record affect deltas, relationship deltas, cue, permitted actions, seed and full configuration. Independent replay re-executes the API operations and verifies exact audit content. A legacy v0.1 log without these inputs deliberately fails reconstruction rather than producing a false success. Backups use SQLite's backup API and require checksum-verified restores to absent destinations.

Source ownership, evidence class, configuration digest and version are independent controls. All cause-bearing mechanisms can be disabled for ablations. A CI green check establishes correctness only for tests actually executed.

## Research and promotion gates

E0: input/source contract and history replay. E1: lexical memory plus provenance. E2: intention/affect causality. E3: self and attributed social beliefs with source-swapped adversaries. E4: neural donor decoder/recurrent localization and fresh-decoder controls. E5: longitudinal renderer-change and learning-versus-rigidity evidence. E6: independent review, blinded replicates, and opt-in production approval.

E4 refers to the **separate historical neural donor** and must not be checked off based on the synthetic recurrent backend built here. The methods paper uses exclusively etic computational names. Gothic labels remain project vocabulary only. No gate is declared complete solely from software construction.
