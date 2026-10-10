"""Controlled endogenous cognition and sleep-like maintenance.

These are caller-scheduled CPU cycles, not autonomous background execution,
not dreams as memories, and not a second language model.
"""
from dataclasses import asdict
from .models import ACTIONS,clip
from .store import serial,digest
from .memory import retrieve
from .oracle import propose
from .dynamics import propagate,arbitrate
from .development import advance
from .neural_field import propagate as neural_propagate

def pulse(engine,seed=0,mode="wake"):
    if mode not in ("wake","sleep"):raise ValueError("unknown endogenous phase")
    if type(seed) is not int or not 0<=seed<=2147483647:
        raise ValueError("invalid seed")
    db=engine.store;cfg=engine.config
    with db.tx():
        tick=int(db.meta("tick"))+1
        allowed=("defer",) if mode=="sleep" else ACTIONS
        db.event(tick,"pulse_input",{"mode":mode,"seed":seed,"allowed":list(allowed),
             "config_snapshot":asdict(cfg)})
        active=[r["label"] for r in db.db.execute(
            "SELECT label FROM intentions WHERE status='active' ORDER BY id")]
        recent=db.db.execute("SELECT text FROM observations ORDER BY id DESC LIMIT 1").fetchone()
        query=" ".join(active[:2])+(" "+recent["text"] if recent else "")
        memories=retrieve(db.db,query)
        hypothesis=propose(db.db,tick,seed,memories) if cfg.oracle else None
        if mode=="sleep":
            # Only regulation and affect decay. Sleep cannot approve stories.
            for r in db.db.execute("SELECT name,value FROM affect"):
                db.db.execute("UPDATE affect SET value=? WHERE name=?",
                    (round(clip(r["value"]*0.93,0,1),9),r["name"]))
        state=propagate(db.db,cfg,"environment","")
        if cfg.developmental:
            state=advance(db.db,state,tick)
        if cfg.neural_field:
            field,neural=neural_propagate(db.db,cfg.subject_id,state["field"],tick)
            state["field"]=field;state["neural"]=neural
        action,scores=arbitrate(state,allowed)
        audit={"tick":tick,"action":action,"scores":scores,"state":state,
               "observation_id":None,"origin_id":None,
               "memory_pointers":memories,"oracle":hypothesis,
               "allowed_actions":list(allowed),"config":cfg.policy_version,
               "phase":mode,"endogenous":True}
        stored_hash=digest(audit)
        cur=db.db.execute("INSERT INTO decisions(tick,action,audit,hash) VALUES(?,?,?,?)",
                          (tick,action,serial(audit),stored_hash))
        audit["decision_id"]=cur.lastrowid
        db.event(tick,"policy_decision",{"decision_id":cur.lastrowid,"action":action,
                                         "audit_digest":stored_hash})
        db.put("tick",tick)
        return audit
