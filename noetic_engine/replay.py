"""Replay a complete Noetic event history into a fresh independent brain.

Only signed-off input operations are replayed. Derived records must match
byte-for-byte; missing v0.1 inputs fail rather than pretending reproducibility.
"""
import json,sqlite3
from dataclasses import asdict
from pathlib import Path
from .engine import NoeticEngine
from .models import Configuration,Observation,EvidenceClass
from .store import digest

def replay_database(source_path,destination_path):
    if source_path==destination_path or destination_path==":memory:":
        raise ValueError("replay requires distinct persistent paths")
    if Path(destination_path).exists():
        raise ValueError("destination must not exist")
    source=sqlite3.connect("file:"+str(Path(source_path).resolve())+"?mode=ro",uri=True)
    source.row_factory=sqlite3.Row
    try:
        events=[dict(r) for r in source.execute("SELECT * FROM events ORDER BY id")]
        if not events: raise ValueError("nothing to replay")
        for e in events:
            if digest(json.loads(e["payload"]))!=e["hash"]:
                raise ValueError("source event integrity failure")
        original=[dict(r) for r in source.execute("SELECT * FROM decisions ORDER BY id")]
        for d in original:
            if digest(json.loads(d["audit"]))!=d["hash"]:
                raise ValueError("source decision integrity failure")
        for r in source.execute("SELECT * FROM observations"):
            core={"origin_id":r["origin"],"subject_id":r["subject"],
                "actor_id":r["actor"],"evidence_class":r["class"],
                "source":r["source"],"text":r["text"]}
            if digest(core)!=r["hash"]:
                raise ValueError("source observation integrity failure")
        snapshots=[json.loads(e["payload"])["config_snapshot"] for e in events
                   if e["kind"] in ("observation","pulse_input") and "config_snapshot" in json.loads(e["payload"])]
        if not snapshots: raise ValueError("legacy ledger lacks complete replay configuration")
        config=Configuration(**snapshots[0])
        if any(snapshot!=snapshots[0] for snapshot in snapshots):
            raise ValueError("mixed controller configurations in a single ledger")
        authorities={json.loads(e["payload"])["decision_id"]:json.loads(e["payload"])
                     for e in events if e["kind"]=="outcome_authority"}
        with NoeticEngine(destination_path,config) as engine:
            for event in events:
                kind=event["kind"];p=json.loads(event["payload"])
                if kind=="intention_created":
                    engine.add_intention(p["id"],p["label"],p["tendency"],p["strength"])
                elif kind=="intention_resolved":
                    engine.resolve_intention(p["id"],p["status"])
                elif kind=="symbol_bound":
                    engine.associate_symbol(p["symbol"],p["tendency"],p["origin"],p["strength"])
                elif kind=="social_claim_recorded":
                    actual=engine.add_social_claim(p["origin"],p["attributed_actor"],
                        p["believed_subject"],p["predicate"],p["valence"],
                        p["confidence"],p["epistemic"],p.get("quotation"))
                    if actual!=p["id"]:raise ValueError("social claim ID divergence")
                elif kind=="social_claim_reviewed":
                    engine.review_social_claim(p["id"],p["reviewer"],p["disposition"])
                elif kind=="self_hypothesis":
                    actual=engine.propose_self_hypothesis(p["origin"],p["predicate"],
                        p["tendency"],p["valence"],p["confidence"])
                    if actual!=p["id"]:raise ValueError("self hypothesis ID divergence")
                elif kind=="self_review":
                    engine.review_self_hypothesis(p["id"],p["reviewer"],p["disposition"])
                elif kind=="oracle_review":
                    engine.review_oracle(p["id"],p["reviewer"],p["disposition"],p["justification"])
                elif kind=="pulse_input":
                    if p["config_snapshot"]!=asdict(config):
                        raise ValueError("pulse configuration changed")
                    actual=engine.pulse(seed=p["seed"],mode=p["mode"])
                    if actual["allowed_actions"]!=p["allowed"]:
                        raise ValueError("endogenous action mask divergence")
                elif kind=="observation":
                    needed=("affect_delta","relationship_delta","cue","seed","allowed","config_snapshot")
                    if any(k not in p for k in needed):
                        raise ValueError("source observation predates replay-complete protocol")
                    o=Observation(p["origin_id"],p["subject_id"],p["text"],p["source"],
                        EvidenceClass(p["evidence_class"]),p["actor_id"],
                        p["affect_delta"],p["relationship_delta"],p["cue"])
                    result=engine.step(o,p["allowed"],p["seed"])
                    if result["observation_id"]!=p["record_id"]:
                        raise ValueError("observation sequence divergence")
                elif kind=="outcome":
                    auth=authorities.get(p["decision_id"])
                    if auth is None:
                        raise ValueError("outcome without attributed authority")
                    engine.record_outcome(p["decision_id"],p["reward"],
                        auth["authority"],auth.get("source_origin"))
                elif kind in ("policy_decision","outcome_authority","developmental_consolidation","neural_reinforcement"):
                    pass
                else:
                    raise ValueError("unknown event kind in replay: "+kind)
            target=[dict(r) for r in engine.store.db.execute("SELECT * FROM events ORDER BY id")]
            decisions=[dict(r) for r in engine.store.db.execute("SELECT * FROM decisions ORDER BY id")]
            match=(len(events)==len(target) and
                   all((a["kind"],a["tick"],a["payload"],a["hash"])==
                       (b["kind"],b["tick"],b["payload"],b["hash"])
                       for a,b in zip(events,target)) and
                   len(original)==len(decisions) and
                   all((a["action"],a["audit"],a["hash"])==
                       (b["action"],b["audit"],b["hash"])
                       for a,b in zip(original,decisions)))
            if not match: raise ValueError("replayed history diverged from source")
            # Derived mutable state is never assumed trustworthy because an
            # attacker might change a projection without modifying event rows.
            tables=("meta","affect","field","intentions","relations","symbols",
                    "oracle","social_claims","social_reviews","oracle_reviews",
                    "self_hypotheses","self_reviews","developmental_state",
                    "field_snapshots","recurrent_state")
            for table in tables:
                left=[tuple(r) for r in source.execute(
                    "SELECT * FROM "+table+" ORDER BY rowid")]
                right=[tuple(r) for r in engine.store.db.execute(
                    "SELECT * FROM "+table+" ORDER BY rowid")]
                if left!=right:
                    raise ValueError("replay projection divergence in "+table)
            if not engine.store.verify():raise ValueError("replay audit verification failed")
            return {"verified":True,"event_count":len(events),
                    "decision_count":len(original),"configuration":asdict(config),
                    "state":engine.status()}
    finally:
        source.close()
