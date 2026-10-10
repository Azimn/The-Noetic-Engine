"""Noetic v0.2 additive schema.

The v0.1 ledger stays readable. Extension state is subject-bound and versioned,
and creates NO new identity authority. This is a migration-safe additive profile.
"""
def install(store):
    store.db.executescript("""
    CREATE TABLE IF NOT EXISTS social_claims(
      id INTEGER PRIMARY KEY, origin TEXT NOT NULL,
      attributed_actor TEXT NOT NULL, believed_subject TEXT NOT NULL,
      predicate TEXT NOT NULL, valence REAL NOT NULL, confidence REAL NOT NULL,
      epistemic TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'unreviewed',
      FOREIGN KEY(origin) REFERENCES observations(origin));
    CREATE TABLE IF NOT EXISTS social_reviews(
      id INTEGER PRIMARY KEY, claim_id INTEGER NOT NULL, reviewer TEXT NOT NULL,
      disposition TEXT NOT NULL, tick INTEGER NOT NULL,
      FOREIGN KEY(claim_id) REFERENCES social_claims(id));
    CREATE TRIGGER IF NOT EXISTS social_reviews_immutable
      BEFORE UPDATE ON social_reviews
      BEGIN SELECT RAISE(ABORT,'immutable review'); END;
    CREATE TABLE IF NOT EXISTS oracle_reviews(
      id INTEGER PRIMARY KEY, oracle_id INTEGER NOT NULL, reviewer TEXT NOT NULL,
      disposition TEXT NOT NULL, justification TEXT NOT NULL, tick INTEGER NOT NULL,
      FOREIGN KEY(oracle_id) REFERENCES oracle(id));
    CREATE TRIGGER IF NOT EXISTS oracle_reviews_immutable
      BEFORE UPDATE ON oracle_reviews
      BEGIN SELECT RAISE(ABORT,'immutable review'); END;
    CREATE TABLE IF NOT EXISTS developmental_state(
      tendency TEXT PRIMARY KEY, target REAL NOT NULL, eligibility REAL NOT NULL,
      metaplasticity REAL NOT NULL, update_tick INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS self_hypotheses(
      id INTEGER PRIMARY KEY, origin TEXT NOT NULL, predicate TEXT NOT NULL,
      tendency TEXT NOT NULL, valence REAL NOT NULL, confidence REAL NOT NULL,
      status TEXT NOT NULL DEFAULT 'provisional',
      FOREIGN KEY(origin) REFERENCES observations(origin));
    CREATE TABLE IF NOT EXISTS self_reviews(
      id INTEGER PRIMARY KEY, hypothesis_id INTEGER NOT NULL,
      reviewer TEXT NOT NULL, disposition TEXT NOT NULL, tick INTEGER NOT NULL,
      FOREIGN KEY(hypothesis_id) REFERENCES self_hypotheses(id));
    CREATE TRIGGER IF NOT EXISTS self_reviews_immutable BEFORE UPDATE ON self_reviews
      BEGIN SELECT RAISE(ABORT,'immutable self review'); END;
    CREATE TABLE IF NOT EXISTS field_snapshots(
      id INTEGER PRIMARY KEY, tick INTEGER NOT NULL, values_json TEXT NOT NULL,
      template_json TEXT NOT NULL, digest TEXT NOT NULL);
    CREATE TRIGGER IF NOT EXISTS field_snapshots_immutable
      BEFORE UPDATE ON field_snapshots
      BEGIN SELECT RAISE(ABORT,'immutable field snapshot'); END;
    CREATE TRIGGER IF NOT EXISTS field_snapshots_no_delete
      BEFORE DELETE ON field_snapshots
      BEGIN SELECT RAISE(ABORT,'immutable field snapshot'); END;
    """)
    with store.tx():
        version=store.meta("noetic_extension_schema")
        if version not in (None,"1","2"):
            raise ValueError("incompatible Noetic extension schema")
        store.put("noetic_extension_schema","2")
        for name in ("inquiry","care","caution"):
            store.db.execute("""INSERT OR IGNORE INTO developmental_state
              VALUES(?,0,0,0,0)""",(name,))
