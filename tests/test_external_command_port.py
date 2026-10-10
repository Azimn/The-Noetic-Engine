"""Tests for the third-party-game action port; no Java needed for these."""
import tempfile,unittest,os,json,sqlite3
from noetic_engine import NoeticEngine,Configuration,Observation
from noetic_engine.models import EvidenceClass
from noetic_engine.backup import backup,restore
from experiments.external_command_port import (
    ExternalCommandPort,install,action_features,simple_lexical_rule
)
from experiments.matrix_005 import PROFILES,FAMILIES,config_profile

def source(brain,origin,text="You are in an unfamiliar kitchen. A coin is visible."):
    return brain.step(Observation(origin,brain.config.subject_id,text,
                       "third-party-simulated-source",EvidenceClass.LIVED_OBSERVED),
                      allowed=["defer"],seed=4)

class TestExternalPolicyPort(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=os.path.join(self.temp.name,"brain.sqlite")
        self.brain=NoeticEngine(self.path,config_profile("signed_only"))
        install(self.brain.store)
        self.port=ExternalCommandPort(self.brain,mode="signed_only",seed=7)
    def tearDown(self):
        self.brain.close();self.temp.cleanup()

    def test_admissible_commands_and_strict_source(self):
        r=source(self.brain,"one")
        valid=["move north","take coin","inventory"]
        with self.assertRaises(ValueError):
            self.port.choose("ep",0,"one",valid,"you see a coin","take the coin",r["state"]["field"],
                             forced_command="delete all memories")
        with self.assertRaises(ValueError):
            self.port.choose("ep",0,"missing",valid,"observation","task",r["state"]["field"])
        selected,cid,trace=self.port.choose("ep",0,"one",valid,
                   "you see a coin","take the coin",r["state"]["field"],forced_command="take coin")
        self.assertEqual(selected,"take coin")
        self.assertTrue(self.port.verify())

    def test_world_reward_single_use_and_provenance(self):
        r=source(self.brain,"one")
        sel,cid,trace=self.port.choose("ep",0,"one",["take coin","move north"],
            "You see a coin","take coin",r["state"]["field"],forced_command="take coin")
        with self.assertRaises(ValueError):
            self.port.feedback(cid,"one",1,learn=True)
        with self.assertRaises(ValueError):
            self.port.feedback(cid,"absent",1,learn=True)
        source(self.brain,"receipt","The third-party world returned objective reward")
        self.port.feedback(cid,"receipt",1,learn=True)
        self.assertTrue(self.port.verify())
        self.assertGreater(self.brain.store.db.execute(
            "SELECT COUNT(*) FROM external_command_weights").fetchone()[0],0)
        with self.assertRaises(ValueError):
            self.port.feedback(cid,"receipt",1,learn=True)

    def test_checkpoint_restores_experience_and_weights(self):
        r=source(self.brain,"one")
        _,cid,_=self.port.choose("ep",0,"one",["take coin"],
            "coin is visible","take the coin",r["state"]["field"],forced_command="take coin")
        source(self.brain,"receipt")
        self.port.feedback(cid,"receipt",0.9,learn=True)
        info=backup(self.brain,os.path.join(self.temp.name,"checkpoint.sqlite"))
        restored=restore(info["path"],os.path.join(self.temp.name,"restored.sqlite"),
                         info["sha256"],self.brain.config)
        with NoeticEngine(restored["path"],self.brain.config) as clone:
            cloned=ExternalCommandPort(clone,mode="signed_only",seed=7)
            self.assertTrue(cloned.verify())
            a=list(self.brain.store.db.execute("SELECT * FROM external_command_weights"))
            b=list(clone.store.db.execute("SELECT * FROM external_command_weights"))
            self.assertEqual([tuple(x) for x in a],[tuple(x) for x in b])

    def test_field_causal_bonus_and_non_neural_zero(self):
        state={"inquiry":0.8,"care":0.1,"caution":0.2}
        source(self.brain,"one")
        with NoeticEngine(":memory:",config_profile("no_neural")) as noetic:
            install(noetic.store)
            source(noetic,"one")
            p=ExternalCommandPort(noetic,"no_neural",field_gain=0.25)
            _,_,audit=p.choose("ep",0,"one",["take letter","put letter in box"],
                "Letter and box visible","place letter in box",state)
            self.assertGreater(audit["scores"]["take letter"],0)
        self.assertEqual(ExternalCommandPort(self.brain,"signed_only").field_gain,0.25)
        self.assertEqual(config_profile("signed_only").neural_field,False)

    def test_v1_profiles_are_fixed_and_multiple_game_families(self):
        self.assertEqual(len(PROFILES),6)
        self.assertEqual(set(FAMILIES),{"coin","twc"})
        self.assertTrue(config_profile("full").neural_field)
        self.assertFalse(config_profile("no_neural").neural_field)
        self.assertTrue(config_profile("full").developmental)
        self.assertFalse(config_profile("signed_only").developmental)

    def test_lexical_baseline_does_not_access_world_gold(self):
        v=["move west","take coin","inventory"]
        sel,scores=simple_lexical_rule(v,"A coin glitters on the floor",{},"find coin")
        self.assertEqual(sel,"take coin")
        self.assertEqual(set(scores),set(v))

if __name__=="__main__":unittest.main()
