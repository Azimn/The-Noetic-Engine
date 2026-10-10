"""End-to-end permanent Pretorius Laboratory / Noetic shadow rehearsal.

This is scripted *environment interaction*, not autonomous Pretorius behavior,
psychological continuity, real-world observation, or production memory transfer.
The laboratory is a forked host and never the canonical parent.
"""
import json
import tempfile
from pathlib import Path
from noetic_engine import NoeticEngine,Configuration
from pretorius_lab.habitat_v2 import SpatialHabitat
from pretorius_lab.observation_receipts import ObservationPort
from pretorius_lab.book_library import BookLibrary
from .pretorius_lab_shadow import NoeticLaboratoryShadow

PAGES=[
    "At sunrise the amber lamp stood beside the blue apparatus.",
    "On the following day the amber lamp was extinguished and the glass instrument cooled.",
    "A third observation was left unrecorded pending evidence from a separate witness.",
]

def research_config():
    return Configuration(subject_id="noetic_lab_shadownode",policy_version="lab-shadow-v01",
                         developmental=True,neural_field=False,oracle=False,
                         egregore=False,self_model=False)

def transcript():
    with tempfile.TemporaryDirectory() as d:
        folder=Path(d)
        parent=SpatialHabitat.create(folder/"parent.sqlite")
        catalog=BookLibrary(parent)
        catalog.initialize()
        catalog.install("book:007",edition_id="noetic-test-edition-v1",
             title="Laboratory Observation Journal",author="Synthetic fixture author",
             source_class="original_fixture",source_reference="Noetic shadow experiment fixture, not Pretorius canon",
             pages=PAGES,event_id="fixture-install-007")
        ObservationPort(parent).initialize()
        parent_pre=parent.verify()
        fork_info=parent.fork_to(folder/"isolated_world.sqlite")
        fork=SpatialHabitat(folder/"isolated_world.sqlite")
        cfg=research_config()
        brainpath=folder/"noetic-shadow.sqlite"
        with NoeticEngine(str(brainpath),cfg) as brain:
            bridge=NoeticLaboratoryShadow(fork,brain)
            initial=bridge.inspect("object","beaker:001","initial-beaker")
            shelf=bridge.inspect("shelf","shelf:3","initial-shelf")
            book_initial=bridge.inspect("object","book:007","initial-book")
            floor=bridge.inspect("shelf","floor:sanctum","floor-location")
            room=bridge.inspect("room","room:sanctum","initial-room")
            bridge.book_action("open",event_id="book-open")
            page_one=bridge.read_page(book_id="book:007",event_id="book-page-one")
            bridge.book_action("turn",event_id="book-next",direction=1)
            bridge.book_action("mark",event_id="bookmark-set",bookmark_id="copper-slip")
            bridge.book_action("close",event_id="book-close")
            # Do not hand Noetic page two; book turn/mark is not equivalent
            # to perceptual uptake or an autobiographical observation.
            corner=next(v["anchor_id"] for v in floor.payload["observation"]["positions"]
                        if v["anchor_id"]=="floor:corner:nw")
            p=fork.verify()
            br=bridge.act({"op":"break","object_id":"beaker:001"},
                event_id="break-beaker",expected_revision=p["revision"])
            p=fork.verify()
            co=bridge.act({"op":"collect","object_id":"beaker:001"},
                event_id="collect-fragments",expected_revision=p["revision"])
            p=fork.verify()
            mv=bridge.act({"op":"place","object_id":"beaker:001","anchor_id":corner},
                event_id="move-broken-beaker",expected_revision=p["revision"])
            delivered_after=bridge.inspect("object","beaker:001","after-beaker")
            brain_before=brain.status()
            world_before=fork.verify()
        # Two separately persistent authorities survive process/connection restart.
        fork=SpatialHabitat(folder/"isolated_world.sqlite")
        with NoeticEngine(str(brainpath),cfg) as brain:
            bridge=NoeticLaboratoryShadow(fork,brain)
            # Memory-only stage: no world port called before recall.
            location_memory=bridge.recall("beaker",limit=20)
            book_memory=bridge.recall("amber lamp",limit=20)
            stored=[r[0] for r in brain.store.db.execute("SELECT text FROM observations")]
            if any(PAGES[1] in s for s in stored):
                raise AssertionError("unread page appeared in autobiographical ledger")
            reopened_world=fork.verify()
            book_state=bridge.books.catalog("book:007")["book:007"]
            if book_state["bookmarks"]!={"copper-slip":2}:
                raise AssertionError("physical bookmark did not persist")
            if not location_memory or not book_memory:
                raise AssertionError("memory-only lexical retrieval failed")
            bridge.book_action("open_mark",event_id="book-open-from-mark",
                               bookmark_id="copper-slip")
            page_two=bridge.read_page(book_id="book:007",event_id="book-page-two")
            after_read=brain.status()
            fork.backup_to(folder/"verified-backup.sqlite")
            rescued=SpatialHabitat(folder/"verified-backup.sqlite")
            backup_verified=rescued.verify()["verified"]
            book_backup_verified=BookLibrary(rescued).verify()["verified"]
        parent_after=parent.verify()
        if parent_pre!=parent_after:
            raise AssertionError("isolated fork modified its physical parent")
        if reopened_world["world_epoch"]!=fork_info["world_epoch"]:
            raise AssertionError("sandbox lineage changed after restart")
        if reopened_world["head_hash"]!=world_before["head_hash"]:
            raise AssertionError("world changed across memory-only reboot")
        if not all(x["verified_audit_hashes"] for x in (brain_before,after_read)):
            raise AssertionError("Noetic ledger integrity was not preserved")
        if page_two.payload["page_text"] != PAGES[1]:
            raise AssertionError("page text not backed by installed edition")
        state=fork.locate("beaker:001")
        if state["condition"]!="broken" or state["location"]["anchor_id"]!=corner:
            raise AssertionError("broken beaker changed or disappeared")
        return {
            "protocol":"noetic-laboratory-shadow-v01",
            "epistemic_level":"scripted_sandbox_bridge_not_autonomous_Pretorius_or_identity_validation",
            "source":{"repository":"Azimn/Pretorius-Laboratory",
                      "type":"version_pinned_authoritative_local_world"},
            "parent_unmodified":True,"parent_world_epoch":parent_pre["world_epoch"],
            "fork_world_epoch":fork_info["world_epoch"],
            "world_restarted_at_revision":reopened_world["revision"],
            "world_persistent_beaker":{"id":"beaker:001","condition":state["condition"],
                       "observed_qualitative_location":state["location"]},
            "world_bookmarks_after_restart":book_state["bookmarks"],
            "memory_only_after_restart":{
                "beaker_retrieval":[{"origin_id":x["origin_id"],
                    "evidence_class":x["evidence_class"],"lexical_score":x["lexical_score"]}
                    for x in location_memory],
                "book_retrieval_count":len(book_memory),
                "page_one_offered_and_consumed":True,
                "page_two_absent_until_offered":True,
            },
            "post_reboot_page_read":{"page":page_two.payload["page"],
                "page_text":page_two.payload["page_text"],
                "origin":page_two.origin_id,"edition_digest":page_two.payload["content_digest"]},
            "physical_events":[br,co,mv],
            "brain_memories_before_restart":brain_before["memories"],
            "brain_memories_after_postrestart_read":after_read["memories"],
            "source_receipts_verified":ObservationPort(fork).verify()["verified"],
            "laboratory_world_verified":reopened_world["verified"],
            "laboratory_book_verified":BookLibrary(fork).verify()["verified"],
            "laboratory_backup_verified":backup_verified and book_backup_verified,
            "cognitive_ledger_verified":after_read["verified_audit_hashes"],
            "limits":[
                "All actions were scripted by test harness",
                "Cognitive recall is sparse lexical retrieval, not semantic autobiographical verification",
                "No model swap, environment-controlled agent, or human character adjudication",
                "No Village projection, production cognition or autonomous character state was mutated",
                "Receipt proves offered data, not a human or artificial subject experienced it",
            ],
        }

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True)
    args=p.parse_args()
    data=transcript()
    dst=Path(args.output);dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_text(json.dumps(data,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"experiment":data["protocol"],
       "parent_unmodified":data["parent_unmodified"],
       "persistent_beaker":data["world_persistent_beaker"],
       "bookmark":data["world_bookmarks_after_restart"],
       "unread_page_blocked":data["memory_only_after_restart"]["page_two_absent_until_offered"],
       "backup_verified":data["laboratory_backup_verified"],
       "cognitive_ledger_verified":data["cognitive_ledger_verified"]},sort_keys=True))

if __name__=="__main__":
    main()
