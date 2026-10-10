"""Adversarial source attribution and noncanonical imagination tests."""
import os,tempfile,unittest,sqlite3
from noetic_engine import NoeticEngine,Configuration,Observation,InvalidEvidence
from noetic_engine.models import EvidenceClass
from noetic_engine.renderer import brief_from_decision,DiagnosticRenderer,DecoratedRenderer
from noetic_engine.world import FictionalWorld

OWNER="pretorius_sandbox"
def lived(origin,text="Sarah describes a laboratory incident",actor="sarah",**kwargs):
    return Observation(origin,OWNER,text,"witnessed-fixture",
                       EvidenceClass.LIVED_OBSERVED,actor,**kwargs)

class ExtendedBoundaries(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.brain=NoeticEngine(os.path.join(self.tmp.name,"brain.db"),
                  Configuration(egregore=True,self_model=True,developmental=True,
                                policy_version="noetic-v0.2"))
    def tearDown(self):self.brain.close();self.tmp.cleanup()

    def test_social_attribution_needs_source_and_review(self):
        self.brain.step(lived("witness",text="Sarah said I fear the experiment in the laboratory"))
        ident=self.brain.add_social_claim("witness","sarah",OWNER,"fears",1.,0.9,"direct_quote","I fear the experiment")
        before=self.brain.step(lived("before"))
        self.assertEqual(before["state"]["causes"]["caution"]["attributed_belief"],0.)
        self.brain.review_social_claim(ident,"external-reviewer","admitted_for_policy")
        after=self.brain.step(lived("after"))
        self.assertGreater(after["state"]["causes"]["caution"]["attributed_belief"],0.)
        self.assertEqual(after["state"]["attributed_claim_ids"],[ident])
        self.assertEqual(self.brain.status()["social_claims"][0]["status"],"admitted_for_policy")

    def test_no_foreign_mind_or_hearsay_admission(self):
        self.brain.step(lived("a"))
        with self.assertRaises(InvalidEvidence):
            self.brain.add_social_claim("a","sarah",OWNER,"fears",1.,1.,"direct_quote","invented quotation")
        with self.assertRaises(InvalidEvidence):
            self.brain.add_social_claim("a","different-witness",OWNER,"fears",1.,1.,"direct_quote")
        rumor=Observation("rumor","outsider","Sarah supposedly fears Pretorius",
                          "unverified-note",EvidenceClass.THIRD_PARTY_CLAIM,"speaker")
        self.brain.step(rumor)
        ident=self.brain.add_social_claim("rumor","sarah",OWNER,"fears",1.,1.,"third_party_report")
        with self.assertRaises(InvalidEvidence):
            self.brain.review_social_claim(ident,"reviewer","admitted_for_policy")
        self.assertEqual(self.brain.status()["social_claims"][0]["status"],"unreviewed")

    def test_self_model_requires_lived_anchor(self):
        self.brain.step(lived("a",affect_delta={"affiliation":0.2}))
        h=self.brain.propose_self_hypothesis("a","values","care",0.8,0.8)
        before=self.brain.step(lived("b"))
        self.assertEqual(before["state"]["causes"]["care"]["self_model"],0)
        self.brain.review_self_hypothesis(h,"auditor","corroborated_for_policy")
        after=self.brain.step(lived("c"))
        self.assertGreater(after["state"]["causes"]["care"]["self_model"],0)
        with self.assertRaises(InvalidEvidence):
            self.brain.propose_self_hypothesis("absent","values","care",1,1)

    def test_oracle_cannot_enter_canonical_history(self):
        for i in range(3):
            result=self.brain.step(lived(str(i),"Sarah discusses the laboratory trial again"),seed=9)
        oracle=result["oracle"]
        self.assertIsNotNone(oracle)
        with self.assertRaises(ValueError):
            self.brain.review_oracle(oracle["id"],"auditor","canonical","plausible")
        disposition=self.brain.review_oracle(oracle["id"],"auditor",
                                             "retained_as_question","needs independent evidence")
        self.assertFalse(disposition["canonical"])
        self.assertEqual(self.brain.status()["memories"],3)
        self.assertTrue(all(r["evidence_class"]!="oracle_hypothesis"
                            for r in self.brain.recall("laboratory")))
        with self.assertRaises(InvalidEvidence):
            self.brain.step(Observation("x",OWNER,"An imagined truth","oracle",
                            EvidenceClass.ORACLE_HYPOTHESIS))

    def test_development_and_authority_are_separate(self):
        r=self.brain.step(lived("a",affect_delta={"curiosity":0.9}),
                          allowed=["investigate"])
        self.assertIn("development",r["state"])
        before=self.brain.status()["developmental_state"]["inquiry"]["target"]
        self.brain.record_outcome(r["decision_id"],1.0)
        after=self.brain.status()["developmental_state"]["inquiry"]["target"]
        self.assertNotEqual(before,after)
        with self.assertRaises(ValueError):
            self.brain.record_outcome(r["decision_id"],0.5)
        with self.assertRaises(ValueError):
            self.brain.record_outcome(999,0.5,authority="adjudicated_outcome")

    def test_renderer_changes_only_expression(self):
        r=self.brain.step(lived("one"),allowed=["defer"])
        b=brief_from_decision(self.brain,r["decision_id"])
        self.assertEqual(b.action,"defer")
        self.assertNotEqual(DiagnosticRenderer().render(b),DecoratedRenderer().render(b))
        self.assertEqual(b.action,self.brain.store.db.execute("SELECT action FROM decisions").fetchone()[0])

    def test_event_and_observation_append_only(self):
        self.brain.step(lived("one"))
        with self.assertRaises(sqlite3.IntegrityError):
            self.brain.store.db.execute("UPDATE events SET payload='{}' WHERE id=1")
        with self.assertRaises(sqlite3.IntegrityError):
            self.brain.store.db.execute("DELETE FROM observations WHERE id=1")
        self.assertTrue(self.brain.status()["verified_audit_hashes"])

class WorldSeparation(unittest.TestCase):
    def test_intention_independent_zero_coupling(self):
        with_cues=FictionalWorld(coupling=0)
        other=FictionalWorld(coupling=0)
        a=with_cues.resolve("e","observer1",{"success":0.5,"failure":0.5},
                            {"success":1,"failure":-1},seed=12)
        b=other.resolve("e","observer2",{"success":0.5,"failure":0.5},seed=12)
        self.assertEqual(a["selected"],b["selected"])
        self.assertEqual(a["trace"]["resolved_distribution"],b["trace"]["resolved_distribution"])

    def test_positive_coupling_and_shared_commit(self):
        w=FictionalWorld(coupling=1)
        a=w.resolve("f","observer1",{"success":0.5,"failure":0.5},
                    {"success":1,"failure":-1},seed=9)
        self.assertGreater(a["trace"]["resolved_distribution"]["success"],0.5)
        b=w.resolve("f","observer2",{"success":0.9,"failure":0.1},seed=0)
        self.assertEqual(a["selected"],b["selected"])
        self.assertTrue(b["committed"])
        self.assertTrue(w.verify())

if __name__=="__main__":unittest.main()
