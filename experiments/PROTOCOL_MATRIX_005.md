# MATRIX-005: first executed external text-game causal benchmark protocol

**Protocol frozen before full run.** Date: 2026-10-10. Prior MATRIX-001–004 results are not reused as confirmatory test scenes.

## External data source and objective authority

Benchmark: [TextWorldExpress](https://github.com/cognitiveailab/TextWorldExpress), **PyPI 1.1.0**, bundled Scala/Java simulator with Python Py4J API, Java 17 and Python 3.12. This is an independently developed environment, not a Noetic-authored rule simulation. Official training and test folds and game-generated `validActions`, `score`, `tasksuccess`, `taskfailure`, `reward` determine transitions/outcomes. No model generates these scores.

Two structurally different games (both runnable on CI):
- Coin Collector, `numLocations=4,numDistractorItems=0,includeDoors=0,limitInventorySize=0`.
- TextWorld Commonsense, `numLocations=1,numItemsToPutAway=2,includeDoors=0,limitInventorySize=0`.

Predefined selection: the first **three** official valid training seeds and the first **four** official valid test seeds in increasing numeric order, queried from the game's fold API. No test seed selected by performance. Evaluation limit **18** world commands per episode.

The world engine's runtime/API was first verified in [smoke CI](https://github.com/Azimn/The-Noetic-Engine/actions/runs/38060499244). No generated gold solutions, object trees, privileged simulator data, or hidden task states may reach the agent. Agent-facing data: natural-language observation, task description and exact admissible command list. No hand-extracted fact vectors or optimal labels.

## Matched training and explicit transfer

For each game, collect an external training transcript by uniformly random legal actions with a separate deterministic RNG. Freeze its complete sequence of observations, admissible actions, action commands, score deltas and next observations. **Every learned/ablated arm receives the identical transcript**, including all zeros, terminal failures and sparse rewards. This removes differing training-exposure confounds, though it can make the learned signal weak.

For each arm, record input observation in its Noetic evidence ledger; score the chosen *forced training command* under the separate external-command port; admit a distinct external-world next-observation as the source of the returned reward; update the shared learned value rule unless frozen. All world commands are verified as members of the external admissible list. No Noetic's five intrinsic character-action labels are misrepresented as actual game commands.

After matched training, back up each subject store and restore that *exact* checkpoint into every held-out test episode. Evaluation arms choose legal game commands and receive real world feedback, which is recorded for audit only; **evaluation does not update weights**. Each held-out seed resets the third-party world. Same held-out game seeds, parameters, allowed actions and initial simulator code across profile comparisons, but **after the first different decision the observed trajectories necessarily differ** (they are not forced through identical world states). This is expected online policy evaluation.

## Profiles and action policy

Six prespecified conditions:
1. `full`: Noetic field (intentions + slow developmental regulation + synthetic recurrent units) provides bounded bonus to generic command actions; signed command-value learner receives external rewards.
2. `no_neural`: same field and learner, without recurrent neural contribution.
3. `signed_only`: same learned command-value feature transform and feedback, with **no field contribution** and no neural/developmental modules.
4. `frozen`: common policy without learning.
5. `heuristic`: plainly disclosed fixed lexical/verb rule baseline, no learned reward.
6. `random`: uniform random admissible command baseline, no learning.

The `ExternalCommandPort` is an experimental action selector, **not** `NoeticBrainAdapter`. It uses a common, inspectable feature basis: action-verb family, lexical overlap with observation/task, prior command repetition, length/specificity. An action's field bonus uses a fixed mapping of command families onto inquiry/care/caution. This mapping is arbitrary and requires ablation; do not interpret it as learned biological identity. Both scores and selected world command are logged with source IDs and SHA-256. Internally the old five-action Noetic policy only performs a forced *observation update*; its `defer` output is **not** claimed to have selected the world command. The command port is the actual policy authority in this experiment.

## Main measures

Per game, held-out objective task-success rate, mean environment score, mean commands used, learning exposure count, zero/nonzero training rewards, legal-action rate, action distributions, paired game-seed case traces, cognitive field contribution and outcome audit integrity. Full JSON for training and test with every observation and command. No in-experiment tuning of coefficient values based on held-out outcomes, no unexplained filtering of failed games.

CI first runs all core Noetic unit tests and external API smoke, then the complete 2-game x 6-profile x 4-test-seed matrix, and archives raw case-level evidence. Each test sample is an independent game generation seed but models share the same seed/task across conditions, so outcomes must be assessed in paired comparisons. The tiny number of test seeds prohibits broad significance claims.

## Outstanding scientific requirements

External TextWorldExpress benchmark success primarily tests navigation/task execution, not consistent fictional-person identity. It does not solve historical E4 fresh-decoder reconstruction, neural phenotype localization, Egregore false-belief admission, language model swaps, validated semantic autobiography, subjective access or independent human-judged justified developmental change. Production The-Doctor-Lives remains unaffected.

Even with equal train logs, the full Noetic field has different computational overhead. Report measured runtime separately and never call mere score differences a biological advantage. A stronger future test should use independently authored longer games, larger official fold samples, multiple actual local model renderers and separately human-adjudicated continuity narratives. **Negative and null results must be preserved.**
