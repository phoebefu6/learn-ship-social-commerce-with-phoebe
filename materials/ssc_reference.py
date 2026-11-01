#!/usr/bin/env python3
"""Independent pure-Python reference for assets/ssc-live.js (no numpy, no pandas).

Reads materials/ssc-data.json (the same payload as assets/ssc-data.js) and prints the canon for the
whole ladder as JSON: normal, skip the DE layer (anti-lever), the leaked field (break button), both.
Same definitions, same seed-free deterministic optimiser (weights from zero, the same learning rate,
steps and L2, the same summation order), so values agree with node to floating-point noise.

Usage: python3 -I materials/ssc_reference.py > canon.json
"""
import json
import math
import os
import re
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))


def js_round(x):
    return math.floor(x + 0.5)


class Data:
    def __init__(self, D):
        self.D = D
        dd, self.day = 0, []
        for x in D["dayDelta"]:
            dd += x
            self.day.append(dd)
        self.start, k = [], 0
        for c in D["lpo"]:
            self.start.append(k)
            k += c
        df = D["defects"]
        self.orphan = set(df["orphan"])
        self.dup = set(df["dup"])
        self.neg = {o: c for o, c in df["neg"]}

    def lines(self, o):
        return list(range(self.start[o], self.start[o] + self.D["lpo"][o]))


def clean_frame(S):
    D = S.D
    return [dict(o=o, dup=0, ck=D["cust"][o], exp=D["exp"][o], lines=S.lines(o), adj=[]) for o in range(D["nOrders"])]


def raw_frame(S):
    D, rows = S.D, []
    for o in range(D["nOrders"]):
        ck = -(o + 1) if o in S.orphan else D["cust"][o]
        adj = [S.neg[o]] if o in S.neg else []
        rows.append(dict(o=o, dup=0, ck=ck, exp=D["exp"][o], lines=S.lines(o), adj=adj))
        if o in S.dup:
            rows.append(dict(o=o, dup=1, ck=ck, exp=D["exp"][o], lines=S.lines(o), adj=[]))
    return rows


def ts_ordered(D, o):
    a, c, d = D["apprH"][o], D["carrH"][o], D["delivD"][o]
    return a is not None and c is not None and d is not None and a >= 0 and c >= 0 and d >= 0


def de_checks(S, rows):
    D = S.D
    per = [dict(rows=0, keyFail=0, fkFail=0, tsFail=0, lines=0, amtFail=0) for _ in range(3)]
    for r in rows:
        p = per[r["exp"]]
        p["rows"] += 1
        p["keyFail"] += 1 if r["dup"] else 0
        p["fkFail"] += 1 if r["ck"] < 0 else 0
        p["tsFail"] += 0 if ts_ordered(D, r["o"]) else 1
        for li in r["lines"]:
            p["lines"] += 1
            if D["price"][li] < 0 or D["freight"][li] < 0:
                p["amtFail"] += 1
        for c in r["adj"]:
            p["lines"] += 1
            if c < 0:
                p["amtFail"] += 1
    out = []
    for p in per:
        q = dict(p)
        q.update(keys=1 - p["keyFail"] / p["rows"], fk=1 - p["fkFail"] / p["rows"],
                 ts=1 - p["tsFail"] / p["rows"], amt=1 - p["amtFail"] / p["lines"])
        out.append(q)
    blocking = sum(p["keyFail"] + p["fkFail"] + p["amtFail"] for p in out)
    return dict(exports=out, blocking=blocking, rowsAll=sum(p["rows"] for p in out))


def repair(S, rows):
    out, dropped, resolved, quarantined = [], 0, 0, 0
    for r in rows:
        if r["dup"]:
            dropped += 1
            continue
        ck = r["ck"]
        if ck < 0:
            ck = S.D["cust"][r["o"]]
            resolved += 1
        adj = []
        for c in r["adj"]:
            if c < 0:
                quarantined += 1
            else:
                adj.append(c)
        out.append(dict(o=r["o"], dup=0, ck=ck, exp=r["exp"], lines=r["lines"], adj=adj))
    return out, dict(dropped=dropped, resolved=resolved, quarantined=quarantined)


def counts(rows, exp=None):
    per = {}
    for r in rows:
        if exp is None or r["exp"] == exp:
            per[r["ck"]] = per.get(r["ck"], 0) + 1
    return len(per), sum(1 for v in per.values() if v >= 2)


def registry(S, rows):
    D = S.D
    gmv = sum(D["price"][li] for r in rows for li in r["lines"]) + sum(c for r in rows for c in r["adj"])
    cust, rep = counts(rows)
    return dict(orders=len(rows), gmvCents=gmv, customers=cust, repeaters=rep, repeatRate=rep / cust)


def naive(S, rows):
    D = S.D
    cust = rep = 0
    for e in range(3):
        c, r_ = counts(rows, e)
        cust += c
        rep += r_
    tot = sum(D["price"][li] + D["freight"][li] for r in rows for li in r["lines"]) + sum(c for r in rows for c in r["adj"])
    return dict(orders=len(rows), gmvCents=tot, customers=cust, repeaters=rep, repeatRate=rep / cust)


