import os,tempfile,sqlite3,unittest
from noetic_engine import NoeticEngine,Observation,Configuration,InvalidEvidence
from noetic_engine.models import EvidenceClass

def obs(i,text="A witness requires protection",actor="witness",**kw):
    return Observation(str(i),"pretorius_sandbox",text,"test-fixture",
                       EvidenceClass.LIVED_OBSERVED,actor,**kw)

class TestNoeticLifecycle(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=os.path.join(self.tmp.name,"brain.sqlite")
        self.brain=NoeticEngine(self.path)
    def tearDown(self):
        self.brain.close();self.tmp.cleanup()

    def test_full_cycle_and_restart(self):
        self.brain.add_intention("duty","Keep the witness safe","care")
        r=self.brain.step(obs("one",affect_delta={"affiliation":0.7},relationship_delta=0.5),seed=8)
        self.assertIn(r["action"],r["allowed_actions"])
        self.assertEqual(r["tick"],1)
        self.assertEqual(r["state"]["field"]["care"]>0,True)
        self.assertTrue(self.brain.status()["verified_audit_hashes"])
        self.brain.close()
        self.brain=NoeticEngine(self.path)
        self.assertEqual(self.brain.status()["tick"],1)
        self.assertEqual(self.brain.status()["memories"],1)
        self.assertEqual(self.brain.status()["intentions"][0]["status"],"active")
        self.assertTrue(self.brain.status()["verified_audit_hashes"])
        self.brain.resolve_intention("duty")
        self.assertEqual(self.brain.status()["intentions"][0]["status"],"fulfilled")

    def test_intentions_causally_shift_policy(self):
        self.brain.add_intention("goal","Attend to companion","care")
        with_intent=self.brain.step(obs("yes"),seed=1)
        cfg=Configuration(intentions=False)
        with NoeticEngine(":memory:",cfg) as control:
            no_intent=control.step(obs("yes"),seed=1)
        self.assertGreater(with_intent["state"]["field"]["care"],
                           no_intent["state"]["field"]["care"])

    def test_observer_subject_boundary(self):
        bad=Observation("foreign","different-person","Their diary","archive",
                        EvidenceClass.LIVED_OBSERVED)
        with self.assertRaises(InvalidEvidence):self.brain.step(bad)
        self.assertEqual(self.brain.status()["memories"],0)

    def test_hypothesis_is_not_memory(self):
        self.brain.step(obs("a","A witness enters the laboratory"))
        self.brain.step(obs("b","A witness leaves the laboratory"))
        r=self.brain.step(obs("c","The witness describes the laboratory again"),seed=5)
        self.assertIsNotNone(r["oracle"])
        self.assertEqual(r["oracle"]["status"],"hypothesis_only")
        self.assertEqual(self.brain.status()["memories"],3)
        self.assertEqual(self.brain.status()["oracle_hypotheses"],1)
        self.assertFalse(any("Hypothesis" in x["excerpt"] for x in self.brain.recall("witness")))

    def test_unallowed_action_never_selected(self):
        with self.assertRaises(ValueError):
            self.brain.step(obs("bad"),allowed=["rewrite_reality"])
        self.assertEqual(self.brain.status()["tick"],0)
        r=self.brain.step(obs("ok"),allowed=["defer"])
        self.assertEqual(r["action"],"defer")

    def test_duplicate_origin_rolls_back(self):
        self.brain.step(obs("unique"))
        with self.assertRaises(sqlite3.IntegrityError):self.brain.step(obs("unique"))
        self.assertEqual(self.brain.status()["tick"],1)
        self.assertTrue(self.brain.status()["verified_audit_hashes"])

if __name__=="__main__":unittest.main()
