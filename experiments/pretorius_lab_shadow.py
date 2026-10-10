"""Research-only bridge from authoritative Pretorius Laboratory to Noetic sandbox.

No production subject is touched. The world owns objects and books. This
adapter receives a host-offered qualitative fact, verifies its receipt against
the world lineage, and ONLY THEN supplies it as a synthetic witnessed event to
a separate Noetic laboratory subject. Offer != actual human or AI perception.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from noetic_engine import NoeticEngine, Observation
from noetic_engine.models import EvidenceClass
from pretorius_lab.habitat_v2 import SpatialHabitat
from pretorius_lab.observation_receipts import ObservationPort
from pretorius_lab.book_library import BookLibrary
from pretorius_lab.physics import Conflict, LabError, canonical, digest


@dataclass(frozen=True)
class GroundedDelivery:
    origin_id: str
    source: str
    receipt_hash: str
    world_epoch: str
    payload: dict
    cognitive_decision_id: int


class NoeticLaboratoryShadow:
    """A local research subject, never definitive Pretorius or a Village player.

    No API here exposes the world 'status', inspect_object, coordinates,
    hidden book pages, or unobserved future state to the cognitive consumer.
    """

    def __init__(self, world: SpatialHabitat, brain: NoeticEngine):
        self.world = world
        self.brain = brain
        self.receipts = ObservationPort(world)
        self.books = BookLibrary(world)
        if world.verify()["mode"] != "sandbox":
            raise Conflict("Noetic experimental bridge requires an isolated sandbox fork")
        if brain.config.subject_id == "pretorius" or brain.config.subject_id == "pretorius_sandbox":
            raise ValueError("use an independent noetic laboratory research subject")
        self.receipts.verify()
        self.books.verify()

    def _deliver(self, *, receipt_hash: str, world_epoch: str,
                 origin_id: str, provenance: str, payload: dict) -> GroundedDelivery:
        world = self.world.verify()
        if world["world_epoch"] != world_epoch:
            raise Conflict("offered observation belongs to a different world epoch")
        rendered = canonical(payload)
        if "xyz_mm" in rendered or "page_text" in rendered and provenance == "room_observation":
            raise Conflict("privileged geometry or unread page leaked")
        result = self.brain.step(Observation(
            origin_id=origin_id,
            subject_id=self.brain.config.subject_id,
            actor_id="laboratory_local_harness",
            text=rendered,
            source=f"pretorius-laboratory/{provenance}/{receipt_hash}/{world_epoch}",
            evidence_class=EvidenceClass.LIVED_OBSERVED,
        ))
        return GroundedDelivery(
            origin_id, provenance, receipt_hash, world_epoch, payload,
            result["decision_id"],
        )

    def inspect(self, kind: str, target: str, delivery_id: str) -> GroundedDelivery:
        """Consume one offered object/room/shelf view with a physical-world receipt."""
        result = self.receipts.expose(kind, target, delivery_id=delivery_id)
        if result["delivery_class"] != "offered_to_interface_not_proof_of_reading_or_memory":
            raise Conflict("unexpected source-view receipt class")
        payload = result["offered_payload"]
        # Verify the *specific delivery* persisted, not just a structurally
        # similar local payload. This reads the observation receipt, not world
        # hidden state, and is an operator-side check, not a subject capability.
        self.receipts.verify()
        with self.world._open() as db:
            row = db.execute(
                "SELECT payload,event_hash FROM observation_events WHERE delivery_id=?",
                (delivery_id,),
            ).fetchone()
        if not row or row[1] != result["receipt_hash"]:
            raise Conflict("missing or mismatched source delivery")
        recorded = json.loads(row[0])
        if (recorded["offered_payload"] != payload or
            recorded["payload_digest"] != digest(payload) or
            recorded["kind"] != kind or recorded["target"] != target):
            raise Conflict("altered subject-facing payload")
        return self._deliver(
            receipt_hash=result["receipt_hash"],
            world_epoch=recorded["world_epoch"],
            origin_id="lab-offer:" + delivery_id,
            provenance="room_observation",
            payload={"kind":kind,"target":target,"observation":payload,
                     "delivery_id":delivery_id,
                     "world_revision":recorded["world_revision"]},
        )

    def act(self, action: dict, *, event_id: str, expected_revision: int) -> dict:
        """Mutate ONLY the isolated laboratory fork, never from inferred memory."""
        if self.world.verify()["mode"] != "sandbox":
            raise Conflict("experiment must never write canonical home")
        result = self.world.commit(action,actor="pretorius_research",
                                   event_id=event_id,
                                   expected_revision=expected_revision)
        self.world.verify()
        return {key:result[key] for key in (
            "event_id","world_epoch","base_revision","committed_revision",
            "event_hash","action","visibility"
        )}

    def book_action(self, op: str, *, event_id: str, book_id="book:007",
                    direction: int | None=None, bookmark_id: str | None=None):
        """Book operations remain in host authority; reading is explicit."""
        return self.books.operate(book_id,op,actor="pretorius_research",
                                  event_id=event_id,direction=direction,
                                  bookmark_id=bookmark_id)

    def read_page(self, *, book_id: str, event_id: str):
        """Only text from a real, opened, source-installed page can be consumed."""
        result=self.book_action("read",book_id=book_id,event_id=event_id)
        if result["delivery_class"] != "page_offered_to_interface_not_proof_of_reading":
            raise Conflict("not a source-attested page offering")
        self.books.verify()
        # Link the page offering to the actual append-only book-event hash, not
        # simply to a caller-chosen UUID or a successful catalog lookup.
        with self.world._open() as db:
            book_row=db.execute(
                "SELECT payload,event_hash FROM books_events WHERE event_id=?",
                (result["delivery_event_id"],),
            ).fetchone()
        if not book_row:
            raise Conflict("book delivery lacks an immutable source event")
        book_event=json.loads(book_row[0])
        if (book_event["world_epoch"]!=self.world.verify()["world_epoch"] or
            book_event["action"]!={"op":"read","book_id":book_id} or
            book_event["page_receipt"]["page_digest"]!=digest(result["page_text"]) or
            book_event["page_receipt"]["edition_digest"]!=result["content_digest"]):
            raise Conflict("book delivery evidence does not match offered page")
        receipt={"book_id":result["book_id"],"edition_id":result["edition_id"],
                 "page":result["page"],"page_count":result["page_count"],
                 "page_text":result["page_text"],"content_digest":result["content_digest"],
                 "source_class":result["source_class"],
                 "delivery_event_id":result["delivery_event_id"]}
        delivery=self._deliver(
            receipt_hash=book_row[1],
            world_epoch=book_event["world_epoch"],
            origin_id="lab-book-offer:"+result["delivery_event_id"],
            provenance="installed_book_page",payload=receipt)
        return delivery

    def recall(self, query: str, limit: int=4):
        """No new view from the world; query only the subject's previous ledger."""
        return self.brain.recall(query,limit)
