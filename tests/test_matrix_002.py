"""MATRIX-002 invariants, independent scenes, checkpoint fidelity and controls."""
import unittest
from experiments.matrix_002 import (
    FIXTURE_PATH, PROFILES, FORKS, fixture_load, config, one_case, run
)

class RecoveryProtocol(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture,cls.fixture_sha=fixture_load(FIXTURE_PATH)

    def test_frozen_independent_cohort(self):
        self.assertEqual(len(self.fixture["scenarios"]),4)
        self.assertEqual(len(self.fixture["seeds"]),8)
        self.assertEqual(len(PROFILES),5)
        self.assertEqual(len(FORKS),5)
        self.assertNotIn("witness_duty",[s["id"] for s in self.fixture["scenarios"]])
        self.assertEqual(len(self.fixture_sha),64)

    def test_invalid_config_rejected(self):
        with self.assertRaises(ValueError):config("unknown_profile",7)

    def test_full_profile_has_paired_checkpoint_and_inputs(self):
        c=one_case(self.fixture,self.fixture["scenarios"][0],7,"full")
        forks=c["branches"]
        self.assertEqual(len({x["checkpoint_sha256"] for x in forks.values()}),1)
        self.assertEqual(len(forks["unperturbed"]["trace"]),
                         self.fixture["recovery_cycles"]+1)
        self.assertEqual(len(forks["reward_positive"]["trace"]),
                         self.fixture["learning_cycles"]+4)
        self.assertGreater(c["statistics"]["perturbation_initial_field_l1"],0)
        self.assertTrue(all(x["verified"] for x in forks.values()))

    def test_no_learning_control_reward_reversal(self):
        c=one_case(self.fixture,self.fixture["scenarios"][1],19,"frozen_control")
        self.assertEqual(c["statistics"]["response_reversal_mean_score_l1"],0)
        self.assertEqual(c["statistics"]["response_reversal_action_changes"],0)
        self.assertEqual(c["statistics"]["response_reversal_development_target_l1"],0)

    def test_deterministic_repeat(self):
        scenario=self.fixture["scenarios"][2]
        first=one_case(self.fixture,scenario,41,"full")
        second=one_case(self.fixture,scenario,41,"full")
        self.assertEqual(first["statistics"],second["statistics"])
        for fork in FORKS:
            self.assertEqual(first["branches"][fork]["trace"],
                             second["branches"][fork]["trace"])

if __name__=="__main__":unittest.main()
