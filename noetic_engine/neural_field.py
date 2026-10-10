"""Synthetic, sparse, persistent recurrent dynamics: explicitly NOT FlyWire weights.

This is a causally integrated optional donor. It starts with deterministic random
sparse connections. Hebbian eligibility and Oja-like normalization update them
only after an explicit outcome. No claim of neuronal realism or learned identity.
"""
import json,math,random
from .models import TENDENCIES,clip,bounded
from .store import serial,digest

def initialize(db,subject,units=96,seed=1701):
    existing=db.execute("SELECT payload,digest FROM recurrent_state WHERE subject_id=?",
                        (subject,)).fetchone()
    if existing:
        if digest(json.loads(existing["payload"]))!=existing["digest"]:
            raise ValueError("recurrent substrate integrity failure")
        state=json.loads(existing["payload"])
        if state["units"]!=units or state["seed"]!=seed:
            raise ValueError("neural profile mismatch")
        return
    rng=random.Random(seed)
    weights=[]
    for node in range(units):
        neighbors=sorted(set(((node-1)%units,(node+3)%units,(node*7+11)%units)))
        weights.append([[k,round(rng.uniform(-0.13,0.13),9),0.0] for k in neighbors])
    state={"schema":1,"units":units,"seed":seed,
           "activations":[0.0]*units,"edges":weights,"updates":0,"outcomes":0}
    db.execute("INSERT INTO recurrent_state VALUES(?,?,?)",
               (subject,serial(state),digest(state)))

def load(db,subject):
    row=db.execute("SELECT payload,digest FROM recurrent_state WHERE subject_id=?",
                   (subject,)).fetchone()
    if not row:raise ValueError("neural field not initialized")
    state=json.loads(row["payload"])
    if digest(state)!=row["digest"]:raise ValueError("neural state tampered")
    return state

def save(db,subject,state):
    db.execute("UPDATE recurrent_state SET payload=?,digest=? WHERE subject_id=?",
               (serial(state),digest(state),subject))

def propagate(db,subject,field,tick):
    state=load(db,subject)
    prior=state["activations"]
    units=state["units"]
    for _ in range(2):
        next_act=[]
        for i in range(units):
            tendency=TENDENCIES[i%3]
            drive=0.55*field[tendency]+0.26*prior[i]
            recurrent=sum(edge[1]*prior[edge[0]] for edge in state["edges"][i])
            next_act.append(round(math.tanh(drive+recurrent),9))
        prior=next_act
    for i in range(units):
        for edge in state["edges"][i]:
            edge[2]=round(clip(0.88*edge[2]+0.12*state["activations"][edge[0]]*prior[i]),9)
    state["activations"]=prior
    state["updates"]+=1
    outputs={k:round(sum(prior[i] for i in range(units) if i%3==n)/
                     len(range(n,units,3)),9) for n,k in enumerate(TENDENCIES)}
    adjusted={k:round(clip(field[k]+0.12*outputs[k]),9) for k in TENDENCIES}
    for k,v in adjusted.items():
        db.execute("UPDATE field SET value=? WHERE name=?",(v,k))
    save(db,subject,state)
    return adjusted,{"outputs":outputs,"updates":state["updates"],
                     "checksum":digest(state),"units":units,"tick":tick}

def reinforce(db,subject,reward):
    reward=bounded(reward)
    state=load(db,subject)
    changes=0
    for i,edges in enumerate(state["edges"]):
        post=state["activations"][i]
        for edge in edges:
            old=edge[1]
            edge[1]=round(clip(old+0.025*reward*
                (edge[2]-post*post*old),-0.5,0.5),9)
            if old!=edge[1]:changes+=1
    state["outcomes"]+=1
    save(db,subject,state)
    return {"changed_edges":changes,"outcomes":state["outcomes"],
            "checksum":digest(state),"learning_type":"eligibility_oja_synthetic"}
