"""Lexical memory evidence pointers; no semantic truth or entailment claims."""
import re
def tokens(s): return {x for x in re.findall(r"[a-z0-9]+",s.lower()) if len(x)>2}
def retrieve(db,query,limit=4):
    q=tokens(query)
    if not q:return []
    ranked=[]
    for r in db.execute("SELECT * FROM observations"):
        t=tokens(r["text"]);overlap=len(q&t)
        if overlap:
            ranked.append((overlap/(len(q|t)),r))
    ranked.sort(key=lambda x:(-x[0],x[1]["id"]))
    return [dict(id=r["id"],origin_id=r["origin"],evidence_class=r["class"],subject_id=r["subject"],source=r["source"],excerpt=r["text"][:180],lexical_score=round(score,6),verified_entailment=False) for score,r in ranked[:limit]]
