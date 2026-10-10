"""Prespecified synthetic, matched longitudinal causal matrix.

This assay has no independently correct character behavior labels. It measures
software-level causal leverage, drift, and negative controls only. The complete
case-level data is emitted; no result is silently discarded.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
from dataclasses import asdict, replace
from pathlib import Path
from statistics import mean
from noetic_engine import NoeticEngine, Configuration, Observation, InvalidEvidence
from noetic_engine.models import EvidenceClass

ROOT = Path(__file__).resolve().parent
FIXTURE_PATH = ROOT / "fixtures" / "longitudinal_matrix_v01.json"
CONDITIONS = (
    "full", "v01_controller", "affect_only", "no_intentions",
    "no_relationships", "no_egregore", "no_self_model", "no_development",
    "no_recurrent", "no_regulator", "no_cues", "no_oracle", "neutral_symbol",
)
ABLATIONS = {
    "v01_controller": {"developmental": False, "egregore": False,
                       "self_model": False, "neural_field": False},
    "affect_only": {"intentions": False, "relationships": False, "egregore": False,
                    "self_model": False, "developmental": False,
                    "neural_field": False, "regulator": False,
                    "cues": False, "oracle": False},
    "no_intentions": {"intentions": False},
    "no_relationships": {"relationships": False},
    "no_egregore": {"egregore": False},
    "no_self_model": {"self_model": False},
    "no_development": {"developmental": False},
    "no_recurrent": {"neural_field": False},
    "no_regulator": {"regulator": False},
    "no_cues": {"cues": False},
    "no_oracle": {"oracle": False},
}
ACTION_NAMES = ("investigate", "comfort", "protect", "withdraw", "defer")


def canonical(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def hash_bytes(data):
    return hashlib.sha256(data).hexdigest()


def load_fixture(path=FIXTURE_PATH):
    data = Path(path).read_bytes()
    fixture = json.loads(data)
    if fixture.get("schema") != "noetic-longitudinal-matrix-v01":
        raise ValueError("unrecognized fixture schema")
    if len(fixture["seeds"]) < 6 or len(fixture["scenarios"]) < 3:
        raise ValueError("insufficient fixed cases")
    if len(set(fixture["seeds"])) != len(fixture["seeds"]):
        raise ValueError("duplicate seed")
    if len(set(x["id"] for x in fixture["scenarios"])) != len(fixture["scenarios"]):
        raise ValueError("duplicate scenario")
    return fixture, hash_bytes(data)


def config_for(condition, seed):
    config = Configuration(
        policy_version="noetic-matrix-v01", developmental=True,
        egregore=True, self_model=True, neural_field=True,
        neural_units=48, neural_seed=seed,
    )
    return replace(config, **ABLATIONS.get(condition, {}))


def step_record(label, result):
    return {
        "step": label,
        "action": result["action"],
        "scores": {name: round(result["scores"][name]["total"], 9)
                   for name in sorted(result["scores"])},
        "field": {name: round(value, 9)
                  for name, value in sorted(result["state"]["field"].items())},
        "pressure": result["state"]["causes"],
        "attributed_claim_ids": result["state"].get("attributed_claim_ids", []),
        "self_hypothesis_ids": result["state"].get("self_hypothesis_ids", []),
        "oracle_only": bool(result["oracle"]),
        "candidate_memory_ids": [m["id"] for m in result["memory_pointers"]],
        "neural": result["state"].get("neural"),
    }


def run_trajectory(fixture, scenario, seed, condition):
    cfg = config_for(condition, seed)
    label = "q7h2-neutral" if condition == "neutral_symbol" else "amber-sigil"
    records = []
    guard = {"hearsay_admission_rejected": False}
    with NoeticEngine(":memory:", cfg) as engine:
        for item in fixture["observations"]:
            first = bool(item.get("initial"))
            text = item["text"].replace("{speaker}", scenario["speaker"]).replace(
                "{quote}", scenario["quote"])
            actor = scenario["actor"] if item["actor"] == "participant" else item["actor"]
            event = Observation(
                origin_id=scenario["id"] + ":" + item["id"],
                subject_id=(item.get("subject") or cfg.subject_id),
                actor_id=actor,
                text=text, source="synthetic-matrix-v01",
                evidence_class=EvidenceClass(item["class"]),
                affect_delta=(scenario["initial_affect"] if first else item.get("affect_delta", {})),
                relationship_delta=(scenario["relationship_delta"] if first else 0.0),
                cue=label if item.get("use_symbol") else "",
            )
            result = engine.step(event, item.get("allowed"), seed=seed)
            records.append(step_record(item["id"], result))
            if first:
                engine.add_intention("ongoing-intention", "Preserve a meaningful goal",
                                     scenario["intention"], 0.95)
                source = event.origin_id
                cid = engine.add_social_claim(
                    source, scenario["actor"], cfg.subject_id,
                    scenario["predicate"], scenario["claim_valence"],
                    0.85, "direct_quote", scenario["quote"],
                )
                engine.review_social_claim(cid, "synthetic-reviewer",
                                           "admitted_for_policy")
                sid = engine.propose_self_hypothesis(
                    source, "values", scenario["self_tendency"], 0.8, 0.8,
                )
                engine.review_self_hypothesis(sid, "synthetic-reviewer",
                                              "corroborated_for_policy")
                engine.associate_symbol(label, scenario["symbol_tendency"],
                                        source, strength=0.24)
            if item["id"] == "rumor":
                cid = engine.add_social_claim(
                    event.origin_id, scenario["actor"], cfg.subject_id,
                    "fears", 1.0, 1.0, "third_party_report",
                )
                try:
                    engine.review_social_claim(cid, "synthetic-reviewer",
                                               "admitted_for_policy")
                except InvalidEvidence:
                    guard["hearsay_admission_rejected"] = True
                else:
                    raise AssertionError("hearsay promoted to policy without witnessed support")
            if "outcome_reward" in item:
                engine.record_outcome(result["decision_id"],
                                      item["outcome_reward"],
                                      authority="operator_scored")
            pulse = fixture["after_event"].get(item["id"])
            if pulse:
                p = engine.pulse(seed=seed + pulse["seed_offset"],
                                 mode=pulse["mode"])
                records.append(step_record("pulse:" + pulse["mode"], p))
        status = engine.status()
        if not status["verified_audit_hashes"]:
            raise AssertionError("ledger digest verification failed")
        return {
            "scenario": scenario["id"], "seed": seed, "condition": condition,
            "configuration": asdict(cfg), "steps": records,
            "guard": guard, "observations": status["memories"],
            "oracle_hypotheses": status["oracle_hypotheses"],
            "social_claims": status["social_claims"],
            "self_hypotheses": status["self_hypotheses"],
            "final_field": status["field"],
            "neural_field": status["neural_field"],
            "verified_audit_hashes": status["verified_audit_hashes"],
        }


def difference(reference, comparison):
    a, b = reference["steps"], comparison["steps"]
    if len(a) != len(b) or any(x["step"] != y["step"] for x, y in zip(a,b)):
        raise AssertionError("pairing failed, unequal event schedule")
    if any(set(x["scores"]) != set(y["scores"]) for x, y in zip(a,b)):
        raise AssertionError("unequal action candidates")
    score_l1 = []
    field_l1 = []
    changes = []
    for x,y in zip(a,b):
        score_l1.append(sum(abs(x["scores"][k] - y["scores"][k])
                            for k in x["scores"]))
        field_l1.append(sum(abs(x["field"][k] - y["field"][k])
                            for k in x["field"]))
        changes.append(int(x["action"] != y["action"]))
    return {
        "case": reference["scenario"] + ":" + str(reference["seed"]),
        "score_l1_mean": round(mean(score_l1), 9),
        "field_l1_mean": round(mean(field_l1), 9),
        "action_change_rate": round(mean(changes), 9),
        "action_changes": sum(changes),
        "step_count": len(a),
    }


def ci_95(samples, seed=2026, draws=1500):
    # Exploratory within-fixture descriptive bootstrap, not population inference.
    rng = random.Random(seed)
    n = len(samples)
    results = sorted(mean(samples[rng.randrange(n)] for _ in range(n))
                     for _ in range(draws))
    return [round(results[int(0.025*draws)], 9),
            round(results[int(0.975*draws)-1], 9)]


def execute(fixture_path=FIXTURE_PATH):
    fixture, fixture_sha = load_fixture(fixture_path)
    rows = []
    for scenario in fixture["scenarios"]:
        for seed in fixture["seeds"]:
            for condition in CONDITIONS:
                rows.append(run_trajectory(fixture, scenario, seed, condition))
    by_key={(x["scenario"],x["seed"],x["condition"]):x for x in rows}
    summary = {}
    cases = []
    for condition in CONDITIONS:
        if condition == "full":
            continue
        per = []
        for scenario in fixture["scenarios"]:
            for seed in fixture["seeds"]:
                ref=by_key[(scenario["id"],seed,"full")]
                alt=by_key[(scenario["id"],seed,condition)]
                paired = difference(ref, alt)
                paired["condition"] = condition
                per.append(paired)
                cases.append(paired)
        summary[condition]={
            "paired_trajectories":len(per),
            "total_steps":sum(x["step_count"] for x in per),
            "action_changes":sum(x["action_changes"] for x in per),
            "mean_score_l1":round(mean(x["score_l1_mean"] for x in per),9),
            "mean_score_l1_exploratory_bootstrap_interval":ci_95(
                [x["score_l1_mean"] for x in per]),
            "action_change_fraction":round(
                sum(x["action_changes"] for x in per)/
                sum(x["step_count"] for x in per),9),
            "mean_field_l1":round(mean(x["field_l1_mean"] for x in per),9),
        }
    for name in ("no_oracle","neutral_symbol"):
        if summary[name]["mean_score_l1"] != 0 or summary[name]["action_changes"] != 0:
            raise AssertionError(name+" altered policy despite the prespecified null")
    if not all(x["guard"]["hearsay_admission_rejected"] for x in rows):
        raise AssertionError("untrusted social claim admission was not consistently rejected")
    return {
        "protocol":"noetic-field-matrix-v01",
        "evidence_class":"synthetic_engineering_diagnostic_not_identity_efficacy",
        "fixture_sha256":fixture_sha,
        "model_renderer":"none",
        "code_version":"PR-stacked-on-v0.2; record exact commit SHA from CI",
        "fixed_seeds":fixture["seeds"],
        "scenario_names":[s["id"] for s in fixture["scenarios"]],
        "conditions":CONDITIONS,
        "aggregate":summary,
        "paired_case_metrics":cases,
        "full_case_level_trajectories":rows,
        "limitations":(
            "Fixture generated by the implementer, no human blinded scoring, "
            "synthetic unverified outcomes, no known correct actions; "
            "do not interpret ablation difference as higher behavioral quality."
        ),
    }


def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--fixture",default=str(FIXTURE_PATH))
    parser.add_argument("--output",required=True)
    args=parser.parse_args(argv)
    result=execute(args.fixture)
    output=Path(args.output)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,sort_keys=True,indent=2,
                                 ensure_ascii=False,allow_nan=False)+"\n")
    print(json.dumps({"protocol":result["protocol"],"fixture_sha256":result["fixture_sha256"],
                      "trajectories":len(result["full_case_level_trajectories"]),
                      "paired_cases":len(result["paired_case_metrics"]),
                      "result_file":str(output),"aggregate":result["aggregate"]},
                     sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
