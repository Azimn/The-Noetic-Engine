"""Exploratory failure analysis on immutable MATRIX-005 raw evidence.

This post-hoc diagnostic does NOT tune or change the agent or evaluation;
it describes all completed official test episodes without filtering failures.
"""
import argparse,gzip,json,collections
from pathlib import Path

def read(path):
    with (gzip.open(path,"rt",encoding="utf-8") if str(path).endswith(".gz")
          else open(path,"r",encoding="utf-8")) as stream:
        return json.load(stream)

def action_category(a):
    return str(a).split(" ")[0].lower()

def analyze(report):
    diagnosis={}
    for world in report["environment_profiles"]:
        game=world["game"]
        training=[step for ep in world["behavior_transcripts"] for step in ep["steps"]]
        reward_positive=sum(step["reward"]>0 for step in training)
        source={"training_behavior_actions":len(training),
                "training_positive_reward_steps":reward_positive,
                "training_total_world_reward":round(sum(x["reward"] for x in training),9),
                "official_train_seeds":world["train_seeds"],
                "official_test_seeds":world["test_seeds"]}
        profiles={}
        pmap={x["profile"]:x for x in world["profiles"]}
        for row in world["profiles"]:
            all_episodes=row["test_episodes"]
            commands=[act["action"] for ep in all_episodes for act in ep["actions"]]
            kinds=collections.Counter(action_category(a) for a in commands)
            repeats=sum(commands[i]==commands[i-1] for ep in all_episodes
                for i in [] )  # Repetitions are counted per episode below.
            repeats=sum(sum(ep["actions"][i]["action"]==ep["actions"][i-1]["action"]
                        for i in range(1,len(ep["actions"]))) for ep in all_episodes)
            margins=[]
            for ep in all_episodes:
                for step in ep["actions"]:
                    values=sorted(step["external_policy"]["scores"].values(),reverse=True)
                    if len(values)>1:margins.append(round(values[0]-values[1],9))
            profiles[row["profile"]]={
                "test_episodes":len(all_episodes),"world_score_mean":row["mean_world_score"],
                "successes":row["success_count"],
                "test_commands":len(commands),
                "command_family_counts":dict(sorted(kinds.items())),
                "exact_consecutive_repeats":repeats,
                "mean_value_score_margin":round(sum(margins)/len(margins),9) if margins else None,
                "per_seed_results":[{"seed":ep["seed"],"score":ep["score"],
                                     "success":ep["success"],"steps":ep["steps"],
                                     "command_sequence":[s["action"] for s in ep["actions"]]}
                                    for ep in all_episodes]}
        full=pmap["full"]["test_episodes"]
        compare={}
        for name in ("no_neural","signed_only","frozen","heuristic","random"):
            other=pmap[name]["test_episodes"]
            if [x["seed"] for x in full]!=[x["seed"] for x in other]:
                raise AssertionError("non-paired official test seeds")
            n=sum(1 for a,b in zip(full,other)
                  if [s["action"] for s in a["actions"]]==
                     [s["action"] for s in b["actions"]])
            compare[name]={"exact_matching_action_trajectories":n,
                           "paired_episodes":len(full),
                           "score_differences":[round(a["score"]-b["score"],9)
                                                for a,b in zip(full,other)]}
        diagnosis[game]={"source":source,"profiles":profiles,
                         "full_vs_controls":compare}
    return {"analysis_class":"posthoc_descriptive_immutable_M005",
            "primary_protocol":report["protocol"],
            "external_benchmark_version":report["third_party_version"],
            "diagnostic":diagnosis,
            "limitation":"Describes originally archived 4 test seeds/game. Repeated action types and score margins do not prove or disprove long-horizon character identity."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--raw",required=True)
    p.add_argument("--output",required=True)
    args=p.parse_args()
    result=analyze(read(args.raw))
    dest=Path(args.output);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    compact={k:{"train_positive_steps":v["source"]["training_positive_reward_steps"],
                "full_control_trajectory":v["full_vs_controls"],
                "profile_actions":{p:d["command_family_counts"] for p,d in v["profiles"].items()}}
             for k,v in result["diagnostic"].items()}
    print(json.dumps(compact,sort_keys=True))

if __name__=="__main__":main()
