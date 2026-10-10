"""Independent replay, backup and strict configuration recovery."""
import os,sqlite3,tempfile,unittest
from noetic_engine import NoeticEngine,Observation,Configuration
from noetic_engine.models import EvidenceClass
from noetic_engine.replay import replay_database
from noetic_engine.backup import backup,restore

OWNER="pretorius_sandbox"
def observed(origin,actor="sarah",text="Sarah describes the laboratory dilemma",**kw):
    return Observation(origin,OWNER,text,"fixture",EvidenceClass.LIVED_OBSERVED,actor,**kw)

class Reproducibility(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.cfg=Configuration(egregore=True,self_model=True,developmental=True,
                               policy_version="noetic-v0.2")
        self.source=os.path.join(self.tmp.name,"source.sqlite")
        self.brain=NoeticEngine(self.source,self.cfg)
    def tearDown(self):self.brain.close();self.tmp.cleanup()

    def run_history(self):
        self.brain.add_intention("protect","Protect Sarah","care",0.8)
        first=self.brain.step(observed("a",relationship_delta=0.5,
                                         affect_delta={"affiliation":0.8}),seed=6)
        social=self.brain.add_social_claim("a","sarah",OWNER,"trusts",1,0.9,"direct_quote")
        self.brain.review_social_claim(social,"reviewer","admitted_for_policy")
        self_h=self.brain.propose_self_hypothesis("a","values","care",0.7,0.8)
        self.brain.review_self_hypothesis(self_h,"reviewer","corroborated_for_policy")
        self.brain.associate_symbol("amber","inquiry","a",0.2)
        self.brain.step(observed("b",cue="amber"),seed=6)
        third=self.brain.step(observed("c"),seed=6)
        if third["oracle"]:
            self.brain.review_oracle(third["oracle"]["id"],"reviewer",
                                      "retained_as_question","unknown but interesting")
        self.brain.record_outcome(first["decision_id"],0.6)
        self.brain.resolve_intention("protect")
        return self.brain.status()

    def test_strict_replay_complex_history(self):
        before=self.run_history()
        report=replay_database(self.source,os.path.join(self.tmp.name,"replayed.sqlite"))
        self.assertTrue(report["verified"])
        self.assertEqual(report["state"]["field"],before["field"])
        self.assertEqual(report["state"]["social_claims"],before["social_claims"])
        self.assertEqual(report["state"]["oracle_reviews"],before["oracle_reviews"])
        self.assertEqual(report["state"]["self_hypotheses"],before["self_hypotheses"])
        self.assertGreater(report["event_count"],8)

    def test_backup_restore_roundtrip(self):
        before=self.run_history()
        snapshot=backup(self.brain,os.path.join(self.tmp.name,"snapshot.sqlite"))
        restored=restore(snapshot["path"],os.path.join(self.tmp.name,"restored.sqlite"),
                         snapshot["sha256"],self.cfg)
        self.assertTrue(restored["verified"])
        self.assertEqual(restored["tick"],before["tick"])
        with NoeticEngine(restored["path"],self.cfg) as recovered:
            self.assertEqual(recovered.status()["field"],before["field"])

    def test_config_mismatch_is_rejected(self):
        self.run_history()
        with self.assertRaises(ValueError):
            NoeticEngine(self.source,Configuration(policy_version="noetic-v0.2"))

    def test_untrusted_outcome_authority_rejected(self):
        r=self.brain.step(observed("a"))
        with self.assertRaises(ValueError):
            self.brain.record_outcome(r["decision_id"],1,authority="adjudicated_outcome",
                                      source_origin="absent")
        self.assertTrue(self.brain.status()["verified_audit_hashes"])
        self.brain.step(observed("b"))
        self.brain.record_outcome(r["decision_id"],0.5,authority="adjudicated_outcome",
                                  source_origin="b")

    def test_source_tamper_detected_at_replay(self):
        self.brain.step(observed("a"))
        self.brain.close()
        # Integrity verification checks payload digests without trusting origin.
        with sqlite3.connect(self.source) as db:
            db.execute("DROP TRIGGER protect_event_update")
            db.execute("UPDATE events SET payload='{}' WHERE id=1")
        self.brain=NoeticEngine(self.source,self.cfg)
        with self.assertRaises(ValueError):
            replay_database(self.source,os.path.join(self.tmp.name,"invalid.sqlite"))

if __name__=="__main__":unittest.main()
