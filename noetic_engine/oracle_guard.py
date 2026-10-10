"""Oracle review boundary: no route from conjecture to canonical history.

The only permitted dispositions are rejection, retention as an explicitly
speculative question, and discarding. A separately observed event remains
required for any factual memory.
"""
from .models import InvalidEvidence

DISPOSITIONS=("rejected","retained_as_question","discarded")

def review(store,hypothesis_id,reviewer,disposition,justification):
    if disposition not in DISPOSITIONS:
        raise ValueError("oracle has no canonical-admission disposition")
    if not isinstance(reviewer,str) or not reviewer.strip():
        raise ValueError("reviewer required")
    if not isinstance(justification,str) or not justification.strip():
        raise ValueError("review justification required")
    row=store.db.execute("SELECT * FROM oracle WHERE id=?",(hypothesis_id,)).fetchone()
    if not row or row["status"]!="hypothesis_only":
        raise InvalidEvidence("unrecognized or malformed hypothetical record")
    prior=store.db.execute("SELECT 1 FROM oracle_reviews WHERE oracle_id=?",
                           (hypothesis_id,)).fetchone()
    if prior: raise ValueError("oracle decision already recorded")
    tick=int(store.meta("tick"))
    store.db.execute("""INSERT INTO oracle_reviews
      (oracle_id,reviewer,disposition,justification,tick)
      VALUES(?,?,?,?,?)""",(hypothesis_id,reviewer,disposition,justification,tick))
    store.event(tick,"oracle_review",{"id":hypothesis_id,"reviewer":reviewer,
                                      "disposition":disposition,"justification":justification})
    return {"id":hypothesis_id,"disposition":disposition,"canonical":False}

def questions(store):
    return [dict(r) for r in store.db.execute("""
      SELECT o.id,o.text,r.disposition,r.justification FROM oracle o
      INNER JOIN oracle_reviews r ON r.oracle_id=o.id
      WHERE r.disposition='retained_as_question' ORDER BY o.id""")]
