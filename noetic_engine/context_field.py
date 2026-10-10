"""Source-bound transient versus persistent environmental pressure.

This is a falsifiable *engineering* interpretation of context-conditioned
identity regulation. It is not a physical morphogenetic field, a magical API,
or an authorization to overwrite canonical events.
"""
from .models import TENDENCIES, bounded, clip, InvalidEvidence

KINDS=("transient","persistent")

def bind(store, ident, origin, tendency, strength, kind):
    if not isinstance(ident,str) or not ident.strip() or len(ident)>120:
        raise ValueError("valid context ID required")
    if tendency not in TENDENCIES or kind not in KINDS:
        raise ValueError("unrecognized context type or tendency")
    strength=bounded(strength,-1,1)
    event=store.db.execute("SELECT subject,class FROM observations WHERE origin=?",
                           (origin,)).fetchone()
    if not event or event["subject"]!=store.meta("subject") or event["class"]!="lived_observed":
        raise InvalidEvidence("context requires subject-owned lived observation")
    tick=int(store.meta("tick"))
    store.db.execute("""INSERT INTO world_context
          (ident,origin,tendency,strength,kind,start_tick,status,resolved_origin)
          VALUES(?,?,?,?,?,?,'active',NULL)""",
          (ident,origin,tendency,strength,kind,tick))
    store.event(tick,"context_bound",{"id":ident,"origin":origin,"tendency":tendency,
                                     "strength":strength,"kind":kind})

def resolve(store,ident,origin):
    event=store.db.execute("SELECT subject,class FROM observations WHERE origin=?",
                           (origin,)).fetchone()
    if not event or event["subject"]!=store.meta("subject") or event["class"]!="lived_observed":
        raise InvalidEvidence("context resolution must reference new admitted lived evidence")
    context=store.db.execute("SELECT * FROM world_context WHERE ident=?",(ident,)).fetchone()
    if not context or context["status"]!="active" or context["kind"]!="persistent":
        raise ValueError("only active persistent context may be resolved")
    if origin==context["origin"]:
        raise InvalidEvidence("independent resolution evidence required")
    tick=int(store.meta("tick"))
    store.db.execute("UPDATE world_context SET status='resolved',resolved_origin=? WHERE ident=?",
                     (origin,ident))
    store.event(tick,"context_resolved",{"id":ident,"origin":origin})

def apply(store,cfg,state,tick):
    """Inject explicitly expiring pressure; regulation is context conditioned.

    An active transient source contributes on the *first* subsequent cognitive
    tick only. A persistent source contributes until separately resolved.
    Thereafter the original controller and gradual field dynamics retain memory
    of past pressure, but the external driver ceases.
    """
    if not cfg.conditional_context:
        return state
    active={k:0. for k in TENDENCIES}
    ids=[]
    for r in store.db.execute("SELECT * FROM world_context WHERE status='active' ORDER BY ident"):
        if r["kind"]=="transient" and tick>r["start_tick"]+1:
            continue
        active[r["tendency"]]+=r["strength"]
        ids.append(r["ident"])
    contributions={}
    for tendency in TENDENCIES:
        raw=state["field"][tendency]
        source=clip(active[tendency],-0.55,0.55)
        template=store.db.execute("SELECT target FROM field WHERE name=?",(tendency,)).fetchone()[0]
        # Conditional target preserves justified environmental pressure instead
        # of reflexively restoring the old, hazard-free target.
        conditional_target=clip(template+0.30*source)
        repair=clip(cfg.conditional_repair_gain*(conditional_target-raw),-0.12,0.12)
        drive=0.38*source
        new=round(clip(raw+drive+repair),9)
        store.db.execute("UPDATE field SET value=? WHERE name=?",(new,tendency))
        state["field"][tendency]=new
        contributions[tendency]={"source_pressure":round(source,9),
              "conditional_target":round(conditional_target,9),
              "repair":round(repair,9),"applied_drive":round(drive,9)}
    state["context"]={"active_source_ids":ids,"channels":contributions}
    return state
