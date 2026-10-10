"""Boundary checks for the prespecified synthetic evaluation program."""
import json
import tempfile
import unittest
from pathlib import Path
from experiments.matrix_v01 import (
    FIXTURE_PATH, CONDITIONS, config_for, difference, load_fixture, run_trajectory,
)

class MatrixProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture, cls.sha = load_fixture()

    def test_frozen_fixture_and_factorial(self):
        self.assertEqual(len(self.fixture["scenarios"]),4)
        self.assertEqual(len(self.fixture["seeds"]),8)
        self.assertEqual(len(CONDITIONS),13)
        self.assertEqual(len(self.sha),64)

    def test_reproducible_full_trajectory(self):
        s=self.fixture["scenarios"][0]
        a=run_trajectory(self.fixture,s,7,"full")
        b=run_trajectory(self.fixture,s,7,"full")
        self.assertEqual(a["steps"],b["steps"])
        self.assertEqual(a["final_field"],b["final_field"])
        self.assertTrue(a["verified_audit_hashes"])

    def test_oracle_and_neutral_key_parity(self):
        s=self.fixture["scenarios"][1]
        full=run_trajectory(self.fixture,s,19,"full")
        no_oracle=run_trajectory(self.fixture,s,19,"no_oracle")
        neutral=run_trajectory(self.fixture,s,19,"neutral_symbol")
        for alternative in (no_oracle,neutral):
            comparison=difference(full,alternative)
            self.assertEqual(comparison["score_l1_mean"],0)
            self.assertEqual(comparison["action_changes"],0)
        self.assertGreater(full["oracle_hypotheses"],no_oracle["oracle_hypotheses"])

    def test_causal_effect_not_conflated_with_quality(self):
        s=self.fixture["scenarios"][0]
        full=run_trajectory(self.fixture,s,41,"full")
        removed=run_trajectory(self.fixture,s,41,"no_intentions")
        self.assertGreater(difference(full,removed)["score_l1_mean"],0)

    def test_untrusted_claims_remain_unapproved(self):
        s=self.fixture["scenarios"][2]
        result=run_trajectory(self.fixture,s,73,"full")
        self.assertTrue(result["guard"]["hearsay_admission_rejected"])
        self.assertEqual(sum(x["status"]=="unreviewed"
                             for x in result["social_claims"]),1)
        self.assertEqual(result["observations"],
                         len(self.fixture["observations"]))

    def test_incomplete_fixture_fails_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"bad.json"
            p.write_text(json.dumps({"schema":"noetic-longitudinal-matrix-v01",
                                     "seeds":[1],"scenarios":[]}))
            with self.assertRaises(ValueError):
                load_fixture(p)

    def test_full_and_control_profiles_are_separate(self):
        full=config_for("full",7)
        control=config_for("v01_controller",7)
        self.assertTrue(full.developmental and full.neural_field)
        self.assertFalse(control.developmental or control.neural_field)
        self.assertEqual(full.subject_id,control.subject_id)

if __name__=="__main__":
    unittest.main()
