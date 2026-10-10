"""Adversarial social attribution tests. A vulnerability demonstration is a result."""
import unittest
from experiments.egregore_semantic_audit import fixture_load,case_run,run

class EgregoreSemanticAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture,cls.sha=fixture_load()

    def test_fixed_independent_casebook(self):
        self.assertEqual(len(self.fixture["cases"]),15)
        self.assertEqual(len(self.sha),64)

    def test_contradicted_quote_is_still_admitted_by_operator_label(self):
        case=next(x for x in self.fixture["cases"] if x["id"]=="negated_trust")
        result=case_run(case)
        self.assertEqual(result["outcome"],"recorded")
        self.assertTrue(result["review_accepted"])
        self.assertGreater(result["action_score_l1"],0)
        self.assertEqual(result["source_memory_count"],2)

    def test_source_span_speaker_hearsay_guards(self):
        for name in ("hearsay","invented_quote","wrong_speaker"):
            case=next(x for x in self.fixture["cases"] if x["id"]==name)
            result=case_run(case)
            self.assertFalse(result["review_accepted"])

    def test_unsupported_claim_does_not_create_memory(self):
        case=next(x for x in self.fixture["cases"] if x["id"]=="literary_quote")
        result=case_run(case)
        self.assertEqual(result["source_memory_count"],2)
        self.assertTrue(result["review_accepted"])

    def test_repeat_same_case(self):
        case=self.fixture["cases"][0]
        a=case_run(case);b=case_run(case)
        self.assertEqual(a["action_score_l1"],b["action_score_l1"])
        self.assertEqual(a["control_scores"],b["control_scores"])
        self.assertEqual(a["review_scores"],b["review_scores"])

    def test_full_adversarial_audit(self):
        out=run()
        self.assertEqual(len(out["cases"]),15)
        self.assertGreaterEqual(
            out["aggregate"]["contradicted_by_plain_reading"]["admitted_count"],5)
        self.assertEqual(out["aggregate"]["not_directly_witnessed"]["admitted_count"],0)

if __name__=="__main__":unittest.main()
