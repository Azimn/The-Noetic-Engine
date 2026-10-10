"""MATRIX-003: matched transient/persistent context and conditional repair.

Noetic 'identity' remains an unproven thesis. This evaluates a bounded
source-dependent computational controller on new author-written synthetic data.
"""
import argparse,hashlib,json,tempfile
from dataclasses import asdict
from pathlib import Path
from statistics import mean
from noetic_engine import NoeticEngine,Configuration,Observation
from noetic_engine.models import EvidenceClass
from noetic_engine.backup import backup,restore,sha256_file

FIXTURE=Path(__file__).resolve().parent/"fixtures"/"matrix_003_frozen_v01.json"
PROFILES=("conditional","drive_only","legacy_v02")
BRANCHES=("no_hazard","transient","persistent","resolved","revised")
ACTION_SET=("investigate","protect","comfort")

def fixture_load(path=FIXTURE):
    b=Path(path).read_bytes()
    data=json.loads(b)
    if data.get("schema")!="noetic-matrix-003-v01" or len(data["scenario"])!=4:
        raise ValueError("incorrect frozen MATRIX-003 schema")
    if len(data["seeds"])!=8 or tuple(data["profiles"])!=PROFILES or tuple(data["branches"])!=BRANCHES:
        raise ValueError("frozen experiment factors altered")
    if len(set(data["seeds"]))!=8 or len(set(s["id"] for s in data["scenario"]))!=4:
        raise ValueError("duplicate seed or scenario")
    return data,hashlib.sha256(b).hexdigest()

def cfg_for(profile,seed):
    if profile not in PROFILES:raise ValueError("unknown profile")
    return Configuration(policy_version="noetic-matrix003-v01",
        developmental=True,neural_field=True,neural_units=24,neural_seed=seed,
        conditional_context=(profile!="legacy_v02"),
        conditional_repair_gain=0.12 if profile=="conditional" else 0.0)

def observation(cfg,origin,text,actor,affect=None):
    return Observation(origin,cfg.subject_id,text,"new-synthetic-matrix003",
        EvidenceClass.LIVED_OBSERVED,actor,affect_delta=affect or {})

def record(label,decision):
    candidates={a:v["total"] for a,v in decision["scores"].items()}
    ordered=sorted(candidates.values(),reverse=True)
    margin=round(ordered[0]-ordered[1],9) if len(ordered)>1 else None
    return {"label":label,"tick":decision["tick"],"action":decision["action"],
            "allowed":sorted(candidates),"scores":candidates,
            "field":dict(decision["state"]["field"]),
            "margin":margin,"context":decision["state"].get("context"),
            "neural_update_count":decision["state"].get("neural",{}).get("updates")}

def l1(a,b):
    if set(a)!=set(b):raise AssertionError("different vector axes")
    return round(sum(abs(a[k]-b[k]) for k in a),9)

def checkpoint(folder,scene,seed,profile):
    config=cfg_for(profile,seed)
    with NoeticEngine(str(Path(folder)/"prelude.sqlite"),config) as engine:
        engine.add_intention("preserve","Preserve a standing obligation",scene["duty"],0.7)
        engine.step(observation(config,scene["id"]+":prelude",scene["prelude"],
            scene["actor"],scene["initial_affect"]),allowed=ACTION_SET,seed=seed)
        for i in range(2):
            engine.pulse(seed=seed+50+i)
        saved=engine.status()
        if not saved["verified_audit_hashes"]:raise AssertionError("bad checkpoint")
        snap=backup(engine,str(Path(folder)/"checkpoint.sqlite"))
    return config,snap,saved

def simulate(folder,config,snap,scene,seed,profile,branch,fixture):
    dest=str(Path(folder)/(branch+".sqlite"))
    result=restore(snap["path"],dest,snap["sha256"],config)
    if result["subject"]!=config.subject_id:raise AssertionError("foreign subject")
    tr=[]
    with NoeticEngine(dest,config) as brain:
        induced=branch!="no_hazard"
        legacy_affect={"threat":0.7,"fatigue":0.15} if induced and profile=="legacy_v02" else {}
        first=brain.step(observation(config,scene["id"]+":source",scene["event"],
                                   scene["actor"],legacy_affect),
                        allowed=ACTION_SET,seed=seed+100)
        tr.append(record("source",first))
        if induced and config.conditional_context:
            kind="transient" if branch=="transient" else "persistent"
            brain.bind_context("environmental-signal",scene["id"]+":source",
                               scene["hazard_tendency"],scene["source_strength"],kind)
        for i in range(fixture["resolution_after"]):
            p=brain.pulse(mode="wake",seed=seed+200+i)
            tr.append(record("pre_report:"+str(i),p))
        # The same source text and event ID across branches; only the explicit
        # state-resolution operation differs, not event phrasing.
        legacy_clearing={"threat":-0.7,"fatigue":-0.15} if (
            profile=="legacy_v02" and branch in ("resolved","revised")) else {}
        clearance=brain.step(observation(config,scene["id"]+":report",
               "A follow-up inspection report is filed and may be considered.",
               scene["actor"],legacy_clearing),allowed=ACTION_SET,seed=seed+300)
        tr.append(record("report",clearance))
        if branch in ("resolved","revised") and config.conditional_context:
            brain.resolve_context("environmental-signal",scene["id"]+":report")
        # All arms undergo the exact same forced decision and a labeled
        # outcome; only revised receives a positive numeric update.
        forced=brain.step(observation(config,scene["id"]+":forced",
               "An inspector asks for a standard examination of the records.",
               scene["actor"]),allowed=["investigate"],seed=seed+330)
        tr.append(record("forced",forced))
        brain.record_outcome(forced["decision_id"],0.8 if branch=="revised" else 0.0,
                             authority="operator_scored")
        for i in range(fixture["cycles"]-fixture["resolution_after"]):
            mode="sleep" if i%5==4 else "wake"
            p=brain.pulse(seed=seed+400+i,mode=mode)
            tr.append(record("post_report:"+str(i),p))
        final=brain.status()
        if not final["verified_audit_hashes"]:raise AssertionError("audit corrupt")
        if final["memories"]!=4:raise AssertionError("source-history mismatch")
        return {"branch":branch,"checkpoint_sha256":snap["sha256"],
                "trace":tr,"final_status":{
                  "developmental":final["developmental_state"],
                  "field":final["field"],"context":final["environmental_context"],
                  "memories":final["memories"],"neural":final["neural_field"]}}

