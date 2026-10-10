"""Stable renderer-neutral brain port. All mutations are transactional."""
from .models import Configuration
from .store import Store
from .step import perform
from .operations import intention,finish_intention,bind_symbol,outcome
from .memory import retrieve

class NoeticEngine:
    def __init__(self,path=":memory:",config=None):
        self.config=config or Configuration()
        self.config.validate()
        self.store=Store(path,self.config.subject_id)
        policy=self.store.meta("policy")
        if policy not in (None,self.config.policy_version):
            raise ValueError("policy version mismatch")
        if policy is None:
            with self.store.tx():self.store.put("policy",self.config.policy_version)

    def step(self,observation,allowed=None,seed=0):
        return perform(self,observation,allowed,seed)

    def add_intention(self,ident,label,tendency,strength=1.):
        with self.store.tx():
            intention(self.store,ident,label,tendency,strength,int(self.store.meta("tick")))

    def resolve_intention(self,ident,status="fulfilled"):
        with self.store.tx():
            finish_intention(self.store,ident,status,int(self.store.meta("tick")))

    def associate_symbol(self,symbol,tendency,origin_id,strength=0.2):
        with self.store.tx():
            bind_symbol(self.store,symbol,tendency,strength,origin_id,int(self.store.meta("tick")))

    def record_outcome(self,decision_id,reward):
        with self.store.tx():
            outcome(self.store,decision_id,reward,int(self.store.meta("tick")))

    def recall(self,query,limit=4):
        return retrieve(self.store.db,query,limit)

    def status(self):
        db=self.store
        return {
          "subject_id":db.meta("subject"),"tick":int(db.meta("tick")),
          "affect":db.mapping("affect","name","value"),
          "field":{r["name"]:{"activation":r["value"],"template":r["target"]}
                   for r in db.db.execute("SELECT * FROM field")},
          "intentions":[dict(r) for r in db.db.execute("SELECT * FROM intentions ORDER BY id")],
          "relationships":[dict(r) for r in db.db.execute("SELECT * FROM relations ORDER BY actor")],
          "memories":db.db.execute("SELECT COUNT(*) FROM observations").fetchone()[0],
          "oracle_hypotheses":db.db.execute("SELECT COUNT(*) FROM oracle").fetchone()[0],
          "verified_audit_hashes":db.verify()
        }

    def close(self):self.store.close()

    def __enter__(self):return self
    def __exit__(self,*args):self.close()
