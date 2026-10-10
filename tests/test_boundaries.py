import tempfile,os,unittest
from noetic_engine import NoeticEngine,Observation,InvalidEvidence
from noetic_engine.models import EvidenceClass

class TestCausalityAndBoundaries(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.brain=NoeticEngine(os.path.join(self.tmp.name,"test.db"))
    def tearDown(self):self.brain.close();self.tmp.cleanup()
    def lived(self,id,**kw):
        return Observation(id,"pretorius_sandbox","A laboratory conversation with a witness",
            "fictional-source",EvidenceClass.LIVED_OBSERVED,"witness",**kw)

    def test_relationship_coupling(self):
        self.brain.step(self.lived("a",relationship_delta=0.8))
        first=self.brain.step(self.lived("b"))
        self.assertGreater(first["state"]["causes"]["care"]["social"],0)
        self.assertEqual(self.brain.status()["relationships"][0]["viewpoint"],
                         "subject_estimate")

    def test_nonlived_cannot_edit_affect(self):
        claim=Observation("claim","other","I feel affection","someone-else",
                          EvidenceClass.THIRD_PARTY_CLAIM,"witness",
                          affect_delta={"affiliation":1.})
        with self.assertRaises(InvalidEvidence):self.brain.step(claim)
        self.assertEqual(self.brain.status()["memories"],0)

    def test_third_party_claim_not_lived(self):
        claim=Observation("claim","other","I heard a disturbing rumor","archive",
                          EvidenceClass.THIRD_PARTY_CLAIM,"reporter")
        self.brain.step(claim)
        record=self.brain.recall("disturbing rumor")[0]
        self.assertEqual(record["evidence_class"],"third_party_claim")
        self.assertFalse(record["verified_entailment"])

    def test_symbol_requires_lived_origin(self):
        with self.assertRaises(InvalidEvidence):
            self.brain.associate_symbol("amber","inquiry","missing")
        self.brain.step(self.lived("source"))
        self.brain.associate_symbol("amber","inquiry","source",0.3)
        r=self.brain.step(self.lived("trigger",cue="amber"))
        self.assertGreater(r["state"]["causes"]["inquiry"]["cue"],0)

    def test_outcome_is_once_and_changes_target(self):
        r=self.brain.step(self.lived("a",affect_delta={"curiosity":0.8}))
        before=self.brain.status()["field"]["inquiry"]["template"]
        self.brain.record_outcome(r["decision_id"],0.8)
        after=self.brain.status()["field"]["inquiry"]["template"]
        self.assertNotEqual(before,after)
        with self.assertRaises(ValueError):
            self.brain.record_outcome(r["decision_id"],0.2)

    def test_negative_provenance_oracle(self):
        claim=Observation("h","pretorius_sandbox","An imagined prophecy","model",
                          EvidenceClass.ORACLE_HYPOTHESIS)
        with self.assertRaises(InvalidEvidence):self.brain.step(claim)
        self.assertEqual(self.brain.status()["tick"],0)

    def test_policy_trace_does_not_claim_truth(self):
        self.brain.step(self.lived("a"))
        r=self.brain.step(self.lived("b"))
        self.assertFalse(r["memory_pointers"][0]["verified_entailment"])
        self.assertTrue(self.brain.status()["verified_audit_hashes"])

if __name__=="__main__":unittest.main()
