import unittest
from experiments.compare_matrix_004_archives import stable

class ArchiveComparisonTests(unittest.TestCase):
    def test_excludes_only_runtime_measurements(self):
        a={"cases":[{"reward":1,"elapsed_cpu_scope_seconds":0.3}],
           "summary":{"mean_elapsed_seconds":0.2,"correct":1}}
        b={"cases":[{"reward":1,"elapsed_cpu_scope_seconds":7.3}],
           "summary":{"mean_elapsed_seconds":2.1,"correct":1}}
        self.assertEqual(stable(a),stable(b))
    def test_fails_if_reward_or_decision_changes(self):
        a={"cases":[{"action":"protect","reward":1,"elapsed_cpu_scope_seconds":0.3}]}
        b={"cases":[{"action":"defer","reward":-1,"elapsed_cpu_scope_seconds":0.4}]}
        self.assertNotEqual(stable(a),stable(b))

if __name__=="__main__":unittest.main()
