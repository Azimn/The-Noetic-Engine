"""MATRIX-005: real TextWorldExpress worlds, common offline training log, test-fold play.

External environment owns commands and rewards; no gold paths and no hidden
object tree. The Noetic cognitive engine supplies a bounded field for a distinct,
audited command-selection port. This does not test an end-to-end language model.
"""
from __future__ import annotations
import argparse,hashlib,importlib.metadata,json,random,tempfile,time
from pathlib import Path
from statistics import mean
from noetic_engine import NoeticEngine,Configuration,Observation
from noetic_engine.models import EvidenceClass
from noetic_engine.backup import backup,restore,sha256_file
from .external_command_port import ExternalCommandPort,install as install_port

PROTOCOL="matrix-005-textworldexpress-v01"
FAMILIES={
    "coin":"numLocations=4,numDistractorItems=0,includeDoors=0,limitInventorySize=0",
    "twc":"numLocations=1,numItemsToPutAway=2,includeDoors=0,limitInventorySize=0",
}
PROFILES=("full","no_neural","signed_only","frozen","heuristic","random")
TRAIN_N=3
TEST_N=4
STEP_LIMIT=18
SUBJECT="noetic_external_sandbox"

def env_new(game,params):
    from textworld_express import TextWorldExpressEnv
    env=TextWorldExpressEnv(envStepLimit=STEP_LIMIT)
    env.load(gameName=game,gameParams=params)
    return env

def named_seeds(env,fold,count):
    options={"train":env.getValidSeedsTrain,
             "dev":env.getValidSeedsDev,
             "test":env.getValidSeedsTest}[fold]()
    seeds=sorted(int(x) for x in options)
    if len(seeds)<count:raise RuntimeError("insufficient official "+fold+" seeds")
    if len(seeds)!=len(set(seeds)):raise RuntimeError("duplicate external fold seeds")
    return seeds[:count]

def fresh_observation(brain,origin,text):
    obs=Observation(origin_id=origin,subject_id=SUBJECT,
        text=text[:16000] if text else "(empty world description)",
        source="TextWorldExpress-1.1.0",
        evidence_class=EvidenceClass.LIVED_OBSERVED,
        actor_id="official_simulator")
    return brain.step(obs,allowed=["defer"],seed=3)

def config_profile(mode):
    return Configuration(subject_id=SUBJECT,policy_version=PROTOCOL,
       oracle=False,egregore=False,self_model=False,
       consequence_head=False,conditional_context=False,
       neural_field=(mode=="full"),neural_units=24,neural_seed=17,
       developmental=(mode in ("full","no_neural")),
       intentions=True,relationships=False,cues=False)

def make_log(game,params,seeds):
    env=env_new(game,params)
    try:
        logs=[]
        for seed in seeds:
            obs,info=env.reset(seed=seed,gameFold="train",generateGoldPath=False)
            task=info["taskDescription"]
            rng=random.Random("behavior:"+game+":"+str(seed))
            entries=[]
            for step in range(STEP_LIMIT):
                valid=sorted(info["validActions"])
                if not valid:raise RuntimeError("no valid actions from external game")
                action=rng.choice(valid)
                observation_after,reward,done,next_info=env.step(action)
                if not isinstance(reward,(float,int)) or not -1<=reward<=1:
                    raise RuntimeError("unbounded official game reward")
                entries.append({"step":step,"observation":obs,"task":task,
                                "valid_actions":valid,"command":action,
                                "reward":round(float(reward),9),
                                "next_observation":observation_after,
                                "world_done":bool(done),
                                "score":round(float(next_info["score"]),9)})
                obs,info=observation_after,next_info
                if done:break
            logs.append({"game":game,"fold":"train","seed":seed,
                         "steps":entries,"finished":bool(info.get("tasksuccess",False)),
                         "final_score":round(float(info["score"]),9)})
        return logs
    finally:env.close()

def put_source(brain,game,fold,seed,step,phase,text,task=""):
    origin=":".join([game,fold,str(seed),str(step),phase])
    decision=fresh_observation(brain,origin,(task+"\n"+text).strip())
    return origin,decision

def offline_train(brain,port,game,logs):
    all_cases=[]
    for record in logs:
        port.begin_episode()
        seed=record["seed"]
        episode=game+":train:"+str(seed)
        for s in record["steps"]:
            origin,internal=put_source(brain,game,"train",seed,s["step"],
                                       "sense",s["observation"],s["task"])
            chosen,id,action_trace=port.choose(
                episode,s["step"],origin,s["valid_actions"],
                s["observation"],s["task"],internal["state"]["field"],
                forced_command=s["command"],training=True)
            if chosen!=s["command"]:
                raise AssertionError("training action exposure changed")
            receipt,_=put_source(brain,game,"train",seed,s["step"],
                                 "consequence",s["next_observation"])
            port.feedback(id,receipt,s["reward"],
                          learn=port.mode not in ("frozen","heuristic","random"))
            all_cases.append({"episode":episode,"step":s["step"],
                              "command":chosen,"reward":s["reward"],
                              "observation_origin":origin,
                              "reward_origin":receipt,
                              "external_decision_id":id,
                              "source_game_score":s["score"]})
    return all_cases

