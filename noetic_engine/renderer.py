"""Renderer-neutral policy port with evidence and uncertainty labels.

Noetic chooses actions. A renderer expresses an already selected action and
is never permitted to author the canonical history by writing text.
"""
from dataclasses import dataclass
from typing import Protocol,Any

@dataclass(frozen=True)
class DecisionBrief:
    decision_id: int
    subject_id: str
    action: str
    allowed_actions: tuple[str,...]
    evidence: tuple[dict,...]
    social_claim_ids: tuple[int,...]
    speculative: tuple[dict,...]
    field: dict
    configuration_digest: str

class Renderer(Protocol):
    def render(self,brief:DecisionBrief)->str: ...

def brief_from_decision(engine,decision_id):
    import json
    r=engine.store.db.execute("SELECT audit FROM decisions WHERE id=?",
                              (decision_id,)).fetchone()
    if not r:raise ValueError("unknown decision")
    data=json.loads(r["audit"])
    hypotheses=()
    if data["oracle"] is not None:
        h=data["oracle"]
        hypotheses=({"text":h["text"],"status":"hypothesis_only",
                     "source_ids":h["source_ids"]},)
    evidence=tuple({"record_id":e["id"],"origin_id":e["origin_id"],
                    "subject_id":e["subject_id"],"evidence_class":e["evidence_class"],
                    "source":e["source"],"excerpt":e["excerpt"],
                    "verified_entailment":False}
                   for e in data["memory_pointers"])
    return DecisionBrief(
      decision_id,engine.config.subject_id,data["action"],
      tuple(data["allowed_actions"]),evidence,
      tuple(data["state"].get("attributed_claim_ids",())),
      hypotheses,data["state"]["field"],engine.store.meta("config_digest"))

class DiagnosticRenderer:
    """Truthful and deterministic, not a stand-in for model-based performance."""
    def render(self,brief):
        if brief.action not in brief.allowed_actions:
            raise ValueError("brief contains forbidden action")
        return ("Selected policy: "+brief.action+". Evidence pointers: "+
                str(len(brief.evidence))+". Hypotheses are noncanonical: "+
                str(len(brief.speculative))+".")

class DecoratedRenderer:
    """A second deterministic renderer for cross-renderer API invariants only."""
    def render(self,brief):
        if brief.action not in brief.allowed_actions:
            raise ValueError("forbidden action")
        return "["+brief.subject_id+"] "+brief.action.upper()