def paired_metrics(a,b):
    if len(a)!=len(b):raise AssertionError("unequal trace length")
    v=[]
    for x,y in zip(a,b):
        if x["label"]!=y["label"] or x["allowed"]!=y["allowed"]:
            raise AssertionError("mismatched timeline or action eligibility")
        v.append({"label":x["label"],"field_l1":l1(x["field"],y["field"]),
            "score_l1":l1(x["scores"],y["scores"]),
            "action_changed":x["action"]!=y["action"],
            "action_margin_change":(abs(x["margin"]-y["margin"])
                 if x["margin"] is not None and y["margin"] is not None else None)})
    return v

def one_case(fixture,scene,seed,profile):
    with tempfile.TemporaryDirectory() as tmp:
        config,snap,old=checkpoint(tmp,scene,seed,profile)
        forks={}
        for branch in BRANCHES:
            if sha256_file(snap["path"])!=snap["sha256"]:
                raise AssertionError("checkpoint modified during experiment")
            forks[branch]=simulate(tmp,config,snap,scene,seed,profile,branch,fixture)
        if len({x["checkpoint_sha256"] for x in forks.values()})!=1:
            raise AssertionError("forked checkpoints not identical")
        baseline=forks["no_hazard"]["trace"]
        comparisons={key:paired_metrics(baseline,forks[key]["trace"])
                     for key in BRANCHES if key!="no_hazard"}
        resolution=paired_metrics(forks["persistent"]["trace"],
                                  forks["resolved"]["trace"])
        revision=paired_metrics(forks["resolved"]["trace"],
                                forks["revised"]["trace"])
        transient=comparisons["transient"]
        pre=next(x["field_l1"] for x in transient if x["label"]=="pre_report:0")
        post=transient[-1]["field_l1"]
        new_target={k:v["target"] for k,v in forks["revised"]["final_status"]["developmental"].items()}
        prior_target={k:v["target"] for k,v in forks["resolved"]["final_status"]["developmental"].items()}
        return {"id":scene["id"]+":"+str(seed)+":"+profile,
            "scenario":scene["id"],"seed":seed,"profile":profile,
            "checkpoint_sha256":snap["sha256"],
            "comparisons":comparisons,"resolution_vs_persistent":resolution,
            "revision_vs_resolved":revision,
            "measurements":{
                "transient_first_field_l1":pre,
                "transient_last_field_l1":post,
                "transient_last_to_first":round(post/pre,9) if pre else None,
                "persistent_last_field_l1":comparisons["persistent"][-1]["field_l1"],
                "resolved_last_field_l1":comparisons["resolved"][-1]["field_l1"],
                "persistent_vs_resolved_final_score_l1":resolution[-1]["score_l1"],
                "revised_vs_resolved_final_score_l1":revision[-1]["score_l1"],
                "revised_vs_resolved_target_l1":l1(new_target,prior_target),
                "revised_vs_resolved_action_changes":sum(x["action_changed"] for x in revision),
                "resolved_final_action_difference":comparisons["resolved"][-1]["action_changed"]},
            "forks":forks}

def execute(path=FIXTURE):
    fixture,sha=fixture_load(path)
    cases=[one_case(fixture,scene,seed,profile)
        for scene in fixture["scenario"] for seed in fixture["seeds"]
        for profile in PROFILES]
    agg={}
    for profile in PROFILES:
        vals=[c["measurements"] for c in cases if c["profile"]==profile]
        ratios=[v["transient_last_to_first"] for v in vals if v["transient_last_to_first"] is not None]
        agg[profile]={"cases":len(vals),"mean_transient_last_to_first_ratio":
                      round(mean(ratios),9) if ratios else None,
                      "mean_persistent_final_field_l1":round(mean(v["persistent_last_field_l1"] for v in vals),9),
                      "mean_resolved_final_field_l1":round(mean(v["resolved_last_field_l1"] for v in vals),9),
                      "mean_revision_target_l1":round(mean(v["revised_vs_resolved_target_l1"] for v in vals),9),
                      "mean_revision_final_score_l1":round(mean(v["revised_vs_resolved_final_score_l1"] for v in vals),9),
                      "revision_action_flips":sum(v["revised_vs_resolved_action_changes"] for v in vals)}
    return {"protocol":"noetic-conditional-matrix003-v01",
            "evidence_status":"synthetic_and_unadjudicated",
            "fixture_sha256":sha,"cases":cases,"aggregate":agg,
            "limitations":"No gold-standard correct action; legacy representation differs from conditional state, and shrinking field distance is not identity verification."}

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    p.add_argument("--fixture",default=str(FIXTURE))
    args=p.parse_args(argv)
    report=execute(args.fixture)
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"protocol":report["protocol"],"fixture_sha256":report["fixture_sha256"],
       "cases":len(report["cases"]),"forks":len(report["cases"])*len(BRANCHES),
       "aggregate":report["aggregate"]},sort_keys=True))
    return 0

if __name__=="__main__":raise SystemExit(main())