def agree(x, ref):
    a, b = abs(x), abs(ref)
    if a == 0 and b == 0:
        return 1
    return min(a, b) / max(a, b)


def agreement(m, ref):
    o, g, r = agree(m["orders"], ref["orders"]), agree(m["gmvCents"], ref["gmvCents"]), agree(m["repeatRate"], ref["repeatRate"])
    return dict(orders=o, gmv=g, repeat=r, min=min(o, g, r))


def day_of(iso):
    y, m, d = map(int, iso.split("-"))
    return (date(y, m, d) - date(2016, 9, 1)).days


def feature_rows(S, rows):
    D, M = S.D, S.D["model"]
    n = len(rows)
    nxt, seen = [None] * n, {}
    for i in range(n - 1, -1, -1):
        ck = rows[i]["ck"]
        nxt[i] = seen.get(ck, -1)
        seen[ck] = i
    count, last, out = {}, {}, []
    for i, r in enumerate(rows):
        o = r["o"]
        d = S.day[o]
        prior = count.get(r["ck"], 0)
        rec = 1 / (1 + (d - last[r["ck"]])) if prior > 0 else 0
        val = 0
        fr = 0
        for li in r["lines"]:
            val += D["price"][li]
            fr += D["freight"][li]
        for c in r["adj"]:
            val += c
        v = max(val, 0) / 100
        x = [math.log(1 + prior), rec, math.log(1 + v), fr / (fr + max(val, 0) + 1), D["inst"][o], D["voucher"][o], len(r["lines"])]
        j = nxt[i]
        y = 1 if (j >= 0 and S.day[rows[j]["o"]] - d <= M["labelDays"]) else 0
        out.append(dict(o=o, dup=r["dup"], day=d, x=x, y=y, later=1 if j >= 0 else 0))
        count[r["ck"]] = prior + 1
        last[r["ck"]] = d
    return out


def sigmoid(z):
    return 1 / (1 + math.exp(-z))


def fit(X, y, M):
    m, k = len(X), len(X[0])
    mu, sd = [], []
    for j in range(k):
        s = 0
        for i in range(m):
            s += X[i][j]
        mu.append(s / m)
        s = 0
        for i in range(m):
            s += (X[i][j] - mu[j]) * (X[i][j] - mu[j])
        v = math.sqrt(s / m)
        sd.append(v if v > 0 else 1)
    Z = [[(x - mu[j]) / sd[j] for j, x in enumerate(row)] for row in X]
    w, b = [0.0] * k, 0.0
    lr, l2 = M["lr"], M["l2"]
    for _ in range(M["steps"]):
        g, gb = [0.0] * k, 0.0
        for i in range(m):
            zi = Z[i]
            z = b
            for j in range(k):
                z += w[j] * zi[j]
            e = sigmoid(z) - y[i]
            gb += e
            for j in range(k):
                g[j] += e * zi[j]
        b -= lr * gb / m
        for j in range(k):
            w[j] -= lr * (g[j] / m + l2 * w[j])
    return dict(w=w, b=b, mu=mu, sd=sd)


def score(model, x):
    z = model["b"]
    for j in range(len(x)):
        z += model["w"][j] * (x[j] - model["mu"][j]) / model["sd"][j]
    return sigmoid(z)


