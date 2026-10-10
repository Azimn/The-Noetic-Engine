import unittest
from experiments.matrix_003 import (
    BRANCHES,PROFILES,fixture_load,cfg_for,one_case,FIXTURE
)

class Matrix003(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture,cls.hash=fixture_load(FIXTURE)

    def test_frozen_scenarios_and_comparisons(self):
        self.assertEqual(len(cls_scenarios:=self.fixture["scenario"]),4)
        self.assertEqual(len(self.fixture["seeds"]),8)
        self.assertEqual(len(PROFILES),3)
        self.assertEqual(len(BRANCHES),5)
        self.assertEqual(len(self.hash),64)
        self.assertNotIn("winter_station",[s["id"] for s in cls_scenarios])

    def test_context_profiles_have_intended_gates(self):
        self.assertTrue(cfg_for("conditional",13).conditional_context)
        self.assertEqual(cfg_for("drive_only",13).conditional_repair_gain,0.0)
        self.assertFalse(cfg_for("legacy_v02",13).conditional_context)

    def test_case_has_all_forked_data_and_provenance(self):
        c=one_case(self.fixture,self.fixture["scenario"][0],13,"conditional")
        self.assertEqual(len(c["forks"]),5)
        self.assertEqual(len({f["checkpoint_sha256"] for f in c["forks"].values()}),1)
        self.assertGreater(c["measurements"]["transient_first_field_l1"],0)
        self.assertEqual(len(c["comparisons"]["persistent"]),
                         len(c["forks"]["persistent"]["trace"]))
        self.assertTrue(all(f["final_status"]["memories"]==4 for f in c["forks"].values()))

    def test_temporal_expiry_and_separate_resolution(self):
        c=one_case(self.fixture,self.fixture["scenario"][1],29,"conditional")
        transient=c["forks"]["transient"]["trace"]
        persistent=c["forks"]["persistent"]["trace"]
        resolved=c["forks"]["resolved"]["trace"]
        self.assertIn("environmental-signal",
                      transient[1]["context"]["active_source_ids"])
        self.assertNotIn("environmental-signal",
                         transient[2]["context"]["active_source_ids"])
        self.assertIn("environmental-signal",
                      persistent[-1]["context"]["active_source_ids"])
        self.assertNotIn("environmental-signal",
                         resolved[-1]["context"]["active_source_ids"])

    def test_repeatability_of_identical_case(self):
        a=one_case(self.fixture,self.fixture["scenario"][2],47,"drive_only")
        b=one_case(self.fixture,self.fixture["scenario"][2],47,"drive_only")
        self.assertEqual(a["measurements"],b["measurements"])
        self.assertEqual(a["forks"]["persistent"]["trace"],
                         b["forks"]["persistent"]["trace"])

if __name__=="__main__":unittest.main()
