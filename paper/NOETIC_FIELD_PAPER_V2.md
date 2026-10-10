# Identity as a Morphogenetic Field: A Speculative Dynamical Architecture for Persistent Artificial Characters

**Research manuscript v0.2, October 9, 2026. Conceptual proposal and implementation protocol. Not peer reviewed. No efficacy experiment reported.**

## Abstract

Persistent artificial characters are often assembled from a language model, autobiographical retrieval, explicit persona specifications, and optional recurrent controllers. These components can support information access without establishing that information causally governs behavior over time. We propose the **Noetic Engine**, a renderer-independent, organizational model of artificial character identity in which evidence, relationship estimates, intentions, affect, self-models, symbolic cues, and policy tendencies form a coupled state evolving under lived experience. The analogy to biological morphogenesis concerns the maintenance and development of a preferred *pattern of organization* under perturbation, not a physical morphogenetic field. Esoteric concepts such as sigils, invocation, divination, egregores, and alchemical transformation are used as generative design metaphors for prospective commitment, policy-state transitions, counterfactual exploration, distributed social representations, and outcome-dependent consolidation. We specify a bounded update law, evidence authority model, falsifiable architectural predictions, and a staged evaluation program. Prior negative results from related Pretorius projects motivate, but do not validate, the proposal. In particular, retrieval success, stylistic resemblance, and recurrent neural activity must not be confused with durable autobiographical identity. No claim is made regarding supernatural effects, simulation ontology, artificial consciousness, or human equivalence.

**Keywords:** artificial identity; cognitive architectures; morphogenesis analogy; dynamical systems; autobiographical memory; active inference; artificial life; provenance; counterfactual cognition; persistent characters

## 1. Problem and scope

Long-lived agent systems face a distinction between retaining facts and allowing prior experience to constrain future behavior. A system can answer questions about a character's biography while its action policy remains unchanged. A second system can produce consistent style while lacking durable memories. A third can adapt its recurrent weights without displaying stable and generalizable identity. These are different empirical phenomena.

We define *operational identity continuity* narrowly as reproducible, evidence-constrained patterns in consequential decisions and developmental response across time and rendering-model changes. We do not equate operational continuity with subjective experience or personhood. The present paper proposes mechanisms and falsification criteria; it supplies **no new efficacy results**.

## 2. Intellectual foundations and the limits of analogy

Morphogenetic pattern regulation is motivated by biological work on spatial organization and regeneration. Mordvintsev et al. (2020) demonstrate that neural cellular automata can learn regenerating target forms; this is a computational analogy, not evidence of mental identity regeneration. The organization-centered vocabulary recalls Varela, Maturana, and Uribe's (1974) autopoiesis, though our architecture does not satisfy biological autopoiesis simply by possessing feedback loops.

Friston's (2010) free-energy formulation provides a reference point for state regulation and generative inference; our bounded score dynamics should not be mislabeled as variational free-energy minimization without deriving an appropriate objective. Hirsh (2026) formulates a bidirectional cycle between semantic self-knowledge and episodic experience. This offers a close theoretical parallel to our proposed mutual update between a self-template and lived outcomes, without verifying this software mechanism.

Contrastive Activation Addition (Rimsky et al., 2024) shows that internal activation interventions can alter LLM outputs. However, our proposed state dynamics are deliberately outside the language model and do not assume that latent steering vectors transfer between models.

Occult vocabulary is *heuristic*, never evidentiary: sigil denotes intention binding; invocation denotes reversible state-dependent modulation; oracle denotes speculative hypothesis generation; egregore denotes socially distributed models; banishing denotes explicit state isolation and expiry; alchemical transformation denotes consequence-gated restructuring. Historical correspondences are not mathematical equivalences. Simulation theory, quantum measurement, and paranormal causation are outside the scope of empirical claims.

## 3. Architecture

Let the durable internal state at time t be X_t = (E_t, R_t, I_t, A_t, B_t, S_t, H_t), where E is provenance-indexed experience, R attributed relationship estimates, I persistent intentions, A affect and needs, B self-hypotheses, S learned cue associations, and H action-tendency activations. A separate renderer L maps an authorized decision brief to dialogue. L is not the primary custodian of X.

