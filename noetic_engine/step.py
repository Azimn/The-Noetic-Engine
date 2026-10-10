"""Complete observation-to-decision transaction with inspectable contributions."""
from .models import ACTIONS, clip
from .store import serial,digest
from .memory import retrieve
from .oracle import propose
from .dynamics import propagate,arbitrate

def perform(engine,observation,allowed=None,seed=0):
    cfg=engine.config; db=engine.store
    observation.validate(cfg.subject_id)
    if not isinstance(seed,int) or isinstance(seed,bool) or seed<0 or seed>2147483647:
        raise ValueError("seed must be a nonnegative bounded integer")
    actions=tuple(allowed) if allowed is not None else ACTIONS
    if not actions or len(actions)!=len(set(actions)) or any(a not in ACTIONS for a in actions):
        raise ValueError("invalid available action set")
    with db.tx():
        tick=int(db.meta("tick"))+1
        core={"origin_id":observation.origin_id,"subject_id":observation.subject_id,
              "actor_id":observation.actor_id,"evidence_class":observation.evidence_class.value,
              "source":observation.source,"text":observation.text}
        cur=db.db.execute("""INSERT INTO observations
              (tick,origin,subject,actor,source,class,text,hash)
              VALUES(?,?,?,?,?,?,?,?)""",
              (tick,observation.origin_id,observation.subject_id,observation.actor_id,
               observation.source,observation.evidence_class.value,observation.text,digest(core)))
        record_id=cur.lastrowid
        db.event(tick,"observation",{"record_id":record_id,**core})
        trusted=observation.evidence_class.value=="lived_observed"
        if trusted:
            for k,delta in observation.affect_delta.items():
                old=db.db.execute("SELECT value FROM affect WHERE name=?",(k,)).fetchone()[0]
                db.db.execute("UPDATE affect SET value=? WHERE name=?",
                              (round(clip(old+delta,0,1),9),k))
            if observation.relationship_delta:
                existing=db.db.execute("SELECT trust,confidence FROM relations WHERE actor=?",
                                       (observation.actor_id,)).fetchone()
                old=existing["trust"] if existing else 0.
                conf=existing["confidence"] if existing else 0.
                trust=round(clip(old+observation.relationship_delta),9)
                conf=round(clip(conf+0.2,0,1),9)
                db.db.execute("""INSERT INTO relations VALUES(?,?,?,?,?)
                    ON CONFLICT(actor) DO UPDATE SET
                    trust=excluded.trust,confidence=excluded.confidence,
                    viewpoint=excluded.viewpoint,source_id=excluded.source_id""",
                    (observation.actor_id,trust,conf,"subject_estimate",record_id))
        for i in db.db.execute("SELECT id,tension FROM intentions WHERE status='active'"):
            db.db.execute("UPDATE intentions SET tension=? WHERE id=?",
                          (round(clip(i["tension"]+0.01,0,1),9),i["id"]))
        memories=[x for x in retrieve(db.db,observation.text) if x["id"]!=record_id]
        hypothesis=propose(db.db,tick,seed,memories) if cfg.oracle else None
        state=propagate(db.db,cfg,observation.actor_id,observation.cue)
        action,scores=arbitrate(state,actions)
        audit={"tick":tick,"action":action,"scores":scores,"state":state,
               "observation_id":record_id,"origin_id":observation.origin_id,
               "memory_pointers":memories,"oracle":hypothesis,
               "allowed_actions":list(actions),"config":cfg.policy_version}
        cur=db.db.execute("INSERT INTO decisions(tick,action,audit,hash) VALUES(?,?,?,?)",
                          (tick,action,serial(audit),digest(audit)))
        audit["decision_id"]=cur.lastrowid
        db.event(tick,"policy_decision",{"decision_id":cur.lastrowid,
                                         "action":action,"audit_digest":digest(audit)})
        db.put("tick",tick)
    return audit
