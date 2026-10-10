"""Evidence and controller contracts."""
from dataclasses import dataclass, field
from enum import Enum
from math import isfinite

class InvalidEvidence(ValueError):
    pass

class EvidenceClass(str, Enum):
    CANONICAL_SOURCE = "canonical_source"
    RECONSTRUCTED = "reconstructed"
    SYNTHESIZED_ADMITTED = "synthesized_admitted"
    LIVED_OBSERVED = "lived_observed"
    AGENT_SELF_REPORT = "agent_self_report"
    THIRD_PARTY_CLAIM = "third_party_claim"
    UNVERIFIED_TEXT = "unverified_text"
    ORACLE_HYPOTHESIS = "oracle_hypothesis"

TENDENCIES = ("inquiry", "care", "caution")
AFFECT = ("curiosity", "affiliation", "threat", "fatigue")
ACTION_WEIGHTS = {
    "investigate": {"inquiry": 0.9, "care": -0.1, "caution": -0.2},
    "comfort": {"inquiry": -0.25, "care": 0.95, "caution": -0.05},
    "protect": {"inquiry": -0.2, "care": 0.45, "caution": 0.8},
    "withdraw": {"inquiry": -0.3, "care": -0.3, "caution": 0.65},
    "defer": {"inquiry": -0.02, "care": -0.02, "caution": 0.05}
}
ACTIONS = tuple(ACTION_WEIGHTS)

def bounded(value, low=-1.0, high=1.0):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not isfinite(value):
        raise ValueError("finite numeric value required")
    value = float(value)
    if not low <= value <= high:
        raise ValueError("value outside permitted range")
    return value

def clip(value, low=-1.0, high=1.0):
    return max(low, min(high, value))

@dataclass(frozen=True)
class Observation:
    origin_id: str
    subject_id: str
    text: str
    source: str
    evidence_class: EvidenceClass
    actor_id: str = "environment"
    affect_delta: dict[str, float] = field(default_factory=dict)
    relationship_delta: float = 0.0
    cue: str = ""
    signals: dict[str,float] = field(default_factory=dict)

    def validate(self, owner: str):
        if not all(isinstance(x, str) and x.strip() for x in (
            self.origin_id, self.subject_id, self.text, self.source, self.actor_id)):
            raise InvalidEvidence("origin, subject, text, source and actor required")
        if len(self.text) > 16000 or len(self.origin_id) > 160:
            raise InvalidEvidence("observation too long")
        if not isinstance(self.evidence_class, EvidenceClass):
            raise InvalidEvidence("unknown evidence class")
        if self.evidence_class is EvidenceClass.ORACLE_HYPOTHESIS:
            raise InvalidEvidence("oracle ideas cannot be observed facts")
        if self.evidence_class in (EvidenceClass.LIVED_OBSERVED, EvidenceClass.AGENT_SELF_REPORT) and self.subject_id != owner:
            raise InvalidEvidence("subject provenance mismatch")
        if any(k not in AFFECT for k in self.affect_delta):
            raise InvalidEvidence("unknown affect channel")
        for v in self.affect_delta.values():
            bounded(v)
        bounded(self.relationship_delta)
        if self.signals:
            from .consequence_head import validate_facts
            validate_facts(self.signals)
            if self.evidence_class is not EvidenceClass.LIVED_OBSERVED or self.subject_id!=owner:
                raise InvalidEvidence("untrusted subject cannot supply world facts")
        if self.cue and len(self.cue) > 100:
            raise InvalidEvidence("cue too long")
        if self.evidence_class is not EvidenceClass.LIVED_OBSERVED and (
            self.affect_delta or self.relationship_delta or self.cue):
            raise InvalidEvidence("untrusted evidence cannot directly affect field")

@dataclass(frozen=True)
class Configuration:
    subject_id: str = "pretorius_sandbox"
    decay: float = 0.30
    cap_family: float = 0.45
    cap_total: float = 0.85
    regulator_gain: float = 0.10
    intentions: bool = True
    relationships: bool = True
    oracle: bool = True
    regulator: bool = True
    cues: bool = True
    policy_version: str = "noetic-v0.1"
    developmental: bool = False
    egregore: bool = False
    self_model: bool = False
    neural_field: bool = False
    neural_units: int = 96
    neural_seed: int = 1701
    conditional_context: bool = False
    conditional_repair_gain: float = 0.12
    consequence_head: bool = False
    outcome_learning_enabled: bool = True
    consequence_gain: float = 1.0
    consequence_lr: float = 0.35

    def validate(self):
        if not self.subject_id or not self.subject_id.strip():
            raise ValueError("subject required")
        for k in ("decay", "cap_family", "regulator_gain"):
            bounded(getattr(self, k), 0, 1)
        bounded(self.cap_total, 0, 3)
        bounded(self.conditional_repair_gain,0,0.5)
        bounded(self.consequence_gain,0,4)
        bounded(self.consequence_lr,0,1)
        if type(self.neural_units) is not int or not 12<=self.neural_units<=4096:
            raise ValueError("neural_units must be between 12 and 4096")
        if type(self.neural_seed) is not int or not 0<=self.neural_seed<2**31:
            raise ValueError("invalid neural seed")
