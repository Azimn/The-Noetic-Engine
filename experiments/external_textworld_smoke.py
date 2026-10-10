"""External benchmark handshake: no gold paths or privileged simulator fields."""
import json
import importlib.metadata
from textworld_express import TextWorldExpressEnv

def main():
    result={"package":importlib.metadata.version("textworld-express"),"probes":[]}
    for game,params in [
        ("coin","numLocations=4,numDistractorItems=0,includeDoors=0,limitInventorySize=0"),
        ("twc","numLocations=1,numItemsToPutAway=2,includeDoors=0,limitInventorySize=0"),
    ]:
        env=TextWorldExpressEnv(envStepLimit=24)
        try:
            env.load(gameName=game,gameParams=params)
            obs,info=env.reset(seed=0,gameFold="train",generateGoldPath=False)
            actions=sorted(info["validActions"])
            if not actions:raise RuntimeError("no external valid actions")
            action=actions[0]
            next_obs,reward,done,next_info=env.step(action)
            result["probes"].append({
                "game":game,"params":params,
                "observation_type":type(obs).__name__,
                "sample_observation":obs[:160],
                "valid_action_count":len(actions),
                "sample_actions":actions[:7],
                "selected_action":action,
                "step_reward":reward,
                "next_valid_count":len(next_info["validActions"]),
                "done":done,"score":next_info.get("score"),
                "tasksuccess":next_info.get("tasksuccess"),
                "taskfailure":next_info.get("taskfailure"),
                "python_keys":sorted(k for k in info if k not in ("goldPath",)),
            })
        finally:env.close()
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
