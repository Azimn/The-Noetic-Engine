# MATRIX-005 post-hoc trace audit (DO NOT treat as confirmatory test)

**Original execution:** https://github.com/Azimn/The-Noetic-Engine/actions/runs/38060954980
**Post-hoc diagnostic execution:** https://github.com/Azimn/The-Noetic-Engine/actions/runs/38061116435
**Primary original data:** `results/matrix_005/cases.json.gz`, preserved byte-for-byte.
**Diagnostic tool:** `experiments/analyze_matrix_005.py`. Only derived counts and paired trace comparisons; it does not select new cases, retrain policies, or alter original outcomes.

## A more decisive null than aggregate win rates alone

For **all four official test-fold Coin Collector episodes**, the full Noetic action sequence was *exactly identical* to the no-recurrent action sequence and to the simpler non-neural signed learner sequence. For **all four official test-fold TextWorld Commonsense episodes**, the same exact command-trace identity held.

| Comparison against full | Identical coin-game command trajectories | Identical commonsense-game trajectories |
|---|---:|---:|
| No recurrent field | **4/4** | **4/4** |
| Signed value learning without field | **4/4** | **4/4** |
| Frozen no-learning controller | 0/4 | 0/4 |
| Fixed lexical heuristic | 1/4 | 0/4 |
| Uniform random legal actions | 0/4 | 0/4 |

Thus the Noetic field's bounded command-type bonus did **not** alter actual selected commands on any evaluated game. The neural substrate, slow field and related state may have changed numerical intermediate activity or scores, but not **world-facing behavior** here. Claims of incremental cognitive benefit would be unsupported.

## Sparse reward, frozen-control pathology

The common action transcript used for training contained only **two positive reward transitions** for Coin Collector and **fourteen positive reward transitions** for Commonsense cleanup. That severely limits informative credit assignment and may explain why the learned models repeatedly choose the same short action families.

The frozen no-learning policy selected `inventory` for **all 72 commands** it executed across Coin Collector test games and **all 72** across Commonsense cleanup. This stems from its untrained equal-score lexical ordering, not proof that its architecture intrinsically cannot solve either game. Consequently, its 0/4 results are an intentionally harsh but weak null control; the stronger random and fixed lexical baselines are essential.

Observed selected command families (total actions across four test games):

| Condition | Coin Collector | Commonsense cleanup |
|---|---|---|
| Full (same as no-neural/signed) | `move` 54, `take` 1 | `take` 40, `put` 32 |
| Frozen | `inventory` 72 | `inventory` 72 |
| Lexical heuristic | `move` 24, `take` 3 | `take` 35, `put` 35 |
| Random | `inventory` 14, `look` 12, `move` 19, `take` 2 | `close` 4, `inventory` 10, `look` 13, `open` 8, `put` 16, `take` 16 |

The literal command counts are those emitted by the immutable execution. A repeated command category does not by itself prove repeated *identical* world state; only source- and state-specific trace analysis can support that stronger diagnosis.

## Research decision

Retain all original negative outcomes, including the exact **8/8 Noetic-versus-simple command trajectory null**. Do not increase the Noetic field contribution on these public games and call a consequent action change replication.

The next external benchmark stage should freeze new official fold seeds, use a stronger no-learning heuristic that avoids inventory loops, include an explicit visited-room/command-history baseline, and measure enough episodes to distinguish planned exploration from luck. It should test information gain and long-range commitments separately. Any change to the action feature transform, learning rate, planning horizon or field weights is new research, not a continuation of frozen MATRIX-005 outcomes.

The morphogenetic identity hypothesis is still unverified; no production Pretorius integration is authorized.
