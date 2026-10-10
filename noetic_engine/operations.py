"""Explicit durable changes; observations never silently rewrite the self."""
from .models import TENDENCIES,bounded,clip,InvalidEvidence
from .dynamics import learn_from_outcome

def intention(db,ident,label,tendency,strength,tick):
    if not ident or not label or tendency not in TENDENCIES:raise ValueError("invalid intention")
    strength=bounded(strength,0,1)
    if db.db.execute("SELECT 1 FROM intentions WHERE id=?",(ident,)).fetchone():
        raise ValueError("intention ID already used")
    db.db.execute("INSERT INTO intentions VALUES(?,?,?,?,?,'active')",
                  (ident,label,tendency,strength,1.0))
    db.event(tick,"intention_created",{"id":ident,"label":label,"tendency":tendency,"strength":strength})

def finish_intention(db,ident,status,tick):
    if status not in ("fulfilled","abandoned"):raise ValueError("invalid resolution")
    r=db.db.execute("SELECT status FROM intentions WHERE id=?",(ident,)).fetchone()
    if not r or r["status"]!="active":raise ValueError("intention not active")
    db.db.execute("UPDATE intentions SET status=?,tension=0 WHERE id=?",(status,ident))
    db.event(tick,"intention_resolved",{"id":ident,"status":status})

def bind_symbol(db,symbol,tendency,strength,origin,tick):
    if not symbol or len(symbol)>100 or tendency not in TENDENCIES:
        raise ValueError("invalid symbol")
    strength=bounded(strength,-0.45,0.45)
    r=db.db.execute("SELECT id,class,subject FROM observations WHERE origin=?",(origin,)).fetchone()
    if not r or r["class"]!="lived_observed" or r["subject"]!=db.meta("subject"):
        raise InvalidEvidence("symbol requires own lived source event")
    db.db.execute("INSERT INTO symbols VALUES(?,?,?,?)",(symbol,tendency,strength,r["id"]))
    db.event(tick,"symbol_bound",{"symbol":symbol,"tendency":tendency,"strength":strength,"origin":origin})

def outcome(db,decision_id,reward,tick):
    reward=bounded(reward)
    r=db.db.execute("SELECT action FROM decisions WHERE id=?",(decision_id,)).fetchone()
    if not r:raise ValueError("unknown decision")
    for e in db.db.execute("SELECT payload FROM events WHERE kind='outcome'"):
        import json
        if json.loads(e["payload"])["decision_id"]==decision_id:
            raise ValueError("duplicate outcome")
    learn_from_outcome(db,r["action"],reward)
    db.event(tick,"outcome",{"decision_id":decision_id,"reward":reward})
