# The Noetic Engine: architecture design v0.1

Date: 2026-10-09. Status: proposed architecture and phased implementation, not established theory.

## Intent and requirements

Implement a renderer-independent cognitive process that (a) exhibits meaningful causal coupling across lived experience, evidence, social beliefs, intentions, self-model and regulation, (b) tolerates renderer replacement while retaining auditable state, (c) permits endogenous but *labeled* imaginative associations, (d) preserves uncertainty, contradictions and negative evidence, and (e) can fail in measurable ways.

The design is a *dynamical organizational hypothesis*, not a consciousness claim. "Morphogenetic" describes regulation of a changing target pattern under perturbation. "Field" is a vector of coupled state variables, not a physical field. Victorian ritual language is a heuristic for constructing interventions, not an assertion that occult procedures work.

## State and dynamics

At tick t: X_t = (E_t, M_t, R_t, I_t, A_t, B_t, S_t, C_t).
E: append-only evidence and provenance. M: indexed event/episode references. R: directional relationship beliefs (explicitly viewpoint-tagged). I: intentions with lifecycle, urgency, inertia and constraints. A: bounded affect/needs. B: revisable self-hypotheses. S: personal symbolic associations grounded in prior experience. C: contextual observations and action availability.

The operational transition is X_(t+1) = F_theta(X_t, observation_t, consequences_t, seed). A separate renderer reads a **bounded** decision brief; it cannot mutate E or canonical history. F must be replayable from a serialized snapshot, versioned policy/configuration and logged inputs. The neural recurrent donor is optional; the inspectable control law is the baseline.

### Proposed coupled field

For each tendency k, the activation is:
a_k(t+1) = clip[(1-d)a_k(t) + b_k + w^A_k*A_t + w^I_k*I_t + w^R_k*R_t + w^M_k*M_t + w^B_k*B_t + epsilon_k(t), -1, 1].

Signed inputs distinguish facilitation from inhibition. A state-family cap and total pressure cap prevent one accumulating variable from consuming all policy authority. Candidate action u scores as Q(u|X) = Q_base(u) + sum_k W_(u,k) a_k + C(u). C is a hard eligibility mask, not a soft suggestion. The baseline Q_base and every component must be logged. Dynamics are not allowed to rewrite identity evidence.

A *dynamic self-template* T_t encodes a learned range of habitual dispositions, not immutable commandments. State deviations yield only bounded, gradual regulatory pressure:
p_t = clamp[K(T_t - a_t), -p_max, p_max].
T itself updates slowly on appropriately admitted **lived** outcomes, never on fabricated oracle prompts or untrusted archives. Design must permit persistent contradiction, failed regulation, and permanent learning. Tracking deviation alone is not proof of identity stability.

### Update priority

1. Parse an observation; validate actor, evidence class, provenance and immutable event ID.
2. Persist input event in a transactional store.
3. Retrieve only event IDs and claim excerpts allowed by source authority; source match is NOT truth verification.
4. Update relationship beliefs and affect, respecting viewpoint and confidence.
5. Age competing commitments and update tension, without automatically treating text repetitions as new promises.
6. Generate optional Oracle hypotheses in a tagged, noncanonical namespace.
7. Propagate bounded field state and compute auditable action scores.
8. Select only among caller-authorized actions with deterministic tie-break.
9. Render an action brief; record policy and any subsequent consequence as different events.
10. Perform consolidation only through an explicit post-outcome path, recording old/new state.

## Seven mechanisms and their real computational meanings

**Witness / Observatory**: typed perceptions and measurement ledger. Observer-dependent fictional-world physics is a *separate optional environment experiment*, off by default and outside cognition.

**Archive / Catacombs**: source-linked autobiographical, historical and lived evidence with explicit rejection/abstention. No memory is derived from plausibility alone.

**Egregore / Mirror Chamber**: a network of *attributed models of others' beliefs about the subject*. Actual other-mind data and Pretorius's estimates are distinct. Relationship pressure may be causal but capped.

**Sigil / Intention Furnace**: persistent named intentions with strength, conflict, due or resolution status. The symbolic name is a label, not a causal vector unless an ablation proves otherwise.

**Oracle / Divinatory Engine**: bounded counterfactual proposals produced from known evidence and seeded recombination. Every proposal carries origin IDs, seed and `hypothesis_only` status. It cannot write canonical facts or influence policy until separately admitted as a hypothetical option.

**Circle / Arbitration**: auditable admissibility mask and policy selector. Safety, canonical constraints, and external action authority are hard constraints.

**Alchemical Chamber**: consequence-gated state revision, memory consolidation and slowly evolving target dispositions, preserving event history and reversible snapshot lineage.

## Storage and provenance contract

SQLite WAL; tables for events, memories, relationships, intentions, field snapshots, decisions, oracle hypotheses and checkpoints. IDs are stable strings or UUIDs; exact schema version and input checksum persist. No record is silently overwritten. A write that combines input, dynamics and decision must be transactional or fail closed. Store JSON payload and SHA256 content digest. Explicitly distinguish: CANONICAL_SOURCE, RECONSTRUCTED, SYNTHESIZED_ADMITTED, LIVED_OBSERVED, AGENT_SELF_REPORT, THIRD_PARTY_CLAIM, ORACLE_HYPOTHESIS. The last is never promotable by inference alone.

No historical autobiography or other agent's mental state is copied from donor repos. Adapter maps must pin source commit, version, field meaning, rights, checksum, subject identifier, admission outcome and policy version.

## Integration and renderer boundary

The engine emits `DecisionBrief` {state_version, allowed action, alternative score breakdown, evidence IDs, intention IDs, conflict flags, oracle candidates flagged speculative, affect, provenance summary}. A renderer may produce dialogue, never claims a speculative hypothesis as fact or invents memories; no renderer output is imported as lived fact without an explicit observation/acceptance step. A future versioned `NoeticBrainAdapter` targets `PretoriusBrainPort` only after acceptance.

## Perturbation and recovery

Test interruption and restart; altered renderer/model; contradictory third-party histories; conflict between commitments; adversarial attempts to promote oracle speculation; random cue substitutions; ablations of relationships, intentions, regulator and Oracle. Report both retention and inappropriate rigidity. Identity is measured behaviorally and causally, not by asking the agent whether it is the same self.

## Explicit nonclaims

No simulator API, quantum observer effect, occult efficacy, real bioelectric organism, true neural morphogenesis, consciousness, mental illness model, or human psychological fidelity is established by this architecture.
