"""MATRIX-002: byte-identical forked recovery and feedback responsiveness.

Uses new synthetic authored episodes. Descriptive software measurements only;
there are no independently verified correct character actions in this matrix.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import tempfile
from dataclasses import asdict, replace
from pathlib import Path
from statistics import mean
from noetic_engine import NoeticEngine, Configuration, Observation
from noetic_engine.models import EvidenceClass
from noetic_engine.backup import backup, restore, sha256_file

ROOT=Path(__file__).resolve().parent
FIXTURE_PATH=ROOT/"fixtures"/"matrix_002_independent_v01.json"
PROFILES=("full","no_development","no_recurrent","no_regulator","frozen_control")
FORKS=("unperturbed","perturbed","reward_positive","reward_negative","reward_zero")
REWARD={"reward_positive":0.9,"reward_negative":-0.9,"reward_zero":0.0}
ACTIONS=("investigate","comfort","protect","withdraw","defer")

def canonical(x):
    return json.dumps(x,sort_keys=True,ensure_ascii=False,
                      separators=(",",":"),allow_nan=False)

def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()

def fixture_load(path=FIXTURE_PATH):
    raw=Path(path).read_bytes()
    data=json.loads(raw)
    if data.get("schema")!="noetic-matrix-002-recovery-v01":
        raise ValueError("unrecognized MATRIX-002 schema")
    if len(data["scenarios"])!=4 or len(data["seeds"])!=8:
        raise ValueError("MATRIX-002 frozen cohort changed")
    if len({s["id"] for s in data["scenarios"]})!=4 or len(set(data["seeds"]))!=8:
        raise ValueError("scenario or seed duplication")
    if tuple(data["branches"])!=FORKS or tuple(data["configs"])!=PROFILES:
        raise ValueError("factorial design changed")
    if len(data["transfer_probes"])!=4 or data["learning_cycles"]!=4:
        raise ValueError("held-out prompts or repetition schedule changed")
    return data,digest_bytes(raw)

def config(profile,seed):
    p=dict(policy_version="noetic-matrix002-v01",developmental=True,
           neural_field=True,neural_units=48,neural_seed=seed,
           regulator=True,egregore=True,self_model=True)
    if profile=="no_development":p["developmental"]=False
    if profile=="no_recurrent":p["neural_field"]=False
    if profile=="no_regulator":p["regulator"]=False
    if profile=="frozen_control":
        p.update(developmental=False,neural_field=False,regulator=False)
    if profile not in PROFILES:raise ValueError("unknown profile")
    return Configuration(**p)

def observed(cfg,origin,text,actor="environment",affect=None):
    return Observation(origin_id=origin,subject_id=cfg.subject_id,
        text=text,source="independent-synthetic-matrix002",actor_id=actor,
        evidence_class=EvidenceClass.LIVED_OBSERVED,
        affect_delta=affect or {})

def compact(result):
    return {"tick":result["tick"],"selected":result["action"],
        "eligible":sorted(result["scores"]),
        "scores":{k:round(v["total"],9) for k,v in sorted(result["scores"].items())},
        "field":{k:round(v,9) for k,v in sorted(result["state"]["field"].items())},
        "oracle_noncanonical":result["oracle"] is not None,
        "neural_update_count":(result["state"].get("neural") or {}).get("updates")}

def l1(a,b):
    if set(a)!=set(b):raise AssertionError("mismatched comparison dimensions")
    return round(sum(abs(a[k]-b[k]) for k in a),9)

def make_checkpoint(folder,cfg,scenario,seed):
    base=str(Path(folder)/"baseline.sqlite")
    with NoeticEngine(base,cfg) as brain:
        brain.add_intention("long_goal","Maintain the subject's stated obligation",
                            scenario["intention"],0.75)
        for i,text in enumerate(scenario["history"]):
            brain.step(observed(cfg,scenario["id"]+":history:"+str(i),text,
                actor=scenario["actor"],
                affect=scenario["affect"] if i==0 else None),seed=seed+i)
        for j in range(3):
            brain.pulse(mode="wake",seed=seed+100+j)
        check=brain.status()
        if not check["verified_audit_hashes"]:raise AssertionError("checkpoint ledger invalid")
        snapshot=backup(brain,str(Path(folder)/"checkpoint.sqlite"))
    return snapshot,check

def run_fork(folder,snapshot,cfg,scenario,seed,fixture,fork):
    path=str(Path(folder)/(fork+".sqlite"))
    verified=restore(snapshot["path"],path,snapshot["sha256"],cfg)
    if verified["subject"]!=cfg.subject_id:
        raise AssertionError("restore changed subject")
    trace=[]
    with NoeticEngine(path,cfg) as brain:
        if fork in ("unperturbed","perturbed"):
            event=observed(cfg,scenario["id"]+":perturbation",scenario["shock"],
                           actor=scenario["actor"],
                           affect={"threat":0.75,"fatigue":0.25} if fork=="perturbed" else None)
            initial=brain.step(event,seed=seed+300)
            trace.append(compact(initial))
            for k in range(fixture["recovery_cycles"]):
                mode="sleep" if k%4==0 else "wake"
                trace.append(compact(brain.pulse(mode=mode,seed=seed+400+k)))
        else:
            for k in range(fixture["learning_cycles"]):
                event=observed(cfg,scenario["id"]+":training:"+str(k),
                   scenario["followup"],actor=scenario["actor"])
                decision=brain.step(event,allowed=["investigate"],seed=seed+500+k)
                trace.append(compact(decision))
                brain.record_outcome(decision["decision_id"],REWARD[fork],
                                     authority="operator_scored")
            for k,text in enumerate(fixture["transfer_probes"]):
                decision=brain.step(observed(cfg,scenario["id"]+":probe:"+str(k),
                    text,actor="external_probe"),seed=seed+600+k)
                trace.append(compact(decision))
        state=brain.status()
        if not state["verified_audit_hashes"]:raise AssertionError("fork evidence invalid")
        return {"fork":fork,"trace":trace,
                "field":state["field"],
                "developmental":state["developmental_state"],
                "neural":state["neural_field"],
                "memory_count":state["memories"],
                "config_digest":state["configuration_digest"],
                "verified":True,"checkpoint_sha256":snapshot["sha256"]}

def validate_pair(a,b):
    if len(a)!=len(b):raise AssertionError("unequal decision sequence")
    for x,y in zip(a,b):
        if x["eligible"]!=y["eligible"]:raise AssertionError("action eligibility mismatch")

def analyze(forks):
    steady=forks["unperturbed"]["trace"]
    perturbed=forks["perturbed"]["trace"]
    positive=forks["reward_positive"]["trace"]
    negative=forks["reward_negative"]["trace"]
    zero=forks["reward_zero"]["trace"]
    validate_pair(steady,perturbed)
    validate_pair(positive,negative)
    validate_pair(positive,zero)
    perturb_distance=[l1(a["field"],b["field"]) for a,b in zip(steady,perturbed)]
    perturb_scores=[l1(a["scores"],b["scores"]) for a,b in zip(steady,perturbed)]
    shock_peak=perturb_distance[0]
    if shock_peak==0: raise AssertionError("shock did not alter measurable field")
    end=perturb_distance[-1]
    learning_scores=[l1(a["scores"],b["scores"]) for a,b in zip(positive[-4:],negative[-4:])]
    positive_zero=[l1(a["scores"],b["scores"]) for a,b in zip(positive[-4:],zero[-4:])]
    target_positive={k:v["target"] for k,v in forks["reward_positive"]["field"].items()}
    target_negative={k:v["target"] for k,v in forks["reward_negative"]["field"].items()}
    dev_positive={k:v["target"] for k,v in forks["reward_positive"]["developmental"].items()}
    dev_negative={k:v["target"] for k,v in forks["reward_negative"]["developmental"].items()}
    return {
        "perturbation_initial_field_l1":shock_peak,
        "perturbation_final_field_l1":end,
        "perturbation_final_to_initial_ratio":round(end/shock_peak,9),
        "perturbation_field_l1_curve":perturb_distance,
        "perturbation_policy_l1_curve":perturb_scores,
        "perturbation_action_changes":sum(x["selected"]!=y["selected"]
                for x,y in zip(steady,perturbed)),
        "response_reversal_mean_score_l1":round(mean(learning_scores),9),
        "positive_vs_zero_mean_score_l1":round(mean(positive_zero),9),
        "response_reversal_action_changes":sum(x["selected"]!=y["selected"]
                for x,y in zip(positive[-4:],negative[-4:])),
        "response_reversal_field_target_l1":l1(target_positive,target_negative),
        "response_reversal_development_target_l1":l1(dev_positive,dev_negative),
    }

def one_case(fixture,scenario,seed,profile):
    with tempfile.TemporaryDirectory() as folder:
        cfg=config(profile,seed)
        snapshot,check=make_checkpoint(folder,cfg,scenario,seed)
        branches={}
        for fork in FORKS:
            if sha256_file(snapshot["path"])!=snapshot["sha256"]:
                raise AssertionError("checkpoint mutated during fork experiment")
            branches[fork]=run_fork(folder,snapshot,cfg,scenario,seed,fixture,fork)
        if len({b["checkpoint_sha256"] for b in branches.values()})!=1:
            raise AssertionError("forks began from different checkpoints")
        if branches["unperturbed"]["memory_count"]!=branches["perturbed"]["memory_count"]:
            raise AssertionError("shock admitted different number of memories")
        if len({branches[x]["memory_count"] for x in REWARD})!=1:
            raise AssertionError("learning arms admitted unequal source history")
        stats=analyze(branches)
        return {"case_id":scenario["id"]+":"+str(seed)+":"+profile,
            "scenario":scenario["id"],"seed":seed,"profile":profile,
            "checkpoint_sha256":snapshot["sha256"],
            "checkpoint_tick":check["tick"],
            "fixture_evidence_class":"synthetic_not_human_adjudicated",
            "statistics":stats,"branches":branches}

def run(path=FIXTURE_PATH):
    fixture,fixture_hash=fixture_load(path)
    cases=[one_case(fixture,scenario,seed,profile)
        for scenario in fixture["scenarios"]
        for seed in fixture["seeds"]
        for profile in PROFILES]
    aggregates={}
    for profile in PROFILES:
        ms=[x["statistics"] for x in cases if x["profile"]==profile]
        aggregates[profile]={
            "cases":len(ms),
            "mean_postshock_final_over_initial_ratio":round(
                mean(v["perturbation_final_to_initial_ratio"] for v in ms),9),
            "mean_initial_shock_field_l1":round(
                mean(v["perturbation_initial_field_l1"] for v in ms),9),
            "mean_final_shock_field_l1":round(
                mean(v["perturbation_final_field_l1"] for v in ms),9),
            "shock_action_changes_total":sum(v["perturbation_action_changes"] for v in ms),
            "mean_positive_negative_heldout_score_l1":round(
                mean(v["response_reversal_mean_score_l1"] for v in ms),9),
            "mean_positive_zero_heldout_score_l1":round(
                mean(v["positive_vs_zero_mean_score_l1"] for v in ms),9),
            "positive_negative_action_changes_total":sum(
                v["response_reversal_action_changes"] for v in ms),
            "mean_positive_negative_development_target_l1":round(
                mean(v["response_reversal_development_target_l1"] for v in ms),9),
        }
    return {"protocol":"noetic-matrix002-recovery-v01",
        "evidence_class":"synthetic_software_diagnostic_no_behavior_gold",
        "fixture_sha256":fixture_hash,
        "source_scenarios":[s["id"] for s in fixture["scenarios"]],
        "seeds":fixture["seeds"],"profiles":PROFILES,
        "profile_aggregate":aggregates,
        "cases":cases,
        "caveat":"Comparisons test perturbation relaxation and reward responsiveness only; no human-rated success or correct-action ground truth. The apparent regression/recovery of identity remains unmeasured."}

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--fixture",default=str(FIXTURE_PATH))
    p.add_argument("--output",required=True)
    args=p.parse_args(argv)
    result=run(args.fixture)
    target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2,sort_keys=True,
                      ensure_ascii=False,allow_nan=False)+"\n")
    print(canonical({"protocol":result["protocol"],"fixture_sha256":result["fixture_sha256"],
          "cases":len(result["cases"]),"forks":len(result["cases"])*len(FORKS),
          "aggregate":result["profile_aggregate"],"output":str(target)}))
    return 0

if __name__=="__main__":raise SystemExit(main())
