"""Feature-gated conditional context source boundaries and independent replay."""
import os,tempfile,unittest
from noetic_engine import NoeticEngine,Configuration,Observation,InvalidEvidence
from noetic_engine.models import EvidenceClass
from noetic_engine.replay import replay_database

def lived(i,subject="pretorius_sandbox",classification=EvidenceClass.LIVED_OBSERVED):
    return Observation(i,subject,"External context reported in observation", "synthetic",
                       classification,actor_id="environment")

CFG=Configuration(conditional_context=True,policy_version="noetic-context-gate-test")

class ConditionalSourceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=os.path.join(self.tmp.name,"brain.sqlite")
        self.brain=NoeticEngine(self.path,CFG)
    def tearDown(self):
        self.brain.close();self.tmp.cleanup()

    def test_transient_expires_without_fabricating_memories(self):
        self.brain.step(lived("observed"))
        self.brain.bind_context("shock","observed","caution",0.8,"transient")
        one=self.brain.pulse(seed=5)
        self.assertIn("shock",one["state"]["context"]["active_source_ids"])
        two=self.brain.pulse(seed=6)
        self.assertNotIn("shock",two["state"]["context"]["active_source_ids"])
        self.assertEqual(self.brain.status()["memories"],1)

    def test_persistent_requires_new_resolution_evidence(self):
        self.brain.step(lived("first"))
        self.brain.bind_context("hazard","first","caution",0.8,"persistent")
        for n in range(4):
            p=self.brain.pulse(seed=n)
            self.assertIn("hazard",p["state"]["context"]["active_source_ids"])
        with self.assertRaises(InvalidEvidence):
            self.brain.resolve_context("hazard","first")
        self.brain.step(lived("safe"))
        self.brain.resolve_context("hazard","safe")
        self.assertNotIn("hazard",self.brain.pulse()["state"]["context"]["active_source_ids"])

    def test_foreign_archive_cannot_introduce_or_resolve_world_state(self):
        self.brain.step(lived("foreign","someone_else",EvidenceClass.THIRD_PARTY_CLAIM))
        with self.assertRaises(InvalidEvidence):
            self.brain.bind_context("evil","foreign","care",1,"persistent")
        self.assertEqual(self.brain.status()["environmental_context"],[])
        self.brain.step(lived("subject_observed"))
        self.brain.bind_context("one","subject_observed","care",0.5,"persistent")
        with self.assertRaises(InvalidEvidence):
            self.brain.resolve_context("one","foreign")

    def test_config_feature_gate_blocks_unapproved_runtime(self):
        with NoeticEngine(":memory:") as baseline:
            baseline.step(lived("source"))
            with self.assertRaises(ValueError):
                baseline.bind_context("bad","source","caution",0.6,"transient")

    def test_exact_replay_with_context_termination(self):
        self.brain.step(lived("begin"))
        self.brain.bind_context("event","begin","caution",0.75,"persistent")
        self.brain.pulse(seed=2)
        self.brain.step(lived("end"))
        self.brain.resolve_context("event","end")
        self.brain.pulse(mode="sleep",seed=3)
        before=self.brain.status()
        r=replay_database(self.path,os.path.join(self.tmp.name,"replay.sqlite"))
        self.assertTrue(r["verified"])
        self.assertEqual(before["field"],r["state"]["field"])
        self.assertEqual(before["environmental_context"],r["state"]["environmental_context"])

if __name__=="__main__":unittest.main()
