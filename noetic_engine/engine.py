"""Stable renderer-neutral brain port. All mutations are transactional."""
from dataclasses import asdict
from .models import Configuration
from .store import digest
from .extensions import install
from .egregore import record_claim, review_claim
from .selfmodel import propose as propose_self, review as review_self
from .oracle_guard import review as review_oracle_record
from .development import consolidate, lesion_signature
from .neural_field import initialize as neural_initialize, load as neural_load, reinforce as neural_reinforce
from .store import Store
from .step import perform
from .endogenous import pulse as perform_pulse
from .operations import intention,finish_intention,bind_symbol,outcome
from .memory import retrieve

class NoeticEngine:
    def __init__(self,path=":memory:",config=None):
        self.config=config or Configuration()
        self.config.validate()
        self.store=Store(path,self.config.subject_id)
        install(self.store)
        existing=self.store.meta("config_digest")
        expected=digest(asdict(self.config))
        if existing is not None and existing!=expected:
            raise ValueError("configuration digest mismatch; clone state for experimental ablation")
        if existing is None:
            with self.store.tx():self.store.put("config_digest",expected)
        if self.config.neural_field:
            with self.store.tx():
                neural_initialize(self.store.db,self.config.subject_id,
                                  self.config.neural_units,self.config.neural_seed)
        policy=self.store.meta("policy")
        if policy not in (None,self.config.policy_version):
            raise ValueError("policy version mismatch")
        if policy is None:
            with self.store.tx():self.store.put("policy",self.config.policy_version)

    def step(self,observation,allowed=None,seed=0):
        return perform(self,observation,allowed,seed)

    def pulse(self,seed=0,mode="wake"):
        return perform_pulse(self,seed,mode)

    def add_intention(self,ident,label,tendency,strength=1.):
        with self.store.tx():
            intention(self.store,ident,label,tendency,strength,int(self.store.meta("tick")))

    def resolve_intention(self,ident,status="fulfilled"):
        with self.store.tx():
            finish_intention(self.store,ident,status,int(self.store.meta("tick")))

    def associate_symbol(self,symbol,tendency,origin_id,strength=0.2):
        with self.store.tx():
            bind_symbol(self.store,symbol,tendency,strength,origin_id,int(self.store.meta("tick")))

    def record_outcome(self,decision_id,reward,authority="operator_scored",source_origin=None):
        if authority not in ("operator_scored","adjudicated_outcome"):
            raise ValueError("unsupported outcome authority")
        if authority=="adjudicated_outcome":
            if not source_origin:
                raise ValueError("adjudicated outcomes need an independent lived source observation")
            r=self.store.db.execute(
                "SELECT subject,class FROM observations WHERE origin=?",
                (source_origin,)).fetchone()
            if not r or r["subject"]!=self.config.subject_id or r["class"]!="lived_observed":
                raise ValueError("outcome authority source fails provenance check")
        with self.store.tx():
            outcome(self.store,decision_id,reward,int(self.store.meta("tick")))
            if self.config.developmental:
                row=self.store.db.execute("SELECT action FROM decisions WHERE id=?",
                                          (decision_id,)).fetchone()
                changed=consolidate(self.store.db,row["action"],reward,decision_id,authority)
                self.store.event(int(self.store.meta("tick")),"developmental_consolidation",
                                 {**changed,"source_origin":source_origin})
            if self.config.neural_field:
                changed_neural=neural_reinforce(self.store.db,self.config.subject_id,reward)
                self.store.event(int(self.store.meta("tick")),"neural_reinforcement",
                                 {"decision_id":decision_id,**changed_neural})
            self.store.event(int(self.store.meta("tick")),"outcome_authority",
                             {"decision_id":decision_id,"authority":authority,
                              "source_origin":source_origin})

    def add_social_claim(self,origin,attributed_actor,believed_subject,predicate,
                         valence,confidence,epistemic):
        with self.store.tx():
            return record_claim(self.store,origin,attributed_actor,believed_subject,
                                predicate,valence,confidence,epistemic)

    def review_social_claim(self,claim_id,reviewer,disposition):
        with self.store.tx():
            review_claim(self.store,claim_id,reviewer,disposition)

    def propose_self_hypothesis(self,origin,predicate,tendency,valence,confidence):
        with self.store.tx():
            return propose_self(self.store,origin,predicate,tendency,valence,confidence)

    def review_self_hypothesis(self,hypothesis_id,reviewer,disposition):
        with self.store.tx():
            review_self(self.store,hypothesis_id,reviewer,disposition)

    def review_oracle(self,hypothesis_id,reviewer,disposition,justification):
        with self.store.tx():
            return review_oracle_record(self.store,hypothesis_id,reviewer,
                                        disposition,justification)

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
          "verified_audit_hashes":db.verify(),
          "developmental_state":lesion_signature(db.db),
          "social_claims":[dict(r) for r in db.db.execute("SELECT * FROM social_claims ORDER BY id")],
          "oracle_reviews":[dict(r) for r in db.db.execute("SELECT * FROM oracle_reviews ORDER BY id")],
          "configuration_digest":db.meta("config_digest"),
          "neural_field":({"units":self.config.neural_units,
                           "updates":neural_load(db.db,self.config.subject_id)["updates"],
                           "outcomes":neural_load(db.db,self.config.subject_id)["outcomes"]}
                           if self.config.neural_field else None),
          "self_hypotheses":[dict(r) for r in db.db.execute("SELECT * FROM self_hypotheses ORDER BY id")]
        }

    def close(self):self.store.close()

    def __enter__(self):return self
    def __exit__(self,*args):self.close()
