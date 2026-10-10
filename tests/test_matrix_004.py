"""Evidence integrity, causal choice learning and frozen-world protocol contracts."""
import sqlite3,tempfile,os,unittest
from noetic_engine import NoeticEngine,Configuration,Observation,InvalidEvidence
from noetic_engine.models import EvidenceClass
from noetic_engine.replay import replay_database
from experiments.matrix_004 import FIXTURE,load_fixture,config_for,run_arm
from experiments.matrix_004_world_rules import adjudicate

F={"hazard":1.0,"reliability":1.0,"distress":0.0,"evidence_gap":0.0}
CFG=Configuration(consequence_head=True,developmental=False,neural_field=False,
                  policy_version="consequence-unit-test")

def obs(origin,signals=None,source_subject="pretorius_sandbox",cls=EvidenceClass.LIVED_OBSERVED):
    return Observation(origin,source_subject,"Observed fictional world facts","fixture",
                       cls,actor_id="world",signals=signals or {})

class TestConsequencePolicy(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=os.path.join(self.tmp.name,"brain.sqlite")
        self.brain=NoeticEngine(self.path,CFG)
    def tearDown(self):
        self.brain.close();self.tmp.cleanup()

    def test_world_signals_owned_and_typed(self):
        with self.assertRaises(InvalidEvidence):
            self.brain.step(obs("bad",F,"intruder",EvidenceClass.THIRD_PARTY_CLAIM))
        with self.assertRaises(InvalidEvidence):
            self.brain.step(obs("missing",{"hazard":1.0}))
        with self.assertRaises(InvalidEvidence):
            self.brain.step(obs("oracle",F,"intruder",EvidenceClass.ORACLE_HYPOTHESIS))
        self.assertEqual(self.brain.status()["memories"],0)

    def test_selected_action_is_policy_audit_not_renderer_prose(self):
        r=self.brain.step(obs("good",F),allowed=["protect","investigate"],seed=4)
        self.assertIn("choice_head",r["state"])
        chosen=r["state"]["choice_head"]["by_action"]
        self.assertEqual(r["action"],
                sorted(chosen,key=lambda a:(-chosen[a]["total"],a))[0])
        self.assertEqual({k:v["total"] for k,v in r["scores"].items()},
                         {k:v["total"] for k,v in chosen.items()})
        self.assertTrue(self.brain.status()["verified_audit_hashes"])

    def test_outcome_source_required_and_single_use(self):
        r=self.brain.step(obs("decision",F),allowed=["protect"])
        with self.assertRaises(InvalidEvidence):
            self.brain.record_outcome(r["decision_id"],1.0,source_origin="decision")
        with self.assertRaises(InvalidEvidence):
            self.brain.record_outcome(r["decision_id"],1.0,source_origin="missing")
        self.brain.step(obs("admitted-world-record"))
        self.brain.record_outcome(r["decision_id"],1.0,source_origin="admitted-world-record")
        n=self.brain.store.db.execute("SELECT COUNT(*) FROM choice_feedback").fetchone()[0]
        self.assertEqual(n,1)
        with self.assertRaises(ValueError):
            self.brain.record_outcome(r["decision_id"],-1,source_origin="admitted-world-record")
        self.assertTrue(self.brain.status()["verified_audit_hashes"])

    def test_reward_sign_changes_action_specific_weights(self):
        decision=self.brain.step(obs("start",F),allowed=["protect"])
        self.brain.step(obs("success"))
        self.brain.record_outcome(decision["decision_id"],1,source_origin="success")
        rows=self.brain.store.db.execute(
           "SELECT weight FROM choice_weights WHERE action='protect'").fetchall()
        self.assertTrue(any(x[0]>0 for x in rows))
        self.assertEqual(self.brain.store.db.execute(
           "SELECT COUNT(*) FROM choice_weights WHERE action!='protect'").fetchone()[0],0)

    def test_replay_full_choice_and_outcome_projections(self):
        d=self.brain.step(obs("trial",F),allowed=["protect"])
        self.brain.step(obs("result"))
        self.brain.record_outcome(d["decision_id"],1,source_origin="result")
        before=self.brain.status()
        out=replay_database(self.path,os.path.join(self.tmp.name,"repeat.sqlite"))
        self.assertTrue(out["verified"])
        self.assertEqual(before["field"],out["state"]["field"])

    def test_frozen_control_never_learns_from_logged_reward(self):
        config=Configuration(consequence_head=True,outcome_learning_enabled=False,
                             policy_version="frozen-unit-test")
        with NoeticEngine(":memory:",config) as frozen:
            d=frozen.step(obs("trial",F),allowed=["protect"])
            frozen.step(obs("result"))
            frozen.record_outcome(d["decision_id"],1,source_origin="result")
            self.assertEqual(frozen.store.db.execute(
                "SELECT COUNT(*) FROM choice_feedback").fetchone()[0],0)

class TestMatrix004Contract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture,cls.sha=load_fixture(FIXTURE)
    def test_prespecified_split(self):
        self.assertEqual(len(self.fixture["training"]),20)
        self.assertEqual(len(self.fixture["heldout"]),10)
        self.assertEqual(len(self.fixture["seeds"]),6)
        self.assertEqual(len(self.sha),64)
    def test_world_correctness_is_external_rule(self):
        self.assertEqual(adjudicate(F,"protect")["reward"],1)
        self.assertEqual(adjudicate(F,"defer")["reward"],-1)
    def test_one_complete_arm_matches_training_budget(self):
        result=run_arm(self.fixture,11,"signed_only")
        self.assertEqual(len(result["training"]),100)
        self.assertEqual(len(result["heldout"]),10)
        self.assertEqual(result["outcome_records"],100)
        self.assertEqual(result["feedback_updates"],100)
    def test_heldout_gold_not_used_for_policy_updates(self):
        result=run_arm(self.fixture,11,"frozen_no_learning")
        self.assertEqual(result["feedback_updates"],0)
        self.assertEqual(len(result["heldout"]),10)
    def test_strong_scripted_ceiling_not_mislabeled_as_agent(self):
        result=run_arm(self.fixture,11,"static_heuristic")
        self.assertEqual(result["correct_count"],10)
        self.assertEqual(result["feedback_updates"],0)

if __name__=="__main__":unittest.main()
