"""Hypotheses belong to a noncanonical namespace, never the memory ledger."""
import random
from .store import serial
def propose(db,tick,seed,memories):
    if len(memories)<2:return None
    rng=random.Random(f"{seed}:{tick}")
    a,b=rng.sample(memories,2)
    text=("Hypothesis only: Could the situations represented by observation "+
          str(a["id"])+" and observation "+str(b["id"])+" share a relevant pattern?")
    refs=[a["id"],b["id"]]
    cur=db.execute("INSERT INTO oracle(tick,text,source_ids,seed,status) VALUES(?,?,?,?,?)",
                   (tick,text,serial(refs),seed,"hypothesis_only"))
    return {"id":cur.lastrowid,"text":text,"source_ids":refs,"status":"hypothesis_only"}
