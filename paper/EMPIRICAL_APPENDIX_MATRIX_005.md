# Empirical appendix C: External TextWorldExpress task evaluation (MATRIX-005)

**Status:** executed benchmark engineering report, not a peer-reviewed or independently adjudicated character-identity result. Prepared 2026-10-10 as an additive appendix to the Noetic identity paper.

## Why this experiment matters

MATRIX-004's narrow 60% accuracy depended on project-authored world scoring. To test whether any advantage survives a genuinely external state transition authority, MATRIX-005 used **TextWorldExpress v1.1.0**, an independent Scala/Java text-game engine with official train/test folds, natural-language observations, legal command lists and objective simulator scores.

The Noetic five-action character controller could not directly operate arbitrary game commands. Therefore an explicit, reversible *experimental command adapter* was built: Noetic produces bounded motivational field state from typed witnessed game observations, and the separate `ExternalCommandPort` scores *actual* externally admitted command strings. This is not the proposed NoeticBrainAdapter for Pretorius, and the external policy still uses a handcrafted lexical action encoder. The language model did not interpret scene text.

The common training behavior log is generated through uniformly random legal commands on three official training seeds per game. Each policy condition consumes an **identical** transcript of world text, legal commands, actions and objective returned rewards. Its trained source ledger and weights are snapshotted, then cloned separately for four official test games per task. Test reward is recorded but not applied to training. No path generator, game answer key or private state is exposed.

## Prespecified evaluation

Two external environments: Coin Collector (four rooms) and TextWorld Commonsense (one room, two cleanup objects). Maximum of 18 external commands per episode. Six profiles: full field+recurrent, no-recurrent, non-neural signed-value learning, frozen control, fixed lexical command heuristic, and random admissible action. [Protocol](../experiments/PROTOCOL_MATRIX_005.md); [executable source](../experiments/matrix_005.py).

**First green execution:** https://github.com/Azimn/The-Noetic-Engine/actions/runs/38060954980 at `0e010c0fa961fad3824a973fbfe76f89bf8cff62`. 81 regression tests passed. The external two-game matrix executed all 48 held-out game episodes and all six conditions. [Complete original case-level data](../results/matrix_005/cases.json.gz); [readable report](../results/MATRIX_005_RESULTS.md). Subsequent CI runs confirmed the archived data remained stable.

| Policy | Coin Collector terminal success | Commonsense cleanup terminal success | Commonsense mean partial score |
| --- | ---: | ---: | ---: |
| Full Noetic field+neural | 1/4 | 0/4 | 0.500 |
| No recurrent field | 1/4 | 0/4 | 0.500 |
| Signed value learner only | 1/4 | 0/4 | 0.500 |
| Frozen untrained policy | 0/4 | 0/4 | 0.000 |
| Handcrafted lexical heuristic | 3/4 | 1/4 | 0.375 |
| Random legal commands | 2/4 | 1/4 | 0.375 |

**Post-hoc source-trace audit:** https://github.com/Azimn/The-Noetic-Engine/actions/runs/38061116435. The full Noetic controller produced **identical external command sequences** to both no-recurrent and non-neural signed learning on **all eight tested games**. The primary hypothesized neural/developmental contribution to external action selection was therefore absent in this protocol, irrespective of internal field dynamics. Two positive training reward transitions in Coin Collector and fourteen in Commonsense may limit learning strength. The frozen equal-score baseline chose `inventory` for all 72 of its commands in each environment, rendering it an artificially weak no-learning comparator; the stronger lexical and random baselines are critical.

## Scientific interpretation

These are real task outcomes from a third-party software environment, but the four test seeds per game and manually constructed command encoder are insufficient to establish any general policy ranking. Coin Collector's lexical heuristic and random policy both outperform full Noetic on these particular test worlds; the richer system has no measurable extra success, and its measured command traces exactly match the simple learned condition. The benchmark makes no assertion about cognitive identity, preserved autobiography, legitimate affective development or subjective experience.

This result contrasts with the limited context-regulation success in MATRIX-003: Noetic can **separate causal environmental pressure from transient internal state**, but that capability does not automatically yield **competent action selection in external environments**. The more radical morphogenetic identity thesis remains an unverified hypothesis. The scientific program should retain the negative rather than select favorable tasks or increase a coefficient on a disclosed public test set.

## Required next evidence

A new, preregistered official-fold cohort with adequate sample size and genuinely stronger graph-exploration, retrieval, and low-resource language-model planning baselines; structured actions must come only from the environment's actual admissible commands. Independently human-adjudicated character continuity is a separate question and must have blind evaluator agreement and long-running episodes. Previous Egregore semantic-confabulation and fresh-decoder donor issues remain unresolved. No production Pretorius architecture migration follows from MATRIX-005.

This appendix is a descriptive source-verified research supplement, not proof of artificial consciousness, cosmological simulations, historical magic, or a biological connectome model.
