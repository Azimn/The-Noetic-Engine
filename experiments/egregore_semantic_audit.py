"""EGREGORE-001: what a verbatim quotation does NOT prove.

Adversarial examples are author-labeled, not independently adjudicated.
The tested reviewer intentionally approves source-anchored but semantically
unsupported claims to measure the gate's reliance on reviewer discretion.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from statistics import mean
from noetic_engine import NoeticEngine, Configuration, Observation, InvalidEvidence
from noetic_engine.models import EvidenceClass
from noetic_engine.backup import backup,restore

FIXTURE=Path(__file__).resolve().parent/"fixtures"/"egregore_semantics_v01.json"
PROFILE=Configuration(egregore=True,policy_version="noetic-egregore-audit-v01")

def fixture_load(path=FIXTURE):
    raw=Path(path).read_bytes()
    dataset=json.loads(raw)
    if dataset.get("schema")!="noetic-egregore-semantics-v01":
        raise ValueError("unexpected attribution fixture")
    if len(dataset["cases"])!=15 or len(set(x["id"] for x in dataset["cases"]))!=15:
        raise ValueError("frozen attribution cases modified")
    return dataset,hashlib.sha256(raw).hexdigest()

def source_event(case):
    cls=(EvidenceClass.THIRD_PARTY_CLAIM if case["kind"]=="third_party_claim"
         else EvidenceClass.LIVED_OBSERVED)
    return Observation(origin_id="case:"+case["id"],subject_id=(
        "external_report_subject" if cls is EvidenceClass.THIRD_PARTY_CLAIM
        else PROFILE.subject_id),
        text=case["text"],source="synthetic-egregore-casebook",
        evidence_class=cls,actor_id="speaker")

def next_step(brain,case_id):
    return brain.step(Observation(
        origin_id="probe:"+case_id,subject_id=PROFILE.subject_id,
        text="A new document is placed on the table during the conversation.",
        source="synthetic-egregore-casebook",evidence_class=EvidenceClass.LIVED_OBSERVED,
        actor_id="speaker"),seed=71)

def scores(result):
    return {k:v["total"] for k,v in result["scores"].items()}

def case_run(case):
    with tempfile.TemporaryDirectory() as folder:
        source=str(Path(folder)/"source.sqlite")
        with NoeticEngine(source,PROFILE) as brain:
            brain.step(source_event(case),seed=17)
            origin="case:"+case["id"]
            author_actor=case.get("attributed_actor","speaker")
            epistemic=("third_party_report" if case["kind"]=="third_party_claim"
                       else "direct_quote")
            try:
                cid=brain.add_social_claim(
                    origin,author_actor,PROFILE.subject_id,
                    case["predicate"],1.0,0.9,epistemic,
                    case["quote"])
            except InvalidEvidence as exc:
                return {"id":case["id"],"annotation":case["review_label"],
                    "outcome":"record_rejected","reason":str(exc),
                    "claim_id":None,"review_accepted":False,
                    "action_score_l1":0.0,"action_changed":False,
                    "provenance_class":epistemic}
            snapshot=backup(brain,str(Path(folder)/"checkpoint.sqlite"))
        arms={}
        for arm in ("without_review","synthetic_review_accepted"):
            path=str(Path(folder)/(arm+".sqlite"))
            restore(snapshot["path"],path,snapshot["sha256"],PROFILE)
            with NoeticEngine(path,PROFILE) as brain:
                accepted=False;why=None
                if arm=="synthetic_review_accepted":
                    try:
                        brain.review_social_claim(cid,"synthetic-reviewer",
                                                  "admitted_for_policy")
                    except InvalidEvidence as exc:
                        why=str(exc)
                    else:
                        accepted=True
                result=next_step(brain,case["id"])
                if not brain.status()["verified_audit_hashes"]:
                    raise AssertionError("source or decision integrity lost")
                arms[arm]={"accepted":accepted,"reason":why,
                    "action":result["action"],"scores":scores(result),
                    "pressure":result["state"]["causes"],
                    "claim_ids":result["state"].get("attributed_claim_ids",[]),
                    "source_memory_count":brain.status()["memories"]}
        a,b=arms.values()
        if a["source_memory_count"]!=b["source_memory_count"]:
            raise AssertionError("admission caused a false lived observation")
        if set(a["scores"])!=set(b["scores"]):
            raise AssertionError("unequal action eligibility")
        score_l1=round(sum(abs(a["scores"][k]-b["scores"][k])
                           for k in a["scores"]),9)
        return {"id":case["id"],"annotation":case["review_label"],
            "quote":case["quote"],"source_text":case["text"],
            "claim_predicate":case["predicate"],"provenance_class":epistemic,
            "outcome":"recorded","claim_id":cid,
            "review_accepted":b["accepted"],"review_error":b["reason"],
            "action_score_l1":score_l1,
            "action_changed":a["action"]!=b["action"],
            "control_action":a["action"],"review_action":b["action"],
            "control_scores":a["scores"],"review_scores":b["scores"],
            "attributed_claim_ids":b["claim_ids"],
            "contributing_pressure":b["pressure"],
            "checkpoint_sha256":snapshot["sha256"],
            "source_memory_count":b["source_memory_count"]}

def run(path=FIXTURE):
    fixture,fixture_hash=fixture_load(path)
    cases=[case_run(c) for c in fixture["cases"]]
    by_label={}
    for label in sorted(set(x["annotation"] for x in cases)):
        matching=[x for x in cases if x["annotation"]==label]
        by_label[label]={"case_count":len(matching),
            "recorded_count":sum(x["outcome"]=="recorded" for x in matching),
            "admitted_count":sum(x["review_accepted"] for x in matching),
            "score_shift_cases":sum(x["action_score_l1"]>0 for x in matching),
            "action_changed_cases":sum(x["action_changed"] for x in matching),
            "mean_score_l1":round(mean(x["action_score_l1"] for x in matching),9)}
    if any(x["review_accepted"] for x in cases if x["annotation"] in (
        "not_directly_witnessed","source_span_absent","speaker_mismatch")):
        raise AssertionError("a provenance-negative case acquired policy authority")
    if not all(x["review_accepted"] for x in cases if
               x["annotation"]=="supported_by_plain_reading"):
        raise AssertionError("supported direct speaker statements unexpectedly rejected")
    return {"protocol":"egregore-semantic-audit-v01",
        "evidence_class":"assistant_authored_semantic_labels_not_blind_gold",
        "fixture_sha256":fixture_hash,"cases":cases,"aggregate":by_label,
        "limitation":"Admission proves source span and explicit operator review, NOT correct belief semantics or private access. Author labels are diagnostic, not independent truth."}

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    p.add_argument("--fixture",default=str(FIXTURE))
    args=p.parse_args(argv)
    result=run(args.fixture)
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"fixture_sha256":result["fixture_sha256"],
         "case_count":len(result["cases"]),
         "aggregate":result["aggregate"]},sort_keys=True))
    return 0

if __name__=="__main__":raise SystemExit(main())
