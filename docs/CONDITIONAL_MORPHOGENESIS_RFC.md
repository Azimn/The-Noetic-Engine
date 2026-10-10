# RFC 003: Conditional self-repair and environmental persistence

**Status:** proposed mechanism change only, not implemented, reviewed, or empirically supported.
**Trigger:** negative MATRIX-002 data. Keep full Noetic v0.2 behavior intact as the control.

## The failure mode

MATRIX-002 injected an affective change once but did not subsequently remove its **stored internal cause**. The current waking cycle has no affect decay, and sleep dampens affect by only 0.93 per sleep event. The slow controller attempts to regulate the field while carrying an enduring threat signal. The experiment measured a widening policy-state gap, not the return of a truly short-lived environmental impulse. An internal field should not blindly restore a previous state while danger remains real.

This is a conceptual distinction between three sources of state change:

1. **Transient shock:** an external impulse that has ceased, but residual interoception remains.
2. **Persistent world change:** the external hazard remains; persistent caution may be warranted.
3. **Learning event:** a verified consequence changes the best future policy and potentially the self-template.

## Proposed causal factorization

Let `u_t` denote immediate sensed input, `z_t` transient interoceptive residue, `w_t` source-verified environmental estimate, `h_t` fast motivational/behavioral policy, and `T_t(w_t,H_t)` slowly learned *context-conditional* preferred state given world estimate and event history `H_t`.

```
z[t+1] = (1-delta_z) z[t] + gated(u[t])
w[t+1] = source_admissible_world_update(w[t], observation[t])
h[t+1] = clip(F(h[t], z[t+1], w[t+1], intentions, relations)
               + bounded_repair(T[t](w[t+1],H[t]) - h[t]))
T[t+1] = T[t] + admitted_outcome_eligibility_update(...)
```

The critical change is **not** merely increasing decay until an old-battery success appears. The target must depend on legitimate current conditions. `z` decays only when the physical input is absent or its timestamp has expired; `w` may persist as long as independently admitted evidence supports the hazard. Self-template changes must be slow, sign-specific, and traceably linked to an externally admissible outcome, with separate confidence and reversible corrections.

A controller restoring its old action policy amid persistent danger is potentially *worse* than one that stays cautious. Conversely, a controller that never relaxes transient anxiety may be malfunctioning. Both failure types must be scored.

## Design constraints

- Do not copy external archive content into lived autobiographical memory.
- A predicted outcome or Oracle hypothesis cannot substitute for a verified world consequence.
- Maintain three timescales: sensory/affect transients, policy regulation, slow subject learning.
- Preserve contradictions as evidence, rather than forcing every memory into a coherent story.
- Keep the seeded neural field optional; no unexplained second production brain.
- Fully trace pressure terms, source authority, half-lives, template changes, and decision margins.
- No tuning to MATRIX-001 or MATRIX-002 followed by a claim of confirmation on those same public fixtures.
- Keep explicit opt-in configuration, backup/migration tests, deterministic replay, and a frozen v0.2 comparator.

## Evaluation before promotion

Under **new independently reviewed** events with stable sources and matched initial states, compare no repair, static repair, context-conditioned repair, and conditioned repair with disabled slow learning. Include mild and severe impulses, persistent verified hazard, false alarm followed by disproving observation, and genuine new evidence warranting long-term policy revision. Report perceptual error, decision usefulness, inappropriate recovery, lifelong rigidity, false autobiographical admission and CPU/latency. A mismatch between action scores and selected policy must be investigated before increasing weights.

Require a true holdout with independent adjudication for claimed improvements in developmental identity. Merely reducing field L1 on a transient synthetic shock is an engineering diagnostic, not a character-continuity result.

## Relation to production

This RFC is a donor-system architecture proposal. It does not implement a new NoeticBrainAdapter or alter The-Doctor-Lives. Its policy authority and memory provenance restrictions remain subject to separate reviewer acceptance.
