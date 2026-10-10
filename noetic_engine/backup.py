"""Explicit snapshot and restore with subject binding and integrity checks."""
import hashlib,sqlite3
from pathlib import Path
from .engine import NoeticEngine
from .models import Configuration

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as stream:
        for part in iter(lambda:stream.read(1024*1024),b""):
            h.update(part)
    return h.hexdigest()

def backup(engine,destination):
    target=Path(destination)
    if target.exists():raise FileExistsError("refuse to overwrite a backup")
    if str(target)==":memory:":raise ValueError("persistent backup destination required")
    target.parent.mkdir(parents=True,exist_ok=True)
    with engine.store.tx():
        if not engine.store.verify():raise ValueError("source integrity failure")
        # A live transaction cannot be safely backed up using this connection.
    try:
        with sqlite3.connect(str(target)) as copy:
            engine.store.db.backup(copy)
        with NoeticEngine(str(target),engine.config) as snapshot:
            if not snapshot.store.verify():
                raise ValueError("snapshot integrity failed")
            if snapshot.status()["tick"]!=engine.status()["tick"]:
                raise ValueError("snapshot tick mismatch")
        return {"path":str(target),"sha256":sha256_file(target),
                "subject":engine.config.subject_id}
    except Exception:
        target.unlink(missing_ok=True)
        raise

def restore(backup_path,destination,expected_sha256,config=None):
    source=Path(backup_path); target=Path(destination)
    if target.exists():raise FileExistsError("restore requires an absent destination")
    if sha256_file(source)!=expected_sha256:
        raise ValueError("backup checksum mismatch")
    target.parent.mkdir(parents=True,exist_ok=True)
    try:
        with sqlite3.connect(str(source)) as old,sqlite3.connect(str(target)) as new:
            old.backup(new)
        with NoeticEngine(str(target),config or Configuration()) as recovered:
            if not recovered.store.verify():raise ValueError("restored ledger invalid")
            return {"path":str(target),"verified":True,
                    "subject":recovered.config.subject_id,
                    "tick":recovered.status()["tick"]}
    except Exception:
        target.unlink(missing_ok=True)
        raise
