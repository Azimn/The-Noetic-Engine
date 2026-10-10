"""Bounded, inspectable coupling between experience, social state and policy."""
from .models import TENDENCIES, ACTION_WEIGHTS, clip

def propagate(db, cfg, actor, cue):
    affect={r["name"]:r["value"] for r in db.execute("SELECT * FROM affect")}
    prior={r["name"]:(r["value"],r["target"]) for r in db.execute("SELECT * FROM field")}
    family={k:{"affect":0.0,"intention":0.0,"social":0.0,"cue":0.0,"regulator":0.0} for k in TENDENCIES}
    family["inquiry"]["affect"]=0.45*affect["curiosity"]-0.18*affect["fatigue"]-0.12*affect["threat"]
    family["care"]["affect"]=0.48*affect["affiliation"]-0.20*affect["threat"]
    family["caution"]["affect"]=0.55*affect["threat"]+0.10*affect["fatigue"]
    if cfg.intentions:
        for i in db.execute("SELECT * FROM intentions WHERE status='active'"):
            family[i["tendency"]]["intention"]+=0.35*i["strength"]*i["tension"]
    if cfg.relationships:
        r=db.execute("SELECT * FROM relations WHERE actor=?",(actor,)).fetchone()
        if r:
            family["care"]["social"]+=0.35*r["trust"]*r["confidence"]
            family["caution"]["social"]-=0.12*r["trust"]*r["confidence"]
    if cfg.cues and cue:
        r=db.execute("SELECT * FROM symbols WHERE symbol=?",(cue,)).fetchone()
        if r: family[r["tendency"]]["cue"]+=r["strength"]
    new={}
    for k in TENDENCIES:
        old,target=prior[k]
        if cfg.regulator:
            family[k]["regulator"]=clip(cfg.regulator_gain*(target-old),-0.12,0.12)
        for name in ("affect","intention","social","cue"):
            family[k][name]=clip(family[k][name],-cfg.cap_family,cfg.cap_family)
        total=clip(sum(family[k].values()),-cfg.cap_total,cfg.cap_total)
        new[k]=round(clip((1-cfg.decay)*old+total),9)
        db.execute("UPDATE field SET value=? WHERE name=?",(new[k],k))
    return {"field":new,"causes":family,"affect":affect}

def arbitrate(state, allowed):
    scores={}
    for a in allowed:
        components={k:round(w*state["field"][k],9) for k,w in ACTION_WEIGHTS[a].items()}
        scores[a]={"base":0.0,"field":components,"total":round(sum(components.values()),9)}
    winning=sorted(scores,key=lambda a:(-scores[a]["total"],a))[0]
    return winning,scores

def learn_from_outcome(db,action,reward):
    """Developmental target updated only after explicit consequence admission."""
    for k,w in ACTION_WEIGHTS[action].items():
        r=db.execute("SELECT value,target FROM field WHERE name=?",(k,)).fetchone()
        proposed=clip(r["target"]+0.04*reward*w*r["value"])
        db.execute("UPDATE field SET target=? WHERE name=?",(round(proposed,9),k))
