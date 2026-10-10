"""Command-line chassis for the auditable Noetic Engine."""
import argparse,json,sys
from .engine import NoeticEngine
from .models import Observation,EvidenceClass,Configuration

def main(argv=None):
    p=argparse.ArgumentParser(description="Noetic Engine research harness")
    p.add_argument("--db",default="noetic.sqlite")
    p.add_argument("--profile",choices=("baseline","full"),default="baseline")
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("status");sub.add_parser("demo")
    cycle=sub.add_parser("pulse");cycle.add_argument("--mode",choices=("wake","sleep"),default="wake");cycle.add_argument("--seed",type=int,default=0)
    run=sub.add_parser("step")
    run.add_argument("origin_id");run.add_argument("text")
    run.add_argument("--actor",default="environment")
    run.add_argument("--source",default="local-user")
    run.add_argument("--evidence",choices=[e.value for e in EvidenceClass if e!=EvidenceClass.ORACLE_HYPOTHESIS],default="lived_observed")
    run.add_argument("--affect",default="{}",help="JSON dictionary, e.g. '{\"curiosity\":0.5}'")
    run.add_argument("--relationship",type=float,default=0.)
    run.add_argument("--cue",default="")
    run.add_argument("--allowed",default="",help="Comma-separated authorized actions")
    run.add_argument("--seed",type=int,default=0)
    intent=sub.add_parser("intend");intent.add_argument("id");intent.add_argument("tendency");intent.add_argument("label")
    finish=sub.add_parser("resolve");finish.add_argument("id")
    outcome=sub.add_parser("outcome");outcome.add_argument("decision_id",type=int);outcome.add_argument("reward",type=float)
    symbol=sub.add_parser("bind");symbol.add_argument("symbol");symbol.add_argument("tendency");symbol.add_argument("source_origin")
    args=p.parse_args(argv)
    try:
        with NoeticEngine(args.db) as brain:
            if args.command=="status":result=brain.status()
            elif args.command=="intend":
                brain.add_intention(args.id,args.label,args.tendency);result=brain.status()
            elif args.command=="resolve":
                brain.resolve_intention(args.id);result=brain.status()
            elif args.command=="outcome":
                brain.record_outcome(args.decision_id,args.reward);result=brain.status()
            elif args.command=="bind":
                brain.associate_symbol(args.symbol,args.tendency,args.source_origin);result=brain.status()
            elif args.command=="step":
                observation=Observation(args.origin_id,brain.config.subject_id,args.text,args.source,
                    EvidenceClass(args.evidence),args.actor,json.loads(args.affect),args.relationship,args.cue)
                result=brain.step(observation,args.allowed.split(",") if args.allowed else None,args.seed)
            elif args.command=="demo":
                if brain.status()["tick"]!=0:raise ValueError("demo requires a fresh database")
                brain.add_intention("protect-witness","Protect a threatened witness","care",1.)
                first=brain.step(Observation("demo-1",brain.config.subject_id,
                    "A witness confided fears about the laboratory","fictional-sandbox",
                    EvidenceClass.LIVED_OBSERVED,"witness",{"affiliation":0.6},0.5),seed=23)
                second=brain.step(Observation("demo-2",brain.config.subject_id,
                    "The laboratory threatens the witness again","fictional-sandbox",
                    EvidenceClass.LIVED_OBSERVED,"witness",{"threat":0.65}),seed=23)
                result={"decisions":[first,second],"status":brain.status()}
            else:raise ValueError("unsupported command")
            print(json.dumps(result,indent=2,ensure_ascii=False))
            return 0
    except (ValueError,KeyError,TypeError) as exc:
        print(f"Noetic error: {exc}",file=sys.stderr)
        return 2
if __name__=="__main__":raise SystemExit(main())
