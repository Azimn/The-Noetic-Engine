"""Closed fictional-world laboratory, NEVER a claim about physical reality.

World resolution is independent of agent autobiographical evidence. Conscious
observer effects are fictional knobs and default to ZERO coupling. First
resolution commits shared world state, so later observers cannot rewrite it.
"""
import hashlib,json,math,random,sqlite3
from .models import bounded
from .store import serial,digest

class FictionalWorld:
    def __init__(self,path=":memory:",coupling=0.0):
        self.coupling=bounded(coupling,0,1)
        self.db=sqlite3.connect(path,isolation_level=None)
        self.db.row_factory=sqlite3.Row
        self.db.execute("""CREATE TABLE IF NOT EXISTS resolutions(
           event_id TEXT PRIMARY KEY, selected TEXT NOT NULL,
           observer_id TEXT NOT NULL, trace TEXT NOT NULL, sha256 TEXT NOT NULL)""")

    def resolve(self,event_id,observer_id,possibilities,intentions=None,seed=0):
        if not isinstance(event_id,str) or not event_id.strip() or not isinstance(observer_id,str) or not observer_id.strip():
            raise ValueError("event and observer IDs required")
        old=self.db.execute("SELECT selected,trace FROM resolutions WHERE event_id=?",
                            (event_id,)).fetchone()
        if old:
            return {"selected":old["selected"],"trace":json.loads(old["trace"]),"committed":True}
        if not possibilities or len(possibilities)!=len(set(possibilities)):
            raise ValueError("nonempty unique outcomes required")
        for k,p in possibilities.items():
            if not isinstance(k,str) or not k.strip() or not isinstance(p,(float,int)) or isinstance(p,bool):
                raise ValueError("invalid outcome")
            bounded(p,0,1)
        if abs(sum(possibilities.values())-1.0)>1e-8:
            raise ValueError("base probabilities must sum to one")
        bias=intentions or {}
        if any(k not in possibilities for k in bias):
            raise ValueError("intention must refer only to permitted outcomes")
        for v in bias.values():bounded(v)
        if not isinstance(seed,int) or isinstance(seed,bool):
            raise ValueError("integer seed required")
        logits={k:math.log(max(p,1e-15))+self.coupling*bias.get(k,0.0)
                for k,p in possibilities.items()}
        largest=max(logits.values())
        unnorm={k:math.exp(v-largest) if possibilities[k]>0 else 0.0
                for k,v in logits.items()}
        total=sum(unnorm.values())
        dist={k:v/total for k,v in unnorm.items()}
        rng=random.Random(serial({"event":event_id,"seed":seed}))
        sample=rng.random()
        cumulative=0.0; selected=next(iter(dist))
        for k,v in dist.items():
            cumulative+=v
            if sample<cumulative:
                selected=k;break
        trace={"event_id":event_id,"observer_id":observer_id,"seed":seed,
               "base_probabilities":possibilities,"fictional_coupling":self.coupling,
               "intention_bias":bias,"resolved_distribution":dist,
               "chosen":selected,"interpretation":"FICTIONAL_SIMULATOR_ONLY"}
        self.db.execute("INSERT INTO resolutions VALUES(?,?,?,?,?)",
                        (event_id,selected,observer_id,serial(trace),digest(trace)))
        return {"selected":selected,"trace":trace,"committed":False}

    def verify(self):
        return all(digest(json.loads(r["trace"]))==r["sha256"] for r in
                   self.db.execute("SELECT trace,sha256 FROM resolutions"))

    def close(self):self.db.close()
