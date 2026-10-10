"""Research-only command port for external games, with source-linked audit.

IMPORTANT: This is not NoeticBrainAdapter or a production world adapter.
It translates genuine external admissible commands into a separate audited
policy, with the Noetic field contributing a bounded causal bias. The normal
five-action character policy is not falsely represented as selecting commands.
"""
import hashlib,json,math,random,re
from noetic_engine.store import serial,digest
from noetic_engine.models import clip

FAMILIES=("move","take","put","open","look","inventory","other")
ACTIONS_LIMIT=128
STOP={"the","a","an","in","on","at","to","and","from","is","are","you",
      "your","of","it","with","for","there","also","this","that","be"}
FIELD_AXIS={"move":"inquiry","take":"inquiry","put":"care",
            "open":"caution","look":"inquiry","inventory":"inquiry",
            "other":"caution"}

def tokens(s):
    return set(x for x in re.findall(r"[a-z0-9]+",s.lower())
               if len(x)>2 and x not in STOP)

def family(command):
    first=command.split()[0].lower()
    return first if first in FAMILIES else "other"

def action_features(command,observation,visit_counts,task):
    fam=family(command)
    ct=tokens(command)
    ot=tokens(observation)
    tt=tokens(task)
    return {"bias":1.0,"verb:"+fam:1.0,
            "observation_overlap":round(len(ct & ot)/max(len(ct),1),9),
            "task_overlap":round(len(ct & tt)/max(len(ct),1),9),
            "repetition":round(-min(visit_counts.get(command,0),5)/5,9),
            "specificity":1.0 if len(ct)>1 else 0.0}

def install(store):
    store.db.executescript("""
    CREATE TABLE IF NOT EXISTS external_command_weights(
       feature TEXT PRIMARY KEY, weight REAL NOT NULL);
    CREATE TABLE IF NOT EXISTS external_command_choices(
       id INTEGER PRIMARY KEY, episode TEXT NOT NULL, step INTEGER NOT NULL,
       origin TEXT NOT NULL, command TEXT NOT NULL, candidates_json TEXT NOT NULL,
       features_json TEXT NOT NULL, score_json TEXT NOT NULL, audit_sha TEXT NOT NULL,
       FOREIGN KEY(origin) REFERENCES observations(origin));
    CREATE TABLE IF NOT EXISTS external_command_feedback(
       choice_id INTEGER PRIMARY KEY, reward_origin TEXT NOT NULL, reward REAL NOT NULL,
       learning_json TEXT NOT NULL, audit_sha TEXT NOT NULL,
       FOREIGN KEY(choice_id) REFERENCES external_command_choices(id),
       FOREIGN KEY(reward_origin) REFERENCES observations(origin));
    CREATE TRIGGER IF NOT EXISTS external_choices_immutable BEFORE UPDATE ON external_command_choices
      BEGIN SELECT RAISE(ABORT,'immutable external action'); END;
    CREATE TRIGGER IF NOT EXISTS external_feedback_immutable BEFORE UPDATE ON external_command_feedback
      BEGIN SELECT RAISE(ABORT,'immutable external feedback'); END;
    """)

def feature_score(weights,features):
    return sum(weights.get(key,0.0)*x for key,x in features.items())

def simple_lexical_rule(valid,observation,visit_counts,task):
    # Explicit handcrafted baseline, not a learned model.
    preferences={"take":0.9,"put":1.0,"open":0.55,"move":0.4,
                 "look":0.03,"inventory":-0.1,"other":0.}
    scores={}
    for a in valid:
        f=action_features(a,observation,visit_counts,task)
        bonus=0.5 if ("coin" in a.lower() and "coin" in observation.lower()) else 0.0
        scores[a]=round(preferences[family(a)]+0.16*f["observation_overlap"]
                         +0.18*f["task_overlap"]+0.16*f["repetition"]+bonus,9)
    return sorted(valid,key=lambda a:(-scores[a],a))[0],scores

