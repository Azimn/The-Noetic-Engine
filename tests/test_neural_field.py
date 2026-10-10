"""Causal recurrent engagement, seed replay and learned-weight integrity."""
import os,tempfile,unittest
from noetic_engine import NoeticEngine,Configuration,Observation
from noetic_engine.models import EvidenceClass
from noetic_engine.neural_field import load
from noetic_engine.replay import replay_database

CFG=Configuration(developmental=True,egregore=True,self_model=True,
                  neural_field=True,neural_units=48,neural_seed=122,
                  policy_version="noetic-v0.2-neural")
def event(i):
    return Observation(str(i),"pretorius_sandbox",
        "Doctor investigates troubling news","synthetic-fixture",
        EvidenceClass.LIVED_OBSERVED,"observer",
        affect_delta={"curiosity":0.35})

class RecurrentFieldTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=os.path.join(self.temp.name,"source.sqlite")
        self.engine=NoeticEngine(self.path,CFG)
    def tearDown(self):self.engine.close();self.temp.cleanup()

    def test_neural_state_changes_action_scores(self):
        before=self.engine.status()
        r=self.engine.step(event(1),allowed=["investigate","protect"])
        self.assertIn("neural",r["state"])
        self.assertEqual(r["state"]["neural"]["units"],48)
        self.assertEqual(self.engine.status()["neural_field"]["updates"],1)
        self.assertTrue(self.engine.status()["verified_audit_hashes"])
        self.assertNotEqual(before["field"]["inquiry"]["activation"],
                            r["state"]["field"]["inquiry"])

    def test_reward_updates_weights_and_restart(self):
        r=self.engine.step(event(1),allowed=["investigate"])
        before=load(self.engine.store.db,CFG.subject_id)
        self.engine.record_outcome(r["decision_id"],1.)
        after=load(self.engine.store.db,CFG.subject_id)
        self.assertEqual(after["outcomes"],1)
        self.assertNotEqual(before["edges"],after["edges"])
        self.engine.close()
        self.engine=NoeticEngine(self.path,CFG)
        self.assertEqual(load(self.engine.store.db,CFG.subject_id)["edges"],after["edges"])

    def test_neural_replay_matches_full_event_trace(self):
        r=self.engine.step(event(1),seed=4)
        self.engine.record_outcome(r["decision_id"],0.7)
        self.engine.step(event(2),seed=4)
        result=replay_database(self.path,os.path.join(self.temp.name,"replay.sqlite"))
        self.assertTrue(result["verified"])
        self.assertEqual(result["state"]["neural_field"]["updates"],2)
        self.assertEqual(result["state"]["neural_field"]["outcomes"],1)

    def test_fixed_seeds_deterministic(self):
        a=self.engine.step(event(1),seed=17)
        other=NoeticEngine(":memory:",CFG)
        try:
            b=other.step(event(1),seed=17)
            self.assertEqual(a["scores"],b["scores"])
            self.assertEqual(a["state"]["neural"],b["state"]["neural"])
        finally:other.close()

if __name__=="__main__":unittest.main()
