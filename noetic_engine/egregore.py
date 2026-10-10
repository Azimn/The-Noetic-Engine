"""Egregore: evidence-attributed, fallible models of what others *say* about us.

These records are NOT copies of anyone else's mind. Unreviewed, inferred and
third-party hearsay remain causally inert; direct quotations can influence
policy only through a separately logged review.
"""
from .models import bounded, clip, InvalidEvidence

PREDICATES=("fears","trusts","doubts","respects")
EPISTEMIC=("direct_quote","third_party_report","inference")
DISPOSITIONS=("admitted_for_policy","rejected","contested")

def record_claim(store,origin,attributed_actor,believed_subject,predicate,
                 valence,confidence,epistemic,quotation=None):
    if not all(isinstance(x,str) and x.strip() for x in
               (origin,attributed_actor,believed_subject,predicate,epistemic)):
        raise InvalidEvidence("required attribution fields are missing")
    if predicate not in PREDICATES or epistemic not in EPISTEMIC:
        raise InvalidEvidence("unknown belief predicate or attribution class")
    valence=bounded(valence)
    confidence=bounded(confidence,0,1)
    source=store.db.execute("SELECT * FROM observations WHERE origin=?",
                            (origin,)).fetchone()
    if not source:
        raise InvalidEvidence("social claim requires a recorded source event")
    quotation=quotation or ""
    if len(quotation)>500:
        raise InvalidEvidence("quoted source span too long")
    if epistemic=="direct_quote" and (not quotation or quotation not in source["text"]):
        raise InvalidEvidence("direct quotation must match source text exactly")
    if epistemic=="direct_quote" and (source["class"]!="lived_observed" or
        source["subject"]!=store.meta("subject") or
        source["actor"]!=attributed_actor):
        raise InvalidEvidence("direct quotation requires subject-owned witnessed source and matching speaker")
    cur=store.db.execute("""INSERT INTO social_claims
      (origin,attributed_actor,believed_subject,predicate,valence,confidence,epistemic,quotation,status)
      VALUES(?,?,?,?,?,?,?, ?,'unreviewed')""",
      (origin,attributed_actor,believed_subject,predicate,valence,confidence,epistemic,quotation))
    store.event(int(store.meta("tick")),"social_claim_recorded",
        {"id":cur.lastrowid,"origin":origin,"attributed_actor":attributed_actor,
         "believed_subject":believed_subject,"predicate":predicate,
         "valence":valence,"confidence":confidence,"epistemic":epistemic,"quotation":quotation})
    return cur.lastrowid

def review_claim(store,claim_id,reviewer,disposition):
    if disposition not in DISPOSITIONS or not isinstance(reviewer,str) or not reviewer.strip():
        raise ValueError("explicit review actor and valid disposition required")
    row=store.db.execute("SELECT * FROM social_claims WHERE id=?",
                         (claim_id,)).fetchone()
    if not row or row["status"]!="unreviewed":
        raise ValueError("claim absent or already reviewed")
    if disposition=="admitted_for_policy":
        source=store.db.execute("SELECT * FROM observations WHERE origin=?",
                                (row["origin"],)).fetchone()
        if (row["epistemic"]!="direct_quote" or row["believed_subject"]!=store.meta("subject")
            or source["actor"]!=row["attributed_actor"]
            or source["class"]!="lived_observed"
            or not row["quotation"] or row["quotation"] not in source["text"]):
            raise InvalidEvidence("cannot treat hearsay, inference or foreign-subject archive as policy evidence")
    tick=int(store.meta("tick"))
    store.db.execute("UPDATE social_claims SET status=? WHERE id=?",(disposition,claim_id))
    store.db.execute("""INSERT INTO social_reviews(claim_id,reviewer,disposition,tick)
                        VALUES(?,?,?,?)""",(claim_id,reviewer,disposition,tick))
    store.event(tick,"social_claim_reviewed",{"id":claim_id,"reviewer":reviewer,
                                               "disposition":disposition})

def pressure(db,actor,owner):
    rows=db.execute("""SELECT id,predicate,valence,confidence FROM social_claims
      WHERE attributed_actor=? AND believed_subject=? AND epistemic='direct_quote'
        AND status='admitted_for_policy' AND LENGTH(quotation)>0 ORDER BY id""",(actor,owner)).fetchall()
    # No claim of true mental-state access: these are attributed reports only.
    p={"care":0.0,"caution":0.0,"inquiry":0.0}
    for r in rows:
        scaled=r["valence"]*r["confidence"]*0.14
        if r["predicate"]=="fears": p["caution"]+=scaled
        elif r["predicate"]=="doubts": p["inquiry"]+=scaled
        elif r["predicate"]=="trusts": p["care"]+=scaled
        elif r["predicate"]=="respects": p["inquiry"]+=scaled
    return {k:round(clip(v,-0.25,0.25),9) for k,v in p.items()},[r["id"] for r in rows]
