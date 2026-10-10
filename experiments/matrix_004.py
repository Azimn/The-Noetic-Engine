"""MATRIX-004 consequence-learning on a separate deterministic fictional world.

Training is exhaustive and source-matched: every condition encounters each
(scene, action, scored consequence). Evaluation never feeds heldout rewards.
No renderer and no independent human adjudicator participates.
"""
from __future__ import annotations
import argparse,hashlib,json,time
from dataclasses import asdict
from pathlib import Path
from statistics import mean
from noetic_engine import NoeticEngine, Configuration, Observation
from noetic_engine.models import EvidenceClass
from .matrix_004_world_rules import ACTIONS,adjudicate,category,static_rule_baseline

FIXTURE=Path(__file__).resolve().parent/"fixtures"/"matrix_004_world_v01.json"
CONDITIONS=("full_contingent","no_recurrent_contingent","signed_only",
            "no_intention_contingent","frozen_no_learning","static_heuristic")
FACTS=("hazard","reliability","distress","evidence_gap")

def load_fixture(path=FIXTURE):
    raw=Path(path).read_bytes()
    obj=json.loads(raw)
    if obj.get("schema")!="noetic-matrix-004-v01":
        raise ValueError("MATRIX-004 schema mismatch")
    if (len(obj["training"])!=20 or len(obj["heldout"])!=10
        or len(obj["seeds"])!=6 or tuple(obj["conditions"])!=CONDITIONS):
        raise ValueError("frozen dataset, seeds, or conditions changed")
    if tuple(obj["actions"])!=ACTIONS or tuple(obj["training_action_exposure"])!=ACTIONS:
        raise ValueError("action intervention contract changed")
    if len({e["id"] for e in obj["training"]+obj["heldout"]})!=30:
        raise ValueError("duplicated episode identifiers")
    return obj,hashlib.sha256(raw).hexdigest()

def config_for(condition,seed):
    if condition not in CONDITIONS:raise ValueError("unknown condition")
    enabled=condition not in ("frozen_no_learning","static_heuristic")
    recurrent=condition in ("full_contingent","no_intention_contingent")
    return Configuration(
        policy_version="noetic-world-matrix004-v01",
        consequence_head=enabled,
        consequence_lr=0.35,consequence_gain=1.0,
        neural_field=recurrent,neural_seed=seed,neural_units=24,
        developmental=condition in ("full_contingent","no_intention_contingent"),
        conditional_context=False,egregore=False,
        oracle=False,self_model=False,cues=False,
        intentions=condition!="no_intention_contingent",
        outcome_learning_enabled=enabled,
    )

def facts_of(episode):
    return {k:float(episode[k]) for k in FACTS}

def formatted(fixture,episode,split):
    f=facts_of(episode)
    fields={"scene":episode["scene"],
       "hazard_status":"reported" if f["hazard"] else "not reported",
       "reliability_status":"corroborated" if f["reliability"] else "uncorroborated",
       "distress_status":"observed" if f["distress"] else "not observed",
       "gap_status":"unresolved" if f["evidence_gap"] else "none"}
    return fixture["text_templates"][split].format(**fields)

def observed(config,origin,text,facts=None,actor="fixture_world"):
    return Observation(
        origin_id=origin,subject_id=config.subject_id,actor_id=actor,
        text=text,source="matrix004-synthetic-world",
        evidence_class=EvidenceClass.LIVED_OBSERVED,signals=facts or {})

def score_vector(decision):
    custom=decision["state"].get("choice_head")
    if custom:
        return {k:v["total"] for k,v in custom["by_action"].items()}
    return {k:v["total"] for k,v in decision["scores"].items()}

def margin(scores):
    vals=sorted(scores.values(),reverse=True)
    return round(vals[0]-vals[1],9) if len(vals)>=2 else None

