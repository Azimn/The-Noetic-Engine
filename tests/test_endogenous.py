import os,tempfile,unittest
from noetic_engine import NoeticEngine,Configuration,Observation
from noetic_engine.models import EvidenceClass
from noetic_engine.replay import replay_database

CFG=Configuration(developmental=True,neural_field=True,neural_units=24,
                  policy_version="noetic-v0.2-pulse")
class EndogenousCognition(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=os.path.join(self.tmp.name,"mind.sqlite")
        self.brain=NoeticEngine(self.path,CFG)
    def tearDown(self):self.brain.close();self.tmp.cleanup()

    def test_pulse_has_no_false_lived_memory(self):
        before=self.brain.status()["memories"]
        self.brain.add_intention("p","Consider the experiment","inquiry")
        r=self.brain.pulse(seed=4,mode="wake")
        self.assertTrue(r["endogenous"])
        self.assertIsNone(r["observation_id"])
        self.assertEqual(self.brain.status()["memories"],before)
        self.assertIn(r["action"],r["allowed_actions"])

    def test_sleep_decreases_arousal_and_never_actions(self):
        o=Observation("l1",CFG.subject_id,"Danger in the laboratory","fixture",
                      EvidenceClass.LIVED_OBSERVED,
                      affect_delta={"threat":0.8})
        self.brain.step(o)
        before=self.brain.status()["affect"]["threat"]
        r=self.brain.pulse(mode="sleep",seed=4)
        self.assertEqual(r["action"],"defer")
        self.assertLess(self.brain.status()["affect"]["threat"],before)
        self.assertEqual(self.brain.status()["memories"],1)

    def test_endogenous_history_is_replayable(self):
        self.brain.pulse(mode="wake",seed=12)
        self.brain.pulse(mode="sleep",seed=12)
        report=replay_database(self.path,os.path.join(self.tmp.name,"copy.sqlite"))
        self.assertTrue(report["verified"])
        self.assertEqual(report["decision_count"],2)

if __name__=="__main__":unittest.main()
