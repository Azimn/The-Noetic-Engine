"""Two-timescale developmental field and event-gated plasticity.

The inspectable v0.1 controller remains the control. The opt-in developmental
profile changes reachable state trajectories, not the renderer's persona text.
"""
from .models import ACTION_WEIGHTS,clip,bounded
from .store import digest,serial

def advance(db,state,tick):
    """Fast activation plus slow set-point feedback; no reward learned here."""
    trace={}
    for k,v in state["field"].items():
        r=db.execute("SELECT * FROM developmental_state WHERE tendency=?",(k,)).fetchone()
        target,eligibility,meta=r["target"],r["eligibility"],r["metaplasticity"]
        correction=clip(0.10*(target-v),-0.08,0.08)
        updated=round(clip(v+correction),9)
        e=round(clip(0.85*eligibility+0.15*(updated-target)),9)
        m=round(clip(0.97*meta+0.03*abs(updated-target),0,1),9)
        db.execute("""UPDATE developmental_state SET eligibility=?,metaplasticity=?,
            update_tick=? WHERE tendency=?""",(e,m,tick,k))
        db.execute("UPDATE field SET value=? WHERE name=?",(updated,k))
        state["field"][k]=updated
        trace[k]={"setpoint":target,"homeostatic":round(correction,9),
                  "eligibility":e,"metaplasticity":m}
    snap={"field":state["field"],"development":trace}
    db.execute("""INSERT INTO field_snapshots(tick,values_json,template_json,digest)
      VALUES(?,?,?,?)""",(tick,serial(state["field"]),serial(trace),digest(snap)))
    state["development"]=trace
    return state

def consolidate(db,action,reward,decision_id,source_authority="operator_scored"):
    """Revises templates only on an explicitly recorded outcome.

    Operator-scored rewards remain separate from independently adjudicated
    consequences. Neither should imply consciousness or human-like identity.
    """
    reward=bounded(reward)
    if source_authority not in ("operator_scored","adjudicated_outcome"):
        raise ValueError("unsupported outcome authority")
    evidence={}
    for tendency,w in ACTION_WEIGHTS[action].items():
        r=db.execute("SELECT target,eligibility,metaplasticity FROM developmental_state WHERE tendency=?",
                     (tendency,)).fetchone()
        rate=0.05/(1+2*r["metaplasticity"])
        shift=rate*reward*w*r["eligibility"]
        new=round(clip(r["target"]+shift),9)
        db.execute("UPDATE developmental_state SET target=? WHERE tendency=?",(new,tendency))
        evidence[tendency]={"old":r["target"],"new":new,"shift":round(shift,9)}
    return {"decision_id":decision_id,"authority":source_authority,"changes":evidence}

def lesion_signature(db):
    """Snapshot sufficient for lesion and graft comparison, not neural weights."""
    return {r["tendency"]:{"target":r["target"],"eligibility":r["eligibility"],
                           "metaplasticity":r["metaplasticity"]}
            for r in db.execute("SELECT * FROM developmental_state ORDER BY tendency")}