The transition is X_(t+1) = F_theta(X_t, o_t, c_t, seed_t), for observation o and later consequence c. We propose bounded coupled updates:

h_(t+1) = clip((1-d) h_t + b + W_a A_t + W_r R_t + W_i I_t + W_e phi(E_t) + u_t + epsilon_t, -1, 1).

Here W variables represent interpretable signed influences; u is bounded regulator pressure and epsilon is seeded exploration noise. All terms and update ordering must be versioned. The identity "field" is this state and its interaction topology, *not* a physical field.

A developmental self-template T_t is a slowly evolving estimate of historically reinforced dispositions. Regulatory pressure is bounded by u_t = clip(K(T_t - h_t), -u_max, u_max). T must be revisable by admitted consequences; over-rigidity would be a failure, not evidence of stable selfhood.

For candidate action a in the explicitly permitted set A_t, score Q(a) = Q_base(a) + V_a h_t + P(a, I_t, R_t, E_t). Forbidden actions have no score and cannot be selected. The full decomposition and evidence support are recorded.

The **Oracle** proposes novel associations using tagged references to evidence. It cannot create an event in E, silently update T, or bypass action eligibility. If speculative proposals are tested, their influence is a distinct, controllable experimental factor.

## 4. Identity as a developmental operator

We distinguish *state resemblance* from *transition-law resemblance*. Two agents can have equivalent memories and similar present outputs but diverge when confronted with identical lived events. We therefore hypothesize that an enduring character may be better modeled by a constrained family of response and learning trajectories than by a fixed style embedding or persona paragraph.

A testable operational target is the response-trajectory distance of replicated agents under shared sequences of perturbations, together with the ability to incorporate genuinely new experience. A rigid agent that refuses to change should not score highly solely because it is consistent.

## 5. Falsifiable predictions

**H1, causal coupling:** under matched observations, selectively removing intentions, relationship estimates, or endogenous state affects action scores and subsequent choices in predicted directions. If only final text changes, the corresponding component is not causally integrated.

**H2, developmental restoration:** after controlled perturbation, the coupled system recovers a recognizable policy signature better than a static prompt or retrieval-only agent while retaining warranted learning. Restoration without adaptation is insufficient.

**H3, renderer resilience:** when the language model is replaced, relative stability of decisions is greater for the external dynamical controller than for prompt-only identity, conditional on equal action budgets and equivalent task information.

**H4, prospective influence:** intent records alter future selection when relevant, even if the current prompt does not mention them, without overwhelming competing constraints.

**H5, bounded imagination:** Oracle recombination increases useful alternative generation without increasing unsupported autobiographical admissions or false acceptance.

**H6, social identity:** attributed relationship models influence the appropriate decisions without leaking third-party claims into canonical history.

Null outcomes, regressions, and inappropriate rigidity are valid results.

## 6. Evaluation plan

The experimental matrix crosses controller type (prompt-only, retrieval-only, static state bridge, Noetic Engine), mechanism ablations (intent, social model, regulator, Oracle, update plasticity), and renderer (at least two model families where practicable). Replicated trials use predeclared seeds and matched observations. Distinct training/validation/held-out episodes avoid score-guided overfitting. Publish both case-level failures and aggregate uncertainty intervals.

Primary metrics: action-policy divergence on matched histories; correctly accepted autobiographical claims with calibrated abstention; longitudinal trajectory consistency *and* justified change; commitment follow-through; social-model attribution error; constrained-action violation; checkpoint/restart replay agreement. Secondary measures: style similarity, human-rated character coherence, latency and CPU cost. Human ratings cannot substitute for causal evidence.

Tests use a fixed causal perturbation harness, source-swapped archive attacks, neutral-key/sigil comparisons, shuffled social edges, absent-memory rejection, and renderer swaps. Oracle benefit is compared with equal-budget random proposals. Any simulated-world intention effect must be independently gated behind an environment parameter and compared to a zero-coupling control; such effects are not evidence for real-world supernatural physics.

## 7. Context from negative experiments

