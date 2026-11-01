#!/usr/bin/env python3
"""Compare the Python reference and the node run of assets/ssc-live.js BY VALUE over the whole ladder
(normal, skip DE, leaked field, both), then prove the comparison can fail: a planted 0.1% fault on one
number must be caught. Also requires the engine selfTest to pass on the shipped data and to FAIL with
its planted fault.

Usage: python3 -I materials/compare-ladder.py   (exit 0 = agree, fault caught, selfTest behaves)
Writes materials/canon-python.json and materials/canon-node.json.
"""
import copy
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REL = 1e-9


def flatten(x, path=""):
    if isinstance(x, dict):
        for k in sorted(x):
            yield from flatten(x[k], path + "/" + k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from flatten(v, path + "/" + str(i))
    else:
        yield path, x


def compare(a, b):
    fa, fb = dict(flatten(a)), dict(flatten(b))
    bad = []
    for k in sorted(set(fa) | set(fb)):
        if k not in fa or k not in fb:
            bad.append(f"{k}: missing on one side")
            continue
        x, y = fa[k], fb[k]
        if x is None or y is None or isinstance(x, (bool, str)) or isinstance(y, (bool, str)):
            if x != y:
                bad.append(f"{k}: {x!r} vs {y!r}")
        elif abs(x - y) > REL * max(1.0, abs(x), abs(y)):
            bad.append(f"{k}: {x!r} vs {y!r}")
    return bad, len(fa)


def main():
    pyo = subprocess.check_output([sys.executable, "-I", os.path.join(HERE, "ssc_reference.py")])
    ndo = subprocess.check_output(["node", os.path.join(HERE, "run_ladder_node.js")])
    py, nd = json.loads(pyo), json.loads(ndo)
    st, stp = nd.pop("selfTest"), nd.pop("selfTestPlanted")
    with open(os.path.join(HERE, "canon-python.json"), "w") as f:
        json.dump(py, f, indent=1)
    with open(os.path.join(HERE, "canon-node.json"), "w") as f:
        json.dump(nd, f, indent=1)
    bad, n = compare(py, nd)
    print(f"values compared: {n}")
    print("python vs node:", "AGREE" if not bad else "DIFFER")
    for line in bad[:20]:
        print("  ", line)
    planted = copy.deepcopy(nd)
    planted["normal"]["ml"]["lift"] *= 1.001
    caught = bool(compare(py, planted)[0])
    print("planted 0.1% fault on normal/ml/lift:", "caught" if caught else "NOT CAUGHT")
    print("engine selfTest:", json.dumps(st))
    print("engine selfTest with planted fault:", json.dumps(stp))
    ok = not bad and caught and st["pass"] and not stp["pass"]
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