class ExternalCommandPort:
    def __init__(self,brain,mode="full",field_gain=0.25,lr=0.20,seed=0):
        self.brain=brain
        self.mode=mode
        self.field_gain=field_gain
        self.lr=lr
        self.rng=random.Random(seed)
        self.visit_counts={}

    def begin_episode(self):
        self.visit_counts={}

    def _validate(self,valid,command=None):
        if not isinstance(valid,(list,tuple)) or not valid or len(valid)>ACTIONS_LIMIT:
            raise ValueError("external valid-action list missing or too large")
        if any(not isinstance(x,str) or not x or len(x)>240 for x in valid):
            raise ValueError("invalid world command")
        if len(set(valid))!=len(valid):raise ValueError("duplicate world action")
        if command is not None and command not in valid:
            raise ValueError("illegal external command")

    def choose(self,episode,step,origin,valid,observation,task,field,
               forced_command=None,training=False):
        self._validate(valid,forced_command)
        source=self.brain.store.db.execute(
            "SELECT subject,class FROM observations WHERE origin=?",(origin,)).fetchone()
        if not source or source["subject"]!=self.brain.config.subject_id or source["class"]!="lived_observed":
            raise ValueError("choice requires the subject's lived input origin")
        db=self.brain.store
        weights=db.mapping("external_command_weights","feature","weight")
        scores={}
        by_features={}
        for a in valid:
            f=action_features(a,observation,self.visit_counts,task)
            by_features[a]=f
            learned=feature_score(weights,f)
            axis=FIELD_AXIS[family(a)]
            field_contrib=(self.field_gain*field.get(axis,0.0)
                           if self.mode in ("full","no_neural") else 0)
            scores[a]=round(learned+field_contrib,9)
        if forced_command is not None:
            chosen=forced_command
        elif self.mode=="random":
            chosen=self.rng.choice(sorted(valid))
        elif self.mode=="heuristic":
            chosen,_=simple_lexical_rule(valid,observation,self.visit_counts,task)
        else:
            chosen=sorted(valid,key=lambda a:(-scores[a],a))[0]
        trace={"episode":episode,"step":step,"origin":origin,
               "selected":chosen,"eligible_actions":sorted(valid),
               "scores":scores,"features":by_features[chosen],
               "mode":self.mode,"field_gain":self.field_gain,
               "forced_training":forced_command is not None}
        with db.tx():
            cur=db.db.execute("""INSERT INTO external_command_choices
             (episode,step,origin,command,candidates_json,features_json,score_json,audit_sha)
             VALUES(?,?,?,?,?,?,?,?)""",(episode,step,origin,chosen,
                 serial(sorted(valid)),serial(by_features[chosen]),serial(scores),digest(trace)))
            db.event(int(db.meta("tick")),"external_command",
                     {"choice_id":cur.lastrowid,**trace})
        self.visit_counts[chosen]=self.visit_counts.get(chosen,0)+1
        return chosen,cur.lastrowid,trace

    def feedback(self,choice_id,origin,reward,learn=False):
        if type(reward) not in (float,int) or not math.isfinite(reward) or not -1.0<=reward<=1.0:
            raise ValueError("external reward must be finite, [-1,1]")
        db=self.brain.store
        chosen=db.db.execute("SELECT * FROM external_command_choices WHERE id=?",
                             (choice_id,)).fetchone()
        evidence=db.db.execute("SELECT * FROM observations WHERE origin=?",
                               (origin,)).fetchone()
        if not chosen or not evidence or evidence["subject"]!=self.brain.config.subject_id or evidence["class"]!="lived_observed":
            raise ValueError("outcome must refer to admitted, subject-owned world observation")
        if origin==chosen["origin"]:raise ValueError("distinct world receipt required")
        if db.db.execute("SELECT 1 FROM external_command_feedback WHERE choice_id=?",
                         (choice_id,)).fetchone():
            raise ValueError("duplicate external feedback")
        if learn and self.mode in ("random","heuristic","frozen"):
            raise ValueError("control may not silently learn")
        f=json.loads(chosen["features_json"])
        prior=db.mapping("external_command_weights","feature","weight")
        prediction=feature_score(prior,f)
        change={}
        with db.tx():
            if learn and self.mode not in ("random","heuristic","frozen"):
                error=reward-prediction
                norm=sum(abs(v) for v in f.values())
                for k,value in f.items():
                    old=prior.get(k,0.0)
                    new=round(clip(old+self.lr*error*value/max(norm,1),-2,2),9)
                    db.db.execute("""INSERT INTO external_command_weights(feature,weight)
                        VALUES(?,?) ON CONFLICT(feature)
                        DO UPDATE SET weight=excluded.weight""",(k,new))
                    change[k]=new-old
            trace={"choice_id":choice_id,"origin":origin,"reward":reward,
                   "learn":bool(learn),"prediction":round(prediction,9),
                   "changes":change,"algorithm":"shared-verb-feature-signed-value-v01"}
            db.db.execute("""INSERT INTO external_command_feedback
              (choice_id,reward_origin,reward,learning_json,audit_sha)
              VALUES(?,?,?,?,?)""",
              (choice_id,origin,reward,serial(trace),digest(trace)))
            db.event(int(db.meta("tick")),"external_feedback",trace)
        return trace

    def verify(self):
        db=self.brain.store.db
        for row in db.execute("SELECT * FROM external_command_choices"):
            events=db.execute("SELECT payload FROM events WHERE kind='external_command'").fetchall()
            matched=[json.loads(e["payload"]) for e in events if
                     json.loads(e["payload"]).get("choice_id")==row["id"]]
            if len(matched)!=1 or digest({k:v for k,v in matched[0].items() if k!="choice_id"})!=row["audit_sha"]:
                return False
        return all(digest(json.loads(r["learning_json"]))==r["audit_sha"]
                   for r in db.execute("SELECT * FROM external_command_feedback"))
