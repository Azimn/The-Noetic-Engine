"""Transactional SQLite state and audit log."""
import sqlite3, json, hashlib
from contextlib import contextmanager
from pathlib import Path
def serial(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest(x): return hashlib.sha256(serial(x).encode()).hexdigest()
class Store:
    def __init__(self,path,subject):
        if path!=":memory:": Path(path).parent.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(path,isolation_level=None)
        self.db.row_factory=sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY,v TEXT);
        CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,tick INT,kind TEXT,payload TEXT,hash TEXT);
        CREATE TABLE IF NOT EXISTS observations(id INTEGER PRIMARY KEY,tick INT,origin TEXT UNIQUE,subject TEXT,actor TEXT,source TEXT,class TEXT,text TEXT,hash TEXT);
        CREATE TABLE IF NOT EXISTS intentions(id TEXT PRIMARY KEY,label TEXT,tendency TEXT,strength REAL,tension REAL,status TEXT);
        CREATE TABLE IF NOT EXISTS relations(actor TEXT PRIMARY KEY,trust REAL,confidence REAL,viewpoint TEXT,source_id INT);
        CREATE TABLE IF NOT EXISTS affect(name TEXT PRIMARY KEY,value REAL);
        CREATE TABLE IF NOT EXISTS field(name TEXT PRIMARY KEY,value REAL,target REAL);
        CREATE TABLE IF NOT EXISTS symbols(symbol TEXT PRIMARY KEY,tendency TEXT,strength REAL,source_id INT);
        CREATE TABLE IF NOT EXISTS oracle(id INTEGER PRIMARY KEY,tick INT,text TEXT,source_ids TEXT,seed INT,status TEXT);
        CREATE TABLE IF NOT EXISTS decisions(id INTEGER PRIMARY KEY,tick INT,action TEXT,audit TEXT,hash TEXT);
        """)
        with self.tx():
            owner=self.meta("subject")
            if owner not in (None,subject): raise ValueError("subject mismatch")
            if self.meta("schema") not in (None,"1"): raise ValueError("unsupported schema")
            self.put("subject",subject);self.put("schema","1")
            if self.meta("tick") is None:
                self.put("tick","0")
                for k in ("curiosity","affiliation","threat","fatigue"):
                    self.db.execute("INSERT INTO affect VALUES(?,0)",(k,))
                for k in ("inquiry","care","caution"):
                    self.db.execute("INSERT INTO field VALUES(?,0,0)",(k,))
    @contextmanager
    def tx(self):
        self.db.execute("BEGIN IMMEDIATE")
        try: yield
        except Exception: self.db.execute("ROLLBACK");raise
        else: self.db.execute("COMMIT")
    def meta(self,k):
        r=self.db.execute("SELECT v FROM meta WHERE k=?",(k,)).fetchone()
        return r[0] if r else None
    def put(self,k,v):
        self.db.execute("INSERT INTO meta VALUES(?,?) ON CONFLICT(k) DO UPDATE SET v=excluded.v",(k,str(v)))
    def event(self,tick,kind,data):
        self.db.execute("INSERT INTO events(tick,kind,payload,hash) VALUES(?,?,?,?)",(tick,kind,serial(data),digest(data)))
    def mapping(self,table,k,v):
        return {r[k]:r[v] for r in self.db.execute(f"SELECT {k},{v} FROM {table}")}
    def verify(self):
        return (all(digest(json.loads(r["payload"]))==r["hash"] for r in self.db.execute("SELECT payload,hash FROM events")) and
                all(digest(json.loads(r["audit"]))==r["hash"] for r in self.db.execute("SELECT audit,hash FROM decisions")))
    def close(self):self.db.close()
