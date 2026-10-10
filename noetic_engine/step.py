"""Complete observation-to-decision transaction with inspectable contributions."""
from dataclasses import asdict
from .models import ACTIONS, clip
from .development import advance
from .context_field import apply as context_apply
from .consequence_head import choose as choice_choose, register as choice_register
from .neural_field import propagate as neural_propagate
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
        db.event(tick,"observation",{"record_id":record_id,**core,
            "affect_delta":observation.affect_delta,"relationship_delta":observation.relationship_delta,
            "cue":observation.cue,"signals":observation.signals,"seed":seed,"allowed":list(actions),
            "config_snapshot":asdict(cfg)})
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
        if cfg.conditional_context:
            state=context_apply(db,cfg,state,tick)
        if cfg.developmental:
            state=advance(db.db,state,tick)
        if cfg.neural_field:
            adjusted,neurals=neural_propagate(db.db,cfg.subject_id,state["field"],tick)
            state["field"]=adjusted
            state["neural"]=neurals
        action,scores=arbitrate(state,actions)
        contextual=choice_choose(db.db,cfg,observation,tick,scores,actions)
        if contextual:
            action=contextual["selected"]
            state["base_policy_scores"]=scores
            state["choice_head"]={"feature_basis":contextual["features"],
                                  "by_action":contextual["by_action"],
                                  "version":contextual["version"]}
            # Top-level audit scores must describe the ACTUAL selected policy,
            # not merely the pre-learning field's counterfactual scores.
            scores={a:{"base":v["base"],"learned_value":v["value"],
                       "learned_gain":v["gain"],"total":v["total"]}
                    for a,v in contextual["by_action"].items()}
        audit={"tick":tick,"action":action,"scores":scores,"state":state,
               "observation_id":record_id,"origin_id":observation.origin_id,
               "memory_pointers":memories,"oracle":hypothesis,
               "allowed_actions":list(actions),"config":cfg.policy_version}
        stored_digest=digest(audit)
        cur=db.db.execute("INSERT INTO decisions(tick,action,audit,hash) VALUES(?,?,?,?)",
                          (tick,action,serial(audit),stored_digest))
        audit["decision_id"]=cur.lastrowid
        if contextual:
            choice_register(db.db,cur.lastrowid,contextual,tick)
        db.event(tick,"policy_decision",{"decision_id":cur.lastrowid,
                                         "action":action,"audit_digest":stored_digest})
        db.put("tick",tick)
    return audit