def play_test(brain,port,game,params,seed):
    env=env_new(game,params)
    port.begin_episode()
    history=[]
    try:
        obs,info=env.reset(seed=seed,gameFold="test",generateGoldPath=False)
        task=info["taskDescription"]
        for step in range(STEP_LIMIT):
            valid=sorted(info["validActions"])
            if not valid:raise RuntimeError("no admissible actions in external world")
            origin,internal=put_source(brain,game,"test",seed,step,
                                       "sense",obs,task)
            action,choice_id,trace=port.choose(
                game+":test:"+str(seed),step,origin,valid,obs,task,
                internal["state"]["field"])
            if action not in valid:raise AssertionError("invalid world command")
            after,reward,done,nextinfo=env.step(action)
            receipt,_=put_source(brain,game,"test",seed,step,"consequence",after)
            # Evaluation outcomes are logged but not used to update weights.
            port.feedback(choice_id,receipt,float(reward),learn=False)
            history.append({"step":step,"origin":origin,"reward_origin":receipt,
                "observation":obs,"admissible_actions":valid,"action":action,
                "external_policy":trace,"reward":round(float(reward),9),
                "score":round(float(nextinfo["score"]),9),
                "tasksuccess":bool(nextinfo["tasksuccess"]),
                "taskfailure":bool(nextinfo["taskfailure"]),
                "world_done":bool(done),"next_observation":after})
            obs,info=after,nextinfo
            if done:break
        if not port.verify() or not brain.status()["verified_audit_hashes"]:
            raise AssertionError("Noetic/world action evidence integrity failure")
        return {"game":game,"fold":"test","seed":seed,
                "success":bool(info["tasksuccess"]),
                "taskfailure":bool(info["taskfailure"]),
                "score":round(float(info["score"]),9),
                "steps":len(history),
                "actions":history,
                "no_gold_path":True,
                "memory_count":brain.status()["memories"],
                "decision_field_causally_scored":port.mode in ("full","no_neural")}
    finally:env.close()

def run_game(game,params):
    env=env_new(game,params)
    try:
        train_seeds=named_seeds(env,"train",TRAIN_N)
        test_seeds=named_seeds(env,"test",TEST_N)
    finally:env.close()
    logged=make_log(game,params,train_seeds)
    results=[]
    with tempfile.TemporaryDirectory() as tmp:
        for mode in PROFILES:
            cfg=config_profile(mode)
            training_path=str(Path(tmp)/(game+"-"+mode+"-train.sqlite"))
            with NoeticEngine(training_path,cfg) as brain:
                install_port(brain.store)
                port=ExternalCommandPort(brain,mode=mode,seed=73)
                trained=offline_train(brain,port,game,logged)
                snapshot=backup(brain,str(Path(tmp)/(game+"-"+mode+"-checkpoint.sqlite")))
                if not port.verify():raise AssertionError("training command audit invalid")
            evaluations=[]
            for seed in test_seeds:
                dest=str(Path(tmp)/(game+"-"+mode+"-test-"+str(seed)+".sqlite"))
                restored=restore(snapshot["path"],dest,snapshot["sha256"],cfg)
                if restored["subject"]!=SUBJECT:raise AssertionError("foreign brain checkpoint")
                with NoeticEngine(dest,cfg) as brain:
                    # The custom port schema is persistent in restored checkpoint.
                    port=ExternalCommandPort(brain,mode=mode,seed=seed*11+71)
                    evaluations.append(play_test(brain,port,game,params,seed))
            results.append({"profile":mode,"game":game,
                 "train_seeds":train_seeds,"test_seeds":test_seeds,
                 "training_transcript":trained,"test_episodes":evaluations,
                 "checkpoint_sha256":snapshot["sha256"],
                 "success_count":sum(x["success"] for x in evaluations),
                 "mean_world_score":round(mean(x["score"] for x in evaluations),9),
                 "mean_steps":round(mean(x["steps"] for x in evaluations),9)})
    return {"game":game,"params":params,"train_seeds":train_seeds,
            "test_seeds":test_seeds,"behavior_transcripts":logged,
            "profiles":results}

def execute():
    package=importlib.metadata.version("textworld-express")
    if package!="1.1.0":raise RuntimeError("external benchmark version mismatch")
    worlds=[run_game(name,params) for name,params in FAMILIES.items()]
    summary={}
    for result in worlds:
        summary[result["game"]]={p["profile"]:{
            "successes":p["success_count"],"episodes":len(p["test_episodes"]),
            "mean_world_score":p["mean_world_score"],
            "mean_steps":p["mean_steps"]}
            for p in result["profiles"]}
    return {"protocol":PROTOCOL,"third_party_engine":"TextWorldExpress",
            "third_party_version":package,
            "game_folds":"official train and test; first N official valid seeds by ascending ID",
            "gold_paths_requested":False,"privileged_world_state_read":False,
            "full_noetic_port":"experimental generic command reranker, NOT core PretoriusBrainPort",
            "structured_signals_supplied":False,
            "model_renderer_used":False,"environment_profiles":worlds,
            "summary":summary,
            "limitations":"No LLM perception, no formal language comprehension, train/test episode counts small, external goal tasks do not measure character identity, randomly collected common training traces may yield sparse reward."}

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    args=parser.parse_args(argv)
    report=execute()
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"protocol":PROTOCOL,"engine":report["third_party_engine"],
          "version":report["third_party_version"],"summary":report["summary"],
          "cases_path":str(out)},sort_keys=True))
    return 0

if __name__=="__main__":raise SystemExit(main())
