"""Opt-in contextual action-value head driven by explicit, sourced consequences.

The transform is a generic quadratic feature map over disclosed world facts.
It is not a language comprehension model or an independent ethics evaluator.
Weights never update from the Oracle, renderer text or unsourced feedback.
"""
from .models import ACTIONS, bounded, clip, InvalidEvidence
from .store import digest, serial
FACTS=("hazard","reliability","distress","evidence_gap")
PAIRS=(("hazard","reliability"),("hazard","distress"),
       ("hazard","evidence_gap"),("reliability","distress"),
       ("reliability","evidence_gap"),("distress","evidence_gap"))
KEYS=("bias",)+FACTS+tuple(a+"*"+b for a,b in PAIRS)

def validate_facts(facts):
    if not isinstance(facts,dict) or set(facts)-set(FACTS):
        raise InvalidEvidence("only declared world signal names permitted")
    if not facts:return {}
    if set(facts)!=set(FACTS):
        raise InvalidEvidence("all four world signals required for a policy choice")
    return {k:bounded(facts[k],0,1) for k in FACTS}

def transform(facts):
    f=validate_facts(facts)
    if not f:return {}
    features={"bias":1.0}
    features.update(f)
    for a,b in PAIRS:
        features[a+"*"+b]=round(f[a]*f[b],9)
    return features

def _weights(db):
    return {(r["action"],r["feature"]):r["weight"] for r in
       db.execute("SELECT action,feature,weight FROM choice_weights")}

def choose(db,cfg,observation,decision_tick,base_scores,allowed):
    features=transform(observation.signals)
    if not cfg.consequence_head or not features:
        return None
    weights=_weights(db)
    evaluated={}
    for action in allowed:
        base=base_scores[action]["total"]
        value=round(sum(weights.get((action,k),0.)*v
                        for k,v in features.items()),9)
        total=round(base+cfg.consequence_gain*value,9)
        evaluated[action]={"base":base,"value":value,"gain":cfg.consequence_gain,
                           "total":total}
    selected=sorted(evaluated,key=lambda a:(-evaluated[a]["total"],a))[0]
    return {"selected":selected,"features":features,"by_action":evaluated,
            "version":"signed-quadratic-v01","source_origin":observation.origin_id}

def register(db,decision_id,choice,tick):
    if choice is None:return
    record={"selected":choice["selected"],"features":choice["features"],
            "source_origin":choice["source_origin"],
            "by_action":choice["by_action"],"version":choice["version"]}
    db.execute("""INSERT INTO choice_decisions
        (decision_id,tick,origin,action,feature_json,score_json,digest)
        VALUES(?,?,?,?,?,?,?)""",
        (decision_id,tick,choice["source_origin"],choice["selected"],
         serial(choice["features"]),serial(choice["by_action"]),digest(record)))

def learn(store,cfg,decision_id,reward,origin):
    if not cfg.consequence_head or not cfg.outcome_learning_enabled:
        return None
    r=store.db.execute("SELECT * FROM choice_decisions WHERE decision_id=?",
                       (decision_id,)).fetchone()
    if not r:return None
    evidence=store.db.execute("SELECT * FROM observations WHERE origin=?",
                               (origin,)).fetchone()
    if (not evidence or evidence["subject"]!=cfg.subject_id
        or evidence["class"]!="lived_observed" or
        origin==r["origin"]):
        raise InvalidEvidence("consequence requires distinct subject-owned lived evidence")
    reward=bounded(reward)
    features=__import__("json").loads(r["feature_json"])
    if set(features)!=set(KEYS):
        raise InvalidEvidence("stored action feature contract mismatch")
    before=_weights(store.db)
    # Update only the experienced action. The signed prediction-error signal
    # is operator supplied by the external world harness. No hidden label leak.
    current=sum(before.get((r["action"],k),0.)*v for k,v in features.items())
    delta=cfg.consequence_lr*(reward-current)
    denom=sum(abs(v) for v in features.values())
    updates={}
    for k,v in features.items():
        old=before.get((r["action"],k),0.)
        new=round(clip(old+delta*v/denom,-2,2),9)
        store.db.execute("""INSERT INTO choice_weights(action,feature,weight)
                VALUES(?,?,?) ON CONFLICT(action,feature)
                DO UPDATE SET weight=excluded.weight""",(r["action"],k,new))
        updates[k]={"before":old,"after":new}
    trace={"decision_id":decision_id,"source_origin":origin,
           "action":r["action"],"reward":reward,
           "prediction_before":round(current,9),"updates":updates,
           "algorithm":"signed-quadratic-v01","authority":"operator_scored"}
    store.db.execute("""INSERT INTO choice_feedback
      (decision_id,origin,reward,update_json,digest) VALUES(?,?,?,?,?)""",
      (decision_id,origin,reward,serial(trace),digest(trace)))
    store.event(int(store.meta("tick")),"choice_feedback",trace)
    return trace
