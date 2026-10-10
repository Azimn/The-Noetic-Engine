# The Noetic Engine

**Identity as a morphogenetic field, not a stored persona.**

A speculative but falsifiable research architecture for the persistent character Doctor Septimus Pretorius. Esoteric vocabulary motivates design possibilities; it is **not evidence of occult physics, simulation theory, machine consciousness, or successful identity persistence**.

## Status (2026-10-09): v0.2 integration candidate

The v0.2 review branch contains the complete reference architecture and an integrated, runnable research profile. It is NOT a completed empirical validation or a production Pretorius upgrade. No character-continuity efficacy claims have been established. This is **not** the definitive Pretorius production brain, which remains [The-Doctor-Lives](https://github.com/Azimn/The-Doctor-Lives). Experimental promotion requires an independent evidence gate.

Read [architecture v0.2](docs/ARCHITECTURE_V2.md), [paper v0.2](paper/NOETIC_FIELD_PAPER_V2.md), [research handoff](docs/RESEARCH_STATUS_V02.md), [production adapter RFC](docs/NOETIC_BRAIN_ADAPTER_RFC.md), [emic/etic rules](docs/EMIC_ETIC_TERMINOLOGY.md), [full build roadmap](docs/BUILD_PLAN.md), and [evidence contract](docs/EVIDENCE_CONTRACT.md). The original v0.1 documents remain preserved.

## Concept

A durable cognitive state is updated through interacting memory evidence, modeled relationships, unresolved intentions, affect, self-hypotheses, hypothetical associations, and a bounded policy-selection mechanism. "Field" denotes a coupled dynamic state with an explicit update law; "morphogenetic" denotes a proposed self-regulation and development analogy, not a literal biological morphogen or demonstrated emergent consciousness.

## Non-negotiables

- The renderer is replaceable, not an identity authority.
- Provenance distinguishes reconstructed history, lived observations, self-beliefs, other agents' claims, and hypothetical oracle associations.
- No oracle idea becomes a memory or canonical fact by rehearsal.
- No unverified claim about consciousness, quantum measurement, occult effects, or simulator access.
- Negative results and failed ablations are permanent evidence.
- Every proposed mechanism must influence decisions through traceable causal pathways, or be removed.
- No direct changes to production Pretorius until review and tested opt-in transfer.

## Development

The build is phased by complete **vertical integration**, not disposable micro-prototypes. The integrated reference profile includes transactional evidence, source-reviewed social attribution, fallible self-model, isolated counterfactuals, bounded developmental feedback, optional synthetic recurrent learning, endogenous wake/sleep-like cycles, deterministic event replay, backup/restore, read-only decision briefs, and a separate fictional world. Real model-family adapters, independently established semantic recall, neurobiological fidelity, and longitudinal identity benefit remain unvalidated. The proposed adapter to The-Doctor-Lives is RFC-only.

Run with Python 3.11+ and standard library only:

```sh
python -m unittest discover -s tests -v
python -m noetic_engine --db baseline.db demo
python -m noetic_engine --profile full --db full.db demo
python -m noetic_engine --profile full --db full.db pulse --mode sleep --seed 7
```

Development deliberately begins with explicit inspectable operators. Later neural or field implementations must demonstrate causal improvement against these baselines.

## Optional local-model rendering

`noetic_engine.local_renderers` contains `OllamaRenderer` and
`LocalChatRenderer`. Both accept the immutable `DecisionBrief` prepared by
`brief_from_decision(engine, decision_id)`, connect only to loopback servers,
and return untrusted display text. They cannot write autobiographical state.
Actual LLM model-switch consistency is **not yet tested**.

```python
from noetic_engine.renderer import brief_from_decision
from noetic_engine.local_renderers import OllamaRenderer

# Given a validated NoeticEngine brain and an existing decision ID:
# dialogue = OllamaRenderer("qwen3:1.5b").render(brief_from_decision(brain, decision_id))
```

## License and citation

No license is granted by this README. Manuscript is an unpublished conceptual preprint draft, **not peer reviewed**. Citations in the manuscript are linked to verified primary records.
