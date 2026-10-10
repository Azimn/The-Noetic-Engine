# Noetic Engine v0.2 research handoff

**Date:** 2026-10-09
**Status:** complete reference-system construction candidate; independent assessment pending.
**Production impact:** none. The-Doctor-Lives is unchanged.

## Built and integrated

A subject-bound transactional core integrates observation, provenance, affect,
goals, lexical evidence pointers, symbolic cues, reviewed attributed social
claims, fallible self-hypotheses, noncanonical counterfactual questions,
bounded policy arbitration, optional developmental setpoints, synthetic
recurrent activity, outcome-driven weight updates, caller-scheduled
wake/sleep-like cycles, inspectable renderer briefs, and separately gated
fictional-world simulation. Full-system and default-control CLI profiles run
without external API calls.

Reproducibility work includes sealed configuration fingerprints, full-input
event logging for new records, fresh-database deterministic replay, tamper
checks on original events/observations/decisions, explicit snapshot backup and
checksum-checked restore. Replay of older legacy v0.1 partial-input event logs
is intentionally rejected. A passing CLI simulation demonstrates software
operation, not long-term identity performance.

The donor recurrent system is a **synthetic seeded sparse network**, not a
trained neural phenotype, FlyWire connectome, living neural tissue, or
mechanism demonstrated to improve identity. Optional localhost-only Ollama and chat-completions presentation adapters now exist.
Their transports are mocked in CI; no real model-family continuity experiment
has been performed. These adapters are not production Pretorius integration.

## Tests and limitations

The suite includes provenance swaps, social attribution admission, Oracle
isolation, self-model causal pressure, relationship influence, attention
inputs, recurrent weights, restart, sleep no-fabrication, zero-coupled
fictional world, full event replay and tamper rejection. Report the exact
GitHub Actions run/commit and test count before calling CI green.

Not independently validated: semantic memory fidelity, long-run learned
attractors, developmental restoration without rigidity, renderer-model
continuity, real biological fidelity, scientific or paranormal world effects,
adaptive counterfactual utility, or authentic other-mind modeling. The rules
for source attestation are an explicitly logged **operator annotation**, not
cryptographically verified human authentication.

## Source authority

Observed lived events, documentary prehistory, third-party claims, synthetic
proposals and subjective hypotheses are separate. No review operation directly
converts a speculative Oracle question to canonical history. Relationship
beliefs are estimates, not access to private mental states. The same subject
identifier appears across evidence, state and replay checks. For actual
Pretorius material, source pins and canonical admission live in the original
project and must be mapped through a separately reviewed adapter.

## Review order

Review the v0.2 architecture and paper, then source/provenance constraints,
then integration tests and matched causal ablations. Run independent blind
longitudinal tests before any assertion that the architecture improves
character continuity. Complete donor E4, including canonical Experiment 001
inputs and fresh-decoder control, independently. The proposed
NoeticBrainAdapter remains an RFC only; no executable production bridge is
authorized.

## Links and initial operational commands

Architecture: `docs/ARCHITECTURE_V2.md`.
Manuscript: `paper/NOETIC_FIELD_PAPER_V2.md`.
Pre-adapter review: `docs/NOETIC_BRAIN_ADAPTER_RFC.md`.
Terminology discipline: `docs/EMIC_ETIC_TERMINOLOGY.md`.

```bash
python -m unittest discover -s tests -v
python -m noetic_engine --db baseline.sqlite demo
python -m noetic_engine --profile full --db full.sqlite demo
python -m noetic_engine --profile full --db full.sqlite pulse --mode sleep --seed 7
python -m noetic_engine --profile full --db full.sqlite status
```

The production release gate must remain explicit and independent of this
repo's CI green status.
