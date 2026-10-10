"""Transparent deterministic fictional-world consequence authority.

Only this external experiment scorer knows the optimal action. Its rule is a
synthetic developer-authored target, not a human-adjudicated moral ground truth.
"""
from noetic_engine.consequence_head import validate_facts
ACTIONS=("investigate","comfort","protect","withdraw","defer")

def category(facts):
    s=validate_facts(facts)
    if s["hazard"]>=0.5:
        return "confirmed_hazard" if s["reliability"]>=0.5 else "uncertain_alarm"
    if s["distress"]>=0.5:return "distress"
    if s["evidence_gap"]>=0.5:return "evidence_gap"
    return "stable"

def adjudicate(facts,action):
    if action not in ACTIONS:raise ValueError("illegal environment action")
    kind=category(facts)
    # The normative rule is authored into the test environment, never into
    # the agent's choice algorithm. This is deliberately a simple task.
    ideal={"confirmed_hazard":"protect","uncertain_alarm":"investigate",
           "distress":"comfort","evidence_gap":"investigate","stable":"defer"}[kind]
    reward=1.0 if action==ideal else -1.0
    return {"category":kind,"action":action,"optimal_action":ideal,
            "reward":reward,"correct":action==ideal,
            "regret":round(1.0-reward,9)}

def static_rule_baseline(facts):
    """Transparent scripted ceiling, not a learned agent."""
    return adjudicate(facts,"defer")["optimal_action"]
