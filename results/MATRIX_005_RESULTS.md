# MATRIX-005 — First independently developed external text-world evaluation

**Status:** executed engineering benchmark, 2026-10-10. Not a character-identity validation or peer-reviewed result.
**External benchmark:** [TextWorldExpress](https://github.com/cognitiveailab/TextWorldExpress), PyPI release **1.1.0**, Java 17 / Python 3.12.
**Frozen protocol:** `experiments/PROTOCOL_MATRIX_005.md`.
**First full successful source SHA:** `0e010c0fa961fad3824a973fbfe76f89bf8cff62`.
**First execution CI:** https://github.com/Azimn/The-Noetic-Engine/actions/runs/38060954980
**Raw artifact:** https://github.com/Azimn/The-Noetic-Engine/actions/runs/38060954980/artifacts/11672937146
**Permanent raw:** `results/matrix_005/cases.json.gz` and `results/matrix_005/summary.json`.

## Why this matters

Unlike MATRIX-001–004, the goal rules, world transitions, admissible commands, objective rewards and success flags are **owned by an established external simulator**, not invented inside the Noetic Engine. An independent CPU-only text environment supplies game observation text and legal action lists. Neither Noetic nor its renderer is given generated gold paths or privileged object graphs.

We explicitly adapted the external action interface: Noetic's existing five policy labels are **not** game commands. The `ExternalCommandPort` is a separately audited research-only selector over real `validActions`; the normal Noetic decision step updates cognitive state as an observational cycle. Bounded inquiry/care/caution activity can bias real command selection in the full profile. The signed non-neural learner uses identical generic feature and reward updates with no field bonus.

The common training transcript was collected by legal uniformly random actions on **three** official train-fold seeds per game. All models replayed *exactly the same* observation, legal-action, executed-command and environment-reward records, avoiding preferential training exposure. Each profile was checkpointed, then cloned for **four** official test-fold seeds per game. Test feedback is logged but not learned. Every command is checked against the real environment's admissible list.

## First complete executed results

81 existing plus new regression tests passed. There were 2 independent game families x 6 policy conditions x 4 test seeds = **48 complete or capped external test episodes**. The 18-command cap is a prespecified resource constraint and failures/timeouts are retained.

| Condition | Coin Collector success | Coin average score | TextWorld Commonsense success | Commonsense average score |
|---|---:|---:|---:|---:|
| Full Noetic external command policy | 1/4 | 0.250 | 0/4 | 0.500 |
| Without recurrent substrate | 1/4 | 0.250 | 0/4 | 0.500 |
| Non-neural signed command learner | 1/4 | 0.250 | 0/4 | 0.500 |
| Frozen unlearned command policy | 0/4 | 0.000 | 0/4 | 0.000 |
| Fixed task-aware lexical command heuristic | **3/4** | **0.750** | **1/4** | 0.375 |
| Uniform random admissible action | 2/4 | 0.500 | 1/4 | 0.375 |

The full architecture and two simpler learned policy variants had **identical aggregate outcomes** on both external test families, so the neural developmental system has **no demonstrated incremental task success** here. The fixed handcrafted heuristic was more successful in Coin Collector than the learned controllers. Random action selection also outperformed the learned controllers in Coin Collector on these four seeds.

The signed learners' 0.5 average score on Commonsense cleanup is *partial game progress*; none of their test episodes reached the environment's terminal success condition. Success must never be substituted with raw score here.

Noetic's field may alter scores but not actual external actions; full exact-trace counterfactual inspection is necessary to establish whether field contributions ever changed a world command. In aggregate they clearly did not produce a benefit.

## Confounds and limitations

- **Four official test seeds per task family is far too few** for reliable model ranking or inferential superiority claims. Policies are paired by environment seed; these are not independent character/participant samples.
- There is **no local language model**. World text and action words are represented by a handcrafted lexical feature transform, so benchmark outcome is not a test of robust semantic reasoning or a complete renderer-swapped cognitive architecture.
- The external world is independently developed, but the policies, feature extraction and per-episode data collection were constructed for this study. Hand-coded lexical heuristics can exploit specific visible game commands; their performance is a useful strong baseline but not evidence that they are general minds.
- Common train experience came from a small random behavior policy. Sparse terminal game rewards can leave little or no informative credit-assignment signal, so the evaluation should report exactly how many positive training transitions occurred.
- No external reward receipt is cryptographically authenticated. The research harness passes results from the pinned TextWorldExpress process with source and observation IDs. This is stronger source separation than MATRIX-004 but not a general production trust boundary.
- The `ExternalCommandPort` is an explicit **separate experimental command policy** whose bounded Noetic field input can have a causal score effect. This is not a validated model-agnostic PretoriusBrainPort, and a successful game would not itself demonstrate stable artificial character identity, prospective commitments, or long-term autobiographical continuity.
- Version-pinned installation is used, but full reproducibility additionally depends on a stable upstream package artifact, Java runtime, official task seeds, and program environment.
- The previously discovered Egregore belief-confabulation issue remains blocked. The neural donor E4 fresh-decoder protocol and independent human character-evaluation gate are open.

## Design implications

The results materially sharpen the program: **a source-linked cognitive field by itself does not confer general exploration/planning skill**. This first external trial suggests that language grounding, goal-conditioned memory of visited rooms, competent credit assignment and more informative exploration may matter more for game success than an optional recurrent controller. Those are *hypotheses* to be tested, not excuses to increase field weights on the same public test seeds.

The immediate next stage should freeze **larger official train/test cohorts** and add neutral action-history/tabular exploration, a strong learned non-neural agent with observation memory, and an independent local-model action-ranking baseline with equal allowed actions and model budgets. A fully integrated NoeticBrainAdapter and production Pretorius changes are **not justified**. Independent blinded adjudication of warranted long-term identity change remains necessary before claiming the morphogenetic-identity hypothesis is supported.

**Conclusion:** first genuine externally scored Noetic world-interaction benchmark is operational and reproducibly archived. Result: limited progress, **no detected incremental benefit from the exotic recurrent/developmental architecture**, and simple baseline agents remain competitive or stronger. That negative result is the point of the experiment, not a reason to conceal it.
