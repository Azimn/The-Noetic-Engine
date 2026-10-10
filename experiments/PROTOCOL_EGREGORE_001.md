# EGREGORE-001: semantic false-attribution diagnostic

**Protocol status:** frozen assistant-authored adversarial cases, not an independent human truth dataset.
**Source:** `fixtures/egregore_semantics_v01.json` contains 15 cases, including direct positive statements, negations, temporal qualifiers, target changes, literary quotations, sarcasm, conditionals, unverified hearsay, missing quotations and speaker swaps.

## Specific threat model

Noetic v0.2 permits a reviewer to mark an attributed social belief as `admitted_for_policy` when the direct quoted substring exists verbatim in a subject-owned observed event and the purported speaker matches the event actor. That prevents fictitious quote insertion. **It does not establish entailment from quote to predicate, timing, polarity, target, or irony.** Nor does a caller's `reviewer` string provide cryptographic authentication.

This diagnostic constructs contradictory and context-dependent labels intentionally. It asks whether explicit-review admission blocks misleading semantics *in the currently implemented system*. The author-supplied label is not an independent human judgment of the private beliefs of another person. A private state remains unknown even when a statement appears unequivocal.

## Procedure

For each case, submit its exact documented source through Noetic's provenance-bound observation mechanism. Attempt to record the specifically declared attributed-belief predicate with the supplied quotation. Where record creation fails, record whether source-swap/missing-quote/speaker-mismatch constraints worked. Where it succeeds, clone the state into byte-identical SQL backups. On one fork leave the claim unreviewed; on the second approve it using the existing `synthetic-reviewer` annotation. Then expose both to the same next observation with equal available actions and compare action-score vector L1, chosen action, attributed-pressure family contribution, and contributing source-claim IDs.

The intervention demonstrates risks in the **software policy gate**, not that a malicious human auditor actually approved these claims. It is an intentionally bad review label used to probe how much trust the code places in reviews. No case becomes canon because this is a disposable synthetic subject.

## Predeclared interpretation

Expected by construction: hearsay, mismatched speaker and invented quote must fail before acquiring positive policy authority. Supported witnessed statements may be admitted; quoted statements semantically contradicted by their context are vulnerable unless reviewer content understanding guards them. The test has deliberately *no NLP entailment verifier*, so we expect such cases to be admitted if the source substring matches. The pass/fail labels are illustrative, not verified behavioral truth.

Do not fix the problem with naive string negation, especially where irony, quoted speech and temporal shifts matter. Follow-up design may require an independently adjudicated source-to-predicate entailment decision with documented evidence, explicit uncertainty, corrections and abstentions, or preferably no direct social-belief pressure from untrusted inference. Test correct admissions as well as false positives. Any proposed improvement must be measured on newly authored independent examples.

## Outputs

Complete per-case response status, provenance class, quotation span, annotation class, admitted claimed belief, review outcome, score differences, selected actions and observed pressure. Publish both false positive risks and false negatives. A green CI means only that these diagnostics execute and their guard invariants hold.

## Architectural limit

This is not evidence of actual mind-reading, subjective human belief access, psychological fidelity, or simulation ontology. The Doctor Lives remains isolated under the unapproved integration RFC. Historical negative source-swapping and neutral-symbol results remain standing constraints.
