# LAB-SHADOW-001 — Permanent laboratory as an autobiographical continuity benchmark

**Date:** 2026-10-10
**Status:** real cross-repository integration and scripted continuity experiment, NOT autonomous cognition, character-validity evidence, or production integration.
**Dependency:** `Azimn/Pretorius-Laboratory` commit `93d19671f7666b2996e6fcad211c5e6509336466`, **not** an unpinned dependency.
**Execution:** [First green GitHub Actions run](https://github.com/Azimn/The-Noetic-Engine/actions/runs/38069694129), 85 tests passed; full run result stored at `results/lab_shadow/first_executed.json`.

## Why use this environment?

TextWorldExpress MATRIX-005 measured independent external *task competence*, and full Noetic made exactly the same game commands as the non-neural signed learner in eight out of eight tested games. It did not address the user’s main identity question: can a subject return to a **persistent, unchanged or legitimately changed place** and retrieve its own former experience without a fresh all-knowing world dump?

Pretorius Laboratory is a better **ecologically relevant in-project continuity test host**, because objects, damage, locations, physical books, page counts, bookmarks, world epochs, and observation receipts are persistent and replayable. It is NOT an independent benchmark publisher: the same broader research program develops its world and cognitive harness, creating different validity threats. We retain TextWorldExpress as a separate negative control on general action/world competence.

## Immutable experimental boundaries

- A real fresh `SpatialHabitat` physical home and `BookLibrary` are created in an ephemeral test directory. The home receives an explicitly labeled *synthetic, three-page fixture edition*; this is **not Pretorius canon**.
- The executable creates a `SpatialHabitat.fork_to` sandbox. The Noetic adapter REQUIRES mode `sandbox`, verifies the different epoch and uses a **new** `noetic_lab_shadownode` cognitive subject. It refuses a default/production-like Pretorius subject.
- The world authority owns object locations, breakage, physical rules, supported book content, page count/bookmarks and event history. The brain owns only what the adapter explicitly delivered into its research-only witness ledger. Observation receipts certify *offering*, not attention, consciousness or real memory.
- Subject-facing source APIs are `ObservationPort.expose(room|object|shelf)` and `BookLibrary.operate(read)`. The research **operator-side** adapter verifies the source receipt/event hash and epoch before offering source-backed qualitative information to the isolated brain.
- The adapter must NEVER supply raw `inspect_object` geometry, internal `xyz_mm`, object tree state, unoffered book pages, privileged notebook contents, or the canonical parent world state. Exact metric geometry remains unavailable until a future explicit, source-backed measurement action.
- The bridge never writes `The-Doctor-Lives`, any production Pretorius ledger, Village rooms or a canonical laboratory. It is an offline sandbox harness with local actor labels, **not authenticated external actions**.
- Lab time and world revisions are independent of Noetic cognition ticks; shared physical world events are not evidence the subject witnessed them until the adapter actually consumes the offered receipt.

## Executed scripted vignette

1. Initialize a fresh lab, install a three-page, unambiguously synthetic book, then fork the world into a new epoch.
2. Offer the shadow subject qualitative beaker, book, shelf, floor and room views with separately recorded observation receipts. No exact host coordinates enter Noetic’s observations.
3. Open and *read* page one. Turn to page two, place a `copper-slip` bookmark and close the book **without reading page two**. A turn/mark does not establish cognitive consumption.
4. Through the real spatial physics reducer, break the beaker, collect its fragments, and place the broken object in the northwest floor corner; verify world revision after each mutation. Offer a subsequent qualitative beaker view explicitly.
5. Close both Noetic and lab handles. Reopen the same SQLite lab fork and independently reopen the Noetic memory ledger; **before consulting the world again**, query only remembered beaker/book observations. Confirm the second page is absent from the subject’s admitted text.
6. Inspect physical bookmark state via the operator-side verifier; return to the bookmarked page and explicitly offer the page via a verified read event. Now and only now is page two admitted to the shadow subject.
7. Back up the lab fork and verify physical world and book replay; verify the independent Noetic ledger and confirm that the unmodified parent lab has the exact original state and event cursor.

All actions are **scripted by the test harness**. Lexical retrieval over source-backed observations is an engineering property, NOT a demonstrated natural-language answer to an autobiographical question. No LLM renderer, spontaneous action policy, ability to infer book meaning, subjective self-experience, independent human raters or model migration is included.

## Future real evaluation: LAB-CONTINUITY-002

This is the next **independent preregistration gate**, not part of the above successful scripted software check:

- Freeze separate train, development and sealed test laboratory episodes. Use the *same* authoritative persistent world objects and true physical consequences across controller baselines. Each candidate gets only the observations it explicitly requested; no snapshots at memory-only return probes.
- Across multiple simulated lab days/sessions, create prospective intentions (repair glassware, follow a book reference, leave an instrument in a precise qualitative location, return after research), then interrupt/restart the entire brain and language renderer before resuming.
- Introduce a second world actor that changes an object while the agent is absent. This must produce a **stale but honestly remembered belief**, not an automatic update or invented claim of having witnessed the change. Test whether the agent recognizes the uncertainty and reobserves before acting.
- Test real physical actions and task outcomes: correct beaker retrieval and safe handling, bookmark resumption without fabricated pages, detection that an apparently remembered object was moved, avoiding already-occupied shelf slots, and legitimate adaptation to authorized world changes.
- Compare (a) full Noetic, (b) no-development, (c) no-recurrent, (d) retrieval-only/static graph, (e) simple observation/event-ledger with explicit temporal indexing, and (f) strong task planner with equal observations and compute. Explicitly prohibit field or memory sources from reading the world's privileged hidden state.
- Measure memory source/epoch correctness, missed observations, falsely claimed witnessing, physically valid actions, task success, commitment fulfillment, delayed return accuracy, replay stability, model-swap fidelity, and CPU/token cost. Human-blind evaluation of character-consistent *justified change* remains an independent requirement. Include irreversible/incorrect actions and ablation nulls.
- Distinguish **world permanence** (world server source of truth) from **remembering** (subject-side represented evidence), and from **character identity** (trajectory and self-repair). Passing the first two cannot be advertised as proving the third.
- No Village synchronization or live Pretorius adapter until separate authorization, privacy, source-evidence and world epoch reviews. Keep Egregore misattribution and neural E4 fresh-decoder blocks open.

## Reproduction

```bash
python -m pip install "git+https://github.com/Azimn/Pretorius-Laboratory.git@93d19671f7666b2996e6fcad211c5e6509336466"
python -m unittest discover -s tests -v
python -m experiments.lab_shadow_trial --output evidence/lab_shadow.json
```

All source/world/brain data is ephemeral within the rehearsal; *no* user-owned laboratory is read or modified. The run’s first raw JSON is committed as a source reference. World epochs and timestamps are randomly issued per run, so a later run should reproduce **invariants**, not exact JSON bytes.

## Interpretation

The **first executable integration gate passes**: two persistent SQLite authorities interoperate via verified, limited source receipts and survive restart with object/book continuity and separation of unoffered content. The next scientific gate must determine whether Noetic actually does better than simpler temporal memory systems when a subject has to make decisions informed by incomplete, sometimes stale, personal experiences.