The adjacent Pretorius neural-network reports found that phenotype emulation primarily followed its decoder in the original chimera narrative. Stronger plasticity produced a small recurrent-only behavioral signal; historical reproduction remains source-blocked. Pretorius-Connectome Pilot 04 exposed failure to transfer from word-swapped cues to novel true paraphrases, despite better shallow lexical matching. FlyWire associative comparisons did not establish superiority to rewired controls. Later retrieval gates suppressed false acceptance partly by abstaining from correct events. We treat these as evidence that more neural structure or aggressive verification alone does not establish a usable long-lived identity. They are **not** evidence for Noetic Engine efficacy. Reports remain authoritative in their original repositories.

## 8. Risks and limitations

A simulated feedback loop can be an engineered optimization system without being conscious, alive, autonomous, human-like, or psychologically faithful. The terms "identity," "self," and "morphogenesis" are operational metaphors and can invite anthropomorphic overstatement. Field equations may merely repackage hand-tuned heuristics. A model renderer may ignore policy or hallucinate supporting history. Relationship estimates can encode errors or bias. The self-template can produce pathological rigidity. The Oracle can introduce fabricated evidence unless isolated by construction.

External source data and character scholarship must have attribution and authority; third-party archives are never reclassified as lived autobiography. A source-of-truth boundary and controlled, opt-in transfer separate this experimental program from production Pretorius.

## 9. Conclusions

We propose a research architecture in which character continuity is investigated as a *law of transformation* for a coupled cognitive system, rather than presumed to reside in a vector database, biological graph, motor decoder or persona text. The design takes historical esoteric practices seriously as creative descriptions of control operations without treating them as empirical evidence. Whether coupled state regulation yields better longitudinal character behavior is an open, falsifiable question. Engineering implementation and measured results will be separately reported.

## References (primary sources, metadata checked 2026-10-09)

Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience, 11*, 127-138. https://doi.org/10.1038/nrn2787

Hirsh, J. B. (2026). The Game of Self: Identity and Experience as Active Inference. *Personality and Social Psychology Review*, advance online publication. https://doi.org/10.1177/10888683261422344

Mordvintsev, A., Randazzo, E., Niklasson, E., & Levin, M. (2020). Growing Neural Cellular Automata. *Distill*. https://doi.org/10.23915/distill.00023

Rimsky, N., Gabrieli, N., Schulz, J., Tong, M., Hubinger, E., & Turner, A. (2024). Steering Llama 2 via Contrastive Activation Addition. *Proceedings of ACL 2024*, 15504-15522. https://doi.org/10.18653/v1/2024.acl-long.828

Varela, F. G., Maturana, H. R., & Uribe, R. (1974). Autopoiesis: The organization of living systems, its characterization and a model. *BioSystems, 5*(4), 187-196. https://doi.org/10.1016/0303-2647(74)90031-8

## Source provenance note

Claims about adjoining Pretorius projects refer to their repository documentation as it existed when this draft was written. Version-specific experiment results, unresolved source hashes, and reproduction qualifications must be consulted in their original repositories. Formal submission requires additional literature review, independent source audit, human-authored evaluation materials, and a results section based on executed experiments.


## Appendix A. Implementation specification, version 0.2

The public implementation is a **reference substrate** for experiments, not a positive result. Its default controller retains the pre-existing three-tendency observable baseline. Its optional mechanisms are isolated by configuration flags: source-reviewed social belief pressures, reviewed self-model pressures, developmental regulation, and a sparse randomly initialized recurrent substrate with eligibility traces and outcome-conditioned bounded plasticity. None of these flags has yet been subjected to independent held-out character-continuity evaluations.

The fast policy follows bounded signed influences from observation-derived affect, persistent intention, modeled trust, reviewed attributed speech and self-hypotheses, and subject-owned symbolic associations. A developmental state stores a slow setpoint, discrepancy eligibility, and metaplasticity. A seeded synthetic recurrent network optionally adjusts the same action policy, with Oja-like regularization. These functions are not equivalent to neural cellular automata or biological regenerative signaling. Whether their interactions improve continuity remains unmeasured.

