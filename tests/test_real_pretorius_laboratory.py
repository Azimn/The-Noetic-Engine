"""Cross-repo laboratory continuity tests, optional without pinned lab package."""
import tempfile, unittest
from pathlib import Path
try:
    from pretorius_lab.habitat_v2 import SpatialHabitat
    from pretorius_lab.observation_receipts import ObservationPort
    from pretorius_lab.book_library import BookLibrary
    from pretorius_lab.physics import Conflict, LabError
    from experiments.pretorius_lab_shadow import NoeticLaboratoryShadow
    from experiments.lab_shadow_trial import transcript,research_config,PAGES
    HAS_LAB=True
except ImportError:
    HAS_LAB=False

from noetic_engine import NoeticEngine,Configuration

@unittest.skipUnless(HAS_LAB,"pinned Pretorius-Laboratory optional package not installed")
class RealLaboratoryShadowTests(unittest.TestCase):
    def test_end_to_end_restarts_preserve_world_and_cognitive_ledger(self):
        result=transcript()
        self.assertTrue(result["parent_unmodified"])
        self.assertEqual(result["world_persistent_beaker"]["condition"],"broken")
        self.assertEqual(result["world_persistent_beaker"]["observed_qualitative_location"]["anchor_id"],
                         "floor:corner:nw")
        self.assertEqual(result["world_bookmarks_after_restart"],{"copper-slip":2})
        self.assertTrue(result["memory_only_after_restart"]["page_two_absent_until_offered"])
        self.assertEqual(result["post_reboot_page_read"]["page"],2)
        self.assertEqual(result["post_reboot_page_read"]["page_text"],PAGES[1])
        self.assertGreater(len(result["memory_only_after_restart"]["beaker_retrieval"]),0)
        self.assertTrue(result["laboratory_backup_verified"])
        self.assertTrue(result["source_receipts_verified"])
        self.assertTrue(result["cognitive_ledger_verified"])

    def test_canonical_world_write_blocked_even_with_valid_tools(self):
        with tempfile.TemporaryDirectory() as td:
            home=SpatialHabitat.create(Path(td)/"home.sqlite3")
            ObservationPort(home).initialize()
            BookLibrary(home).initialize()
            with NoeticEngine(":memory:",research_config()) as brain:
                with self.assertRaises(Conflict):
                    NoeticLaboratoryShadow(home,brain)
            self.assertEqual(home.verify()["revision"],0)

    def test_doctor_production_subject_id_cannot_be_used_for_shadow(self):
        with tempfile.TemporaryDirectory() as td:
            home=SpatialHabitat.create(Path(td)/"home.sqlite3")
            BookLibrary(home).initialize()
            ObservationPort(home).initialize()
            home.fork_to(Path(td)/"fork.sqlite3")
            fork=SpatialHabitat(Path(td)/"fork.sqlite3")
            with NoeticEngine(":memory:") as default_subject:
                with self.assertRaises(ValueError):
                    NoeticLaboratoryShadow(fork,default_subject)

    def test_unobserved_book_text_never_enters_noetic_ledger(self):
        with tempfile.TemporaryDirectory() as td:
            home=SpatialHabitat.create(Path(td)/"home.sqlite3")
            BookLibrary(home).initialize()
            BookLibrary(home).install(
                "book:007",edition_id="synth-v1",title="Research Text",
                author="Fixture writer",pages=["Known page","Unseen page"],
                source_class="original_fixture",source_reference="synthetic fixture")
            ObservationPort(home).initialize()
            home.fork_to(Path(td)/"fork.sqlite3")
            fork=SpatialHabitat(Path(td)/"fork.sqlite3")
            with NoeticEngine(":memory:",research_config()) as brain:
                adapter=NoeticLaboratoryShadow(fork,brain)
                adapter.inspect("room","room:sanctum","room-1")
                self.assertFalse(any("Unseen page" in row[0] for row in
                    brain.store.db.execute("SELECT text FROM observations")))
                with self.assertRaises(LabError):
                    adapter.read_page(book_id="book:007",event_id="unopened-read")
                self.assertEqual(brain.status()["memories"],1)

if __name__=="__main__":unittest.main()
