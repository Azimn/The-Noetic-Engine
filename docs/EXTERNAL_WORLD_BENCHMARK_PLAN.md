# Beyond MATRIX-004: external interactive-world evaluation

**Status:** design-only external benchmark review. **Not installed or executed.**
**Date:** 2026-10-10. Scope: Noetic evaluation and evidence integrity, not a production Pretorius brain adapter.

## Why another benchmark is necessary

MATRIX-004 showed source-linked consequence learning changes some selected actions and improves a narrow synthetic rule task from 40% to 60%, but the non-neural signed learner matched the full cognitive architecture and a scripted heuristic achieved 100%. Four binary structured input fields encoded crucial world facts directly, and our project authored both observations and the outcome rule. No independent language grounding, multi-step planning, action-quality annotation, or persistent artificial identity was demonstrated.

A stronger evaluator must separate **environment authority**, **observation representation**, **cognitive state**, and **action consequence**. It must not hand agents a fully resolved fact vector that trivially reveals the correct action class.

## Existing reproducible external worlds

1. **TALES** (Microsoft, https://github.com/microsoft/tale-suite): an external Text-Adventure Learning Environment Suite that unifies curated interactive games from Jericho, TextWorld, TextWorld-Express, ScienceWorld, and ALFWorld. The upstream README specifies Python 3.12 and Java for certain environments. Best long-term benchmark harness because it can test more than one family of environments.
2. **ALFWorld** (https://github.com/alfworld/alfworld): interactive textual worlds aligned with the ALFRED embodied-task family, with admissible action commands and objective progress and terminal indicators. A practical first *external* causal benchmark for multi-step action sequences and language-grounded scene interpretation.
3. **TextWorld** (https://github.com/microsoft/TextWorld): game generation and externally scored quest completion, with configurable room/object/quest complexity. The upstream documentation currently describes Linux/macOS package support and recommends Docker for Windows. Valuable controlled procedural tests of long-horizon memory and counterfactual action value.
4. **ScienceWorld** (https://github.com/allenai/ScienceWorld): external scientific-task environment with stateful object interactions and objective completion. Potentially informative for Pretorius's laboratory identity and procedural investigation, but it requires Java and is substantially more complex than MATRIX-004.

These external projects are **not** evidence of consciousness, neural plausibility or stable individual identity. Existing game success can be solved by language-model/world-planning capability alone. Use signed non-neural learners, static retrieval, and permitted simple policies as strong controls.

## Required `ExternalWorldPort` review contract

No engine modification until the adapter boundary is reviewed. Minimal conceptual methods:

```text
reset(seed,split) -> observation, admissible_actions, episode_id
step(episode_id,action) -> observation, reward, done, world_event_id, authority_digest
evaluate(episode_id) -> completed, score, step_count
```

The independent world engine, not Noetic and not the renderer, owns the authoritative state, admissible action list, scoring, and evidence digest. Noetic owns actor-specific intentions, sources, memory, learned policy and decision trace. Any natural-language rendering must be given equal information and token/compute budget across models. An action can only be executed when the world engine explicitly lists it as admissible.

Do **not** equate an environment-provided string or a generic reviewer name with cryptographically authenticated evidence. The eventual port should validate the world implementation version, episode ID, causal ordering, signed/checksummed source receipt (when supported), and single-use feedback. It should never write an Oracle proposal or another actor's archive into the subject's lived memory.

## Proposed controlled study

- Independently sourced, version-pinned train/dev/test tasks from a chosen external environment.
- Stage A: scripted policy ceiling and frozen/static/retrieval baselines, no Noetic learning.
- Stage B: signed non-neural learner versus opt-in Noetic full with and without neural/developmental components.
- Stage C: sustained commitment, contradictory observations, source swaps, interruption/resume, and eventual return to the world after multiple episodes.
- Stage D: change language renderer models with Noetic state frozen, then evaluate action policy, source correctness and task reward. Control for the fact that language model changes can alter perception/feature extraction itself.
- Stage E: independent human adjudication of whether warranted identity changes actually preserve the intended character's history and social commitments. This step cannot be replaced by environment success alone.

Primary environment metrics: objective episode completion, total world reward, normalized cost, invalid actions, evidence confabulation, action trace/margin, self-consistency over episodes, recovery after interrupted state and legitimate goal revision. Secondary subjective character measures require blind independent human review and report annotator disagreement.

## Immediate implementation gate

First choose a genuinely runnable text-only environment compatible with CI resource limits (TALES/ALFWorld/TextWorld) and pin the exact package version and dataset sources. Build a read-only experimental adapter on an isolated branch. Test that the world environment's action scoring cannot be inferred from hidden privileged state in the observation adapter, and prevent training on held-out environment states. Preserve E4 fresh-decoder and EGREGORE-001 production blocks. Do not transfer source memories or weights into The-Doctor-Lives.

This roadmap is **not** a report that any external benchmark has run.