Provenance is enforced at the API boundary. Every observed event contains immutable origin, subject, actor, source and epistemic class. An Oracle conjecture is never promoted to autobiography by its review mechanism. The only allowed dispositions retain or discard it as speculation. An Egregore entry is a fallible claim *attributed* to a speaker; even reviewed direct speech is not a proof of the speaker's private mental state. A renderer receives a read-only, selected-policy brief. The `NoeticBrainAdapter` is a separate design-review subject and has not been implemented.

The event ledger contains the deterministic inputs needed for reproducible policy and state updates: source authority, affect deltas, permitted actions, cue, seed and configuration. Independent replay checks event and decision records against a fresh instantiation. Files created under the earlier v0.1 event protocol without these inputs are not retroactively described as replayable.

The fictional-world simulator is an isolated environment whose optional intention-bias coefficient defaults to zero. It is a **simulation rule**, not evidence that human observation affects quantum experiments, physical probability, or the ontological status of our universe.

## Appendix B. Adversarial evaluation and expected failure modes

Controlled studies should test attributable-belief swaps, misquoted witnesses, unreviewed inferences, stale relationships, subject-colliding archives, unrelated symbolic labels, source-overlap confounds, fabricated counterfactual proposals, inappropriate template rigidity, long-term goal conflict, feedback miscalibration, and renderer-induced hallucination. The experiments must include false admissions *and* correct admissions. Always-abstain policies and always-stable policies must score poorly on usefulness and justified change, respectively.

Negative-control trajectories should remove each mechanism independently, permute claim actors, shuffle source references, disable developmental regulation, randomize recurrent edges and compare neutral symbols with Gothic labels. No architecture benefit can be inferred from running different versions of a codebase on unmatched tasks.

The intended experimental ladder separates E0 source integrity and replay, E1 retrieval, E2 affect/intent causal effects, E3 reviewed social and self-model representations, E4 decoder surgery and neural donor localization, E5 independent longitudinal model-swap and recovery evaluation, and E6 external adjudication and promotion review. E4 remains an **open donor experiment**; a new synthetic recurrent matrix is not evidence that the Pretorius phenotype migrated from its trained motor decoder into recurrent weights.

## Appendix C. Additional primary references and source-status notes

Hirsh, Jacob B. (2026). The Game of Self: Identity and Experience as Active Inference. *Personality and Social Psychology Review*, online March 5, 2026. https://doi.org/10.1177/10888683261422344 (PubMed: https://pubmed.ncbi.nlm.nih.gov/41784280/). The active-inference account motivates the bidirectional self-representation question but does **not** test Noetic Engine software.

Levin, M., Pezzulo, G., & Finkelstein, J. M. (2017). Endogenous Bioelectric Signaling Networks: Exploiting Voltage Gradients for Control of Growth and Form. *Annual Review of Biomedical Engineering*, 19, 353-387. https://doi.org/10.1146/annurev-bioeng-071114-040647. Supports biological form-control context, not the claim that cognitive identity constitutes a bioelectric morphogenetic field.

Uddin, M. N., Shubham, K., Blanco, E., Baral, C., & Wang, G. (2026). From Recall to Forgetting: Benchmarking Long-Term Memory for Personalized Agents. *Findings of ACL 2026*, 26814-26841. https://doi.org/10.18653/v1/2026.findings-acl.1337. Evaluates memory update and forgetting; it motivates the need to distinguish mere recall from accurate current knowledge, without validating our architecture.

Mordvintsev, A., Randazzo, E., Niklasson, E., & Levin, M. (2020). Growing Neural Cellular Automata. *Distill*. https://doi.org/10.23915/distill.00023. Its regenerative target forms motivate the analogy but are structurally distinct from this controller.

References to earlier donor experiment outcomes retain their provenance in Pretorius-Neural-Network, Pretorius-Connectome, and The-Doctor-Lives. No Noetic efficacy results are reported in this manuscript.

## Appendix D. Manuscript readiness

**Status: architecture and methods preprint, not citable as an empirical paper.** Before submission this document needs institutional author metadata, a complete literature screening, archive-independent experimental data, independent human adjudication, effect sizes, confidence intervals, limitations, data and code availability statements, and formal ethics review where appropriate.