def auc(s, y):
    idx = sorted(range(len(s)), key=lambda i: (s[i], i))
    ranks = [0.0] * len(s)
    i = 0
    while i < len(idx):
        j = i
        while j + 1 < len(idx) and s[idx[j + 1]] == s[idx[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for t in range(i, j + 1):
            ranks[idx[t]] = r
        i = j + 1
    npos = sum(1 for v in y if v)
    tot = sum(ranks[i] for i in range(len(y)) if y[i])
    nn = len(y) - npos
    if not npos or not nn:
        return None
    return (tot - npos * (npos + 1) / 2) / (npos * nn)


def lift_top(s, y, frac):
    idx = sorted(range(len(s)), key=lambda i: (-s[i], i))
    n = math.ceil(len(s) * frac)
    pos = sum(1 for v in y if v)
    hit = sum(1 for i in idx[:n] if y[i])
    base = pos / len(s)
    return dict(n=n, hits=hit, positives=pos, base=base, lift=(hit / n) / base if base > 0 else None)


def ml_layer(S, rows, truth_rows, leak):
    M = S.D["model"]
    F, T = feature_rows(S, rows), feature_rows(S, truth_rows)
    cut = day_of(M["trainEnd"]) - M["labelDays"]
    t0, t1 = day_of(M["testStart"]), day_of(M["testEnd"])
    Xtr, ytr = [], []
    for f in F:
        if f["day"] > cut:
            continue
        x = list(f["x"]) + ([f["later"]] if leak else [])
        Xtr.append(x)
        ytr.append(f["y"])
    model = fit(Xtr, ytr, M)
    strain = [score(model, x) for x in Xtr]
    first = {}
    for f in F:
        if not f["dup"] and f["o"] not in first:
            first[f["o"]] = f
    ste, yte = [], []
    for t in T:
        if t["day"] < t0 or t["day"] > t1:
            continue
        x = list(first[t["o"]]["x"]) + ([0] if leak else [])
        ste.append(score(model, x))
        yte.append(t["y"])
    lt, ltr = lift_top(ste, yte, 0.1), lift_top(strain, ytr, 0.1)
    return dict(nTrain=len(Xtr), trainPos=sum(ytr), trainAuc=auc(strain, ytr), trainLift=ltr["lift"],
                nTest=len(ste), testPos=lt["positives"], base=lt["base"], testAuc=auc(ste, yte),
                topN=lt["n"], topHits=lt["hits"], lift=lt["lift"], weights=model["w"], bias=model["b"])


def store_facts(S, rows, store):
    D = S.D
    n = tot = low = 0
    for r in rows:
        sc = D["review"][r["o"]]
        if sc is None:
            continue
        if not any(D["lstore"][li] == store for li in r["lines"]):
            continue
        n += 1
        tot += sc
        low += 1 if sc <= 2 else 0
    mean = "%.1f" % (js_round(tot / n * 10) / 10) if n else "0.0"
    return dict(reviews=n, mean=mean, lowPct=js_round(low / n * 100) if n else 0)


def genai_layer(S, rows):
    D, G = S.D, S.D["genai"]
    passes = agree_n = fp = fn = 0
    verdicts = []
    for it in G["items"]:
        text = it["text"]
        low = text.lower()
        if it["kind"] == "listing":
            L = [l for l in D["listings"] if l["id"] == it["ref"]][0]
            req = [L["category"], "%d g" % L["weightG"]]
        else:
            st = [s for s in D["reviewStores"] if s["id"] == it["ref"]][0]
            f = store_facts(S, rows, st["store"])
            req = ["%d reviews" % f["reviews"], f["mean"], "%d%%" % f["lowPct"]]
        missing = [r for r in req if r.lower() not in low]
        banned = [b for b in G["banned"] if re.search(b["re"], text, re.I)]
        lo, hi = G["length"][it["kind"]]
        wc = len(text.split())
        ok = not missing and not banned and lo <= wc <= hi
        verdicts.append(1 if ok else 0)
        passes += 1 if ok else 0
        if ok == it["golden"]:
            agree_n += 1
        elif ok:
            fp += 1
        else:
            fn += 1
    n = len(G["items"])
    return dict(n=n, **{"pass": passes}, passRate=passes / n, agree=agree_n / n, falsePass=fp, falseFail=fn, verdicts=verdicts)


def product_layer(D, live):
    P = D["product"]
    share = 0
    if live["registry"]:
        share += P["share"]["registry"]
    if live["model"]:
        share += P["share"]["model"]
    if live["genai"]:
        share += P["share"]["genai"]
    blo, bhi = P["buyers"]
    rlo = blo * P["pricePerMonth"][0] * 12 * share
    rhi = bhi * P["pricePerMonth"][1] * 12 * share
    clo = P["buildCost"][0] + blo * P["runCostPerBuyerMonth"][0] * 12
    chi = P["buildCost"][1] + bhi * P["runCostPerBuyerMonth"][1] * 12
    return dict(share=share, buyers=[blo, bhi], revenue=[rlo, rhi], cost=[clo, chi], net=[rlo - chi, rhi - clo])


def run(S, skip_de=False, leak=False):
    D, G = S.D, S.D["gates"]
    clean, raw = clean_frame(S), raw_frame(S)
    de = de_checks(S, raw)
    rep_rows, rep = repair(S, raw)
    active = raw if skip_de else rep_rows
    after = de_checks(S, active)
    reg, nai = registry(S, active), naive(S, raw)
    ra, na = agreement(reg, D["reference"]), agreement(nai, D["reference"])
    ml = ml_layer(S, active, clean, leak)
    gen = genai_layer(S, active)
    de_ok = after["blocking"] == 0
    live = dict(de=de_ok, registry=de_ok and ra["min"] >= G["registryAgree"],
                model=ml["lift"] is not None and ml["lift"] >= G["liftMin"],
                genai=gen["passRate"] >= G["genaiPass"] and gen["agree"] >= G["genaiAgree"])
    return dict(de=de, repair=rep, deAfter=dict(blocking=after["blocking"], rows=after["rowsAll"]),
                registry=reg, naive=nai, registryAgree=ra, naiveAgree=na, ml=ml, genai=gen, live=live,
                product=product_layer(D, live))


def main():
    with open(os.path.join(HERE, "ssc-data.json")) as f:
        D = json.load(f)
    S = Data(D)
    out = dict(normal=run(S), skipDE=run(S, skip_de=True), leak=run(S, leak=True),
               skipDEleak=run(S, skip_de=True, leak=True))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