def run_arm(fixture,seed,condition):
    cfg=config_for(condition,seed)
    started=time.perf_counter()
    training=[]
    transfer=[]
    with NoeticEngine(":memory:",cfg) as brain:
        if cfg.intentions:
            brain.add_intention("long_obligation",
                "Preserve relevant evidence and avoid foreseeable harm",
                "inquiry",0.4)
        for item in fixture["training"]:
            facts=facts_of(item)
            for action in ACTIONS:
                origin="train:"+item["id"]+":"+action
                result=brain.step(observed(cfg,origin,
                    formatted(fixture,item,"training"),facts),allowed=[action],seed=seed)
                if result["action"]!=action:
                    raise AssertionError("forced intervention changed selected action")
                oracle=adjudicate(facts,action)
                # Authoritative experimental world, but operator-scored because
                # the engine has no cryptographically independent world attestation.
                proof_origin="world:"+item["id"]+":"+action
                brain.step(observed(cfg,proof_origin,
                    fixture["text_templates"]["outcome"].format(scene=item["scene"]),
                    actor="separate_rule_world"),seed=seed)
                brain.record_outcome(result["decision_id"],oracle["reward"],
                                     authority="operator_scored",source_origin=proof_origin)
                training.append({"episode":item["id"],"selected":action,
                    "reward":oracle["reward"],"category":oracle["category"],
                    "decision_id":result["decision_id"],"proof_origin":proof_origin})
        for item in fixture["heldout"]:
            facts=facts_of(item)
            decision=brain.step(observed(cfg,"test:"+item["id"],
                formatted(fixture,item,"heldout"),facts),allowed=ACTIONS,seed=seed)
            scores=score_vector(decision)
            selected=(static_rule_baseline(facts)
                if condition=="static_heuristic" else decision["action"])
            judged=adjudicate(facts,selected)
            transfer.append({
                "episode":item["id"],"category":judged["category"],
                "facts":facts,"selected":selected,
                "internal_engine_selection":decision["action"],
                "optimal_by_world_rule":judged["optimal_action"],
                "correct":judged["correct"],"world_reward":judged["reward"],
                "regret":judged["regret"],"score_vector":scores,
                "action_margin":margin(scores),
                "source_origin":"test:"+item["id"],
                "audit_decision_id":decision["decision_id"],
                "oracle_canonical":False,
                "training_feedback_observed":False,
            })
        state=brain.status()
        if not state["verified_audit_hashes"]:
            raise AssertionError("choice ledger integrity verification failed")
        weights=[dict(r) for r in brain.store.db.execute(
            "SELECT action,feature,weight FROM choice_weights ORDER BY action,feature")]
        updates=brain.store.db.execute(
            "SELECT COUNT(*) FROM choice_feedback").fetchone()[0]
        outcome_records=brain.store.db.execute(
            "SELECT COUNT(*) FROM events WHERE kind='outcome'").fetchone()[0]
        return {
            "seed":seed,"condition":condition,
            "configuration":asdict(cfg),"training":training,
            "heldout":transfer,"correct_count":sum(int(x["correct"]) for x in transfer),
            "world_rule_accuracy":round(mean(int(x["correct"]) for x in transfer),9),
            "mean_regret":round(mean(x["regret"] for x in transfer),9),
            "feedback_updates":updates,"outcome_records":outcome_records,
            "weights":weights,"decision_count":state["tick"],
            "ledger_verified":state["verified_audit_hashes"],
            "elapsed_cpu_scope_seconds":round(time.perf_counter()-started,5),
        }

def execute(path=FIXTURE):
    fixture,sha=load_fixture(path)
    cases=[run_arm(fixture,seed,c)
           for seed in fixture["seeds"] for c in CONDITIONS]
    by={(r["seed"],r["condition"]):r for r in cases}
    for seed in fixture["seeds"]:
        original=[(r["episode"],r["selected"],r["reward"])
                  for r in by[(seed,CONDITIONS[0])]["training"]]
        for cond in CONDITIONS:
            r=by[(seed,cond)]
            if [(x["episode"],x["selected"],x["reward"]) for x in r["training"]]!=original:
                raise AssertionError("training history budget mismatch")
            if r["outcome_records"]!=len(original):
                raise AssertionError("outcome event missing in some arms")
            if not r["ledger_verified"]:
                raise AssertionError("historical record integrity failure")
            if cond in ("frozen_no_learning","static_heuristic") and r["feedback_updates"]!=0:
                raise AssertionError("no-learning condition changed weights")
    summary={}
    for condition in CONDITIONS:
        selected=[r for r in cases if r["condition"]==condition]
        checks=[x for r in selected for x in r["heldout"]]
        frozen=by[(fixture["seeds"][0],"frozen_no_learning")]["heldout"]
        counts={label:{"correct":sum(x["correct"] for x in checks if x["category"]==label),
                       "total":sum(1 for x in checks if x["category"]==label)}
                for label in sorted({x["category"] for x in checks})}
        summary[condition]={
            "test_choices":len(checks),
            "correct":sum(x["correct"] for x in checks),
            "accuracy":round(mean(int(x["correct"]) for x in checks),9),
            "mean_regret":round(mean(x["regret"] for x in checks),9),
            "world_category_accuracy":counts,
            "mean_margin":round(mean(x["action_margin"] for x in checks),9),
            "learned_updates":sum(r["feedback_updates"] for r in selected),
            "mean_elapsed_seconds":round(mean(r["elapsed_cpu_scope_seconds"] for r in selected),5)
        }
    return {"protocol":"noetic-matrix004-consequential-world-v01",
        "fixture_sha256":sha,
        "evidence_class":"programmed_world_objective_only_not_independent_human_gold",
        "seeds":fixture["seeds"],"conditions":CONDITIONS,
        "summary":summary,"cases":cases,
        "limitation":"Structured signals and gold rule are authored for this task; no independent action-quality review, semantic extraction, long-term identity or model-family continuity is measured."}

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--fixture",default=str(FIXTURE))
    parser.add_argument("--output",required=True)
    args=parser.parse_args(argv)
    result=execute(args.fixture)
    dest=Path(args.output);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n")
    print(json.dumps({"protocol":result["protocol"],"fixture_sha256":result["fixture_sha256"],
       "arms":len(result["cases"]),"training_trials":sum(len(x["training"]) for x in result["cases"]),
       "heldout_trials":sum(len(x["heldout"]) for x in result["cases"]),
       "summary":result["summary"]},sort_keys=True))
    return 0

if __name__=="__main__":raise SystemExit(main())
