# MATRIX-004 Results — consequential policy learning under a scripted world

**Executed:** 2026-10-10 UTC. **Epistemic status:** synthetic, rule-defined software benchmark; no independent human evaluator.
**Frozen experiment:** `experiments/PROTOCOL_MATRIX_004.md`
**Fixture SHA-256:** `d691a6e66d2f22d71b53d7151e264669b3e0cbfa091c943fd68f049113fc1b0e`
**First successfully executed head:** `16c1ce27c8e3c5ee0989e95e8fbc73cdce875dff`
**CI evidence:** https://github.com/Azimn/The-Noetic-Engine/actions/runs/38058384913
**Unabridged artifact:** https://github.com/Azimn/The-Noetic-Engine/actions/runs/38058384913/artifacts/11672600146
**Permanent case-level archive:** `results/matrix_004/cases.json.gz`; aggregate `results/matrix_004/aggregate.json`.

## Completed procedure

73 tests passed. Six predetermined seeds x six controller conditions = 36 independent subject/runtime arms, each undergoing the *same* set of 100 forced training actions and corresponding rule-scored outcome records. This yielded 3,600 scored training decisions and 360 held-out decisions across 10 new source scenarios. Every outcome was recorded as `operator_scored`, tied to a distinct subject-owned simulated observation and present in the replayable event ledger. The scoring logic is separate executable `experiments/matrix_004_world_rules.py`, with fully disclosed five-action rule.

Every arm received the same 20 training situations, action exposure order and distinct outcome records; no held-out rewards were fed back to the agent. The agent was given four **structured, source-recorded world facts**, not required to extract semantics from natural-language scenes. This benchmark therefore cannot be interpreted as language understanding or actual autobiographical cognition.

## Primary objective-relative results

Accuracy means percent of held-out decisions matching the world rule's ideal action. **Ten unique test cases are repeated across six seeds**, so 60 decisions per arm are not 60 independent scenarios.

| Controller | Correct / 60 | Accuracy | Mean rule regret | Consequence-value updates |
|---|---:|---:|---:|---:|
| Scripted rule heuristic (known-ceiling comparator) | 60 | **100%** | 0.0 | 0 |
| Full Noetic with consequence-choice head | 36 | **60%** | 0.8 | 600 |
| No recurrent field, same choice head | 36 | **60%** | 0.8 | 600 |
| Signed choice learner alone (without learned neural/developmental layer) | 36 | **60%** | 0.8 | 600 |
| Full choice head without persistent intentions | 30 | 50% | 1.0 | 600 |
| Frozen no-learning policy | 24 | **40%** | 1.2 | 0 |

The full system improved by **12 out of 60** selected held-out actions compared with its frozen controller. That improvement was limited to stable, no-action-needed scenes: the full learned policy scored 12/12 on stable cases, whereas the frozen control scored 0/12. Both scored 12/12 on rule-defined uncertain alarms and 12/12 on evidence gaps. **Both failed all 12/12 rule-defined confirmed-hazard cases and all 12/12 distress cases.**

This is a narrow positive software result: outcome-driven learning has become behaviorally effective in at least one scenario class, unlike MATRIX-002 and MATRIX-003 where signed feedback moved scores/targets but changed no selected actions. It **does not demonstrate generalized useful learning**, robust protection/comfort decisions or improvements traceable to a biological-style recurrent architecture.

The unchanged performance after recurrent lesion and the equality of the simple signed-only head are important negative findings: the optional neural field and developmental layer **showed no incremental objective-value advantage** on the limited benchmark. The strong scripted heuristic performed perfectly by construction using the same directly supplied structured facts. A general identity claim cannot be extracted from this simplified environment.

## Critical methodological limitations

1. The training and test worlds, action rules, text templates and feature transform were authored within the same software project. World "ground truth" is by deterministic fiat; no independent human, literary or ethical adjudication exists. Correctness here means satisfying these particular disclosed rules, not making a good real-world decision.
2. Different seeds share the same 10 held-out fact cases. A rigorous uncertainty estimate should cluster by held-out case, not treat all 60 as independent. The data does not justify a statistical superiority claim beyond this fixed fixture.
3. Structured fact input makes the inference problem extremely restricted; no lexical paraphrase, contradicted memory, unreliable narrator or genuine language processing is tested. The Egregore and Oracle were disabled in this protocol.
4. Training actions were **forced** to equalize exposure across arms. This is an off-policy diagnostic, not proof that the agent independently explores effective actions.
5. The update's evidence gate verifies origin, subject and admitted observation class but **does not cryptographically attest the truth of a reward**. A caller may supply a false outcome as a lived observation. Production use requires an authenticated environment-authority interface.
6. No model-renderer substitution, neural donor fresh-decoder test, long-range commitments, partner-dependent continuity, preserved autobiographical identity, or independent human outcome judges participated.
7. The scripted heuristic is an explicit rule-ceiling with direct access to structured facts and should not be mislabeled a trained cognitive agent.

## Decision

**Accept as an initial consequential learning engineering diagnostic**, with a narrow positive improvement to policy selection and strong nulls against an incremental neural/developmental advantage. Do not merge learned coefficients into definitive Pretorius, and do not tune this public fixture to obtain correct `protect` and `comfort` outputs then report it as independent replication.

The appropriate next experiment is a new independently authored task family with graded consequences, hidden/partial observations, delayed and uncertain reward, ambiguous action availability, source-verified external outcomes, and blinded human evaluation. Strong non-neural contextual learner and scripted policy remain mandatory baselines. New data must evaluate actual task utility plus justified character adaptation, not just score margins or arbitrary action flips.

The NoeticBrainAdapter RFC and E4 fresh-decoder neural donor gate remain outstanding; the production Egregore remains blocked by EGREGORE-001.
