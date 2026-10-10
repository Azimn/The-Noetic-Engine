"""Fallible self-model hypotheses, not canon or immutable identity commandments."""
from .models import InvalidEvidence,TENDENCIES,bounded,clip
PREDICATES=("values","fears","identifies_with","avoids")
DISPOSITIONS=("corroborated_for_policy","rejected","contested")

def propose(store,origin,predicate,tendency,valence,confidence):
    if predicate not in PREDICATES or tendency not in TENDENCIES:
        raise ValueError("unsupported self-model hypothesis")
    valence=bounded(valence);confidence=bounded(confidence,0,1)
    r=store.db.execute("SELECT * FROM observations WHERE origin=?",(origin,)).fetchone()
    if not r or r["subject"]!=store.meta("subject") or r["class"]!="lived_observed":
        raise InvalidEvidence("self hypothesis requires subject-owned lived evidence")
    cur=store.db.execute("""INSERT INTO self_hypotheses
      (origin,predicate,tendency,valence,confidence,status)
      VALUES(?,?,?,?,?,'provisional')""",(origin,predicate,tendency,valence,confidence))
    store.event(int(store.meta("tick")),"self_hypothesis",
                {"id":cur.lastrowid,"origin":origin,"predicate":predicate,
                 "tendency":tendency,"valence":valence,"confidence":confidence})
    return cur.lastrowid

def review(store,hypothesis_id,reviewer,disposition):
    if disposition not in DISPOSITIONS or not reviewer or not reviewer.strip():
        raise ValueError("explicit review required")
    row=store.db.execute("SELECT status FROM self_hypotheses WHERE id=?",
                         (hypothesis_id,)).fetchone()
    if not row or row["status"]!="provisional":
        raise ValueError("missing or previously reviewed self hypothesis")
    store.db.execute("UPDATE self_hypotheses SET status=? WHERE id=?",
                     (disposition,hypothesis_id))
    tick=int(store.meta("tick"))
    store.db.execute("INSERT INTO self_reviews(hypothesis_id,reviewer,disposition,tick) VALUES(?,?,?,?)",
                     (hypothesis_id,reviewer,disposition,tick))
    store.event(tick,"self_review",{"id":hypothesis_id,"reviewer":reviewer,
                                    "disposition":disposition})

def pressure(db):
    p={k:0. for k in TENDENCIES};sources=[]
    for r in db.execute("""SELECT * FROM self_hypotheses
            WHERE status='corroborated_for_policy' ORDER BY id"""):
        p[r["tendency"]]+=0.10*r["valence"]*r["confidence"]
        sources.append(r["id"])
    return {k:round(clip(v,-0.20,0.20),9) for k,v in p.items()},sources
