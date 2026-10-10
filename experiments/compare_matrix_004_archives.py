"""Compare deterministic experiment content while excluding nondeterministic timing.

A completed experiment's original raw file is never modified. Timing stays
recorded for resource analysis but is NOT part of a byte-identical replay claim.
"""
import argparse,gzip,json

TIME_FIELDS={"elapsed_cpu_scope_seconds","mean_elapsed_seconds"}

def stable(value):
    if isinstance(value,dict):
        return {k:stable(v) for k,v in value.items() if k not in TIME_FIELDS}
    if isinstance(value,list):
        return [stable(v) for v in value]
    return value

def load(path):
    with (gzip.open(path,"rt") if path.endswith(".gz") else open(path,"rt")) as stream:
        return json.load(stream)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("archived")
    parser.add_argument("rerun")
    args=parser.parse_args()
    a,b=stable(load(args.archived)),stable(load(args.rerun))
    if a!=b:
        raise SystemExit("Deterministic experiment evidence differs from archived result")
    print("Deterministic per-case evidence matches original; elapsed times retained separately.")

if __name__=="__main__":main()
