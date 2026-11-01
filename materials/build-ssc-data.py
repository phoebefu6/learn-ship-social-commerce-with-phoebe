#!/usr/bin/env python3
"""Build the five-layer bench data for learn-ship-social-commerce-with-phoebe.

Internal build script. Not linked from any audience-facing page.

Usage
-----
  python3 -I materials/build-ssc-data.py <dir-with-olist-csvs> [--write]

The directory holds the Kaggle CSVs of the Brazilian E-Commerce Public Dataset by Olist
(CC BY-NC-SA 4.0). No-login route: kagglehub.dataset_download("olistbr/brazilian-ecommerce").

Step 1 reproduces the 8,614-order frame of learn-ship-ecommerce-enabler-with-phoebe
(materials/build-enabler-bench.py there: delivered orders, seed 20260929, 250 of the 2,801 repeat
customers plus one-timers at the real ratio, three marketplace exports split 45/35/20) and ASSERTS
it: 8,333 customers, 8,614 orders, 9,843 lines, exports 3,935 / 2,912 / 1,767. The random draws are
replayed in the same order as the sibling builder so the export split is identical.

Step 2 adds what this course needs, all DERIVED and MASKED (no Olist id, no review text):
  - per order: purchase day (shipped as a running delta, orders are in purchase order), approval / carrier / delivery offsets, installments, voucher flag,
    the first review SCORE (1-5; review text is never read into the output)
  - per line: price and freight in cents, the store (renumbered by frequency)
  - a small fact table for the ten listings and ten stores the gen AI set talks about
  - the reference totals the registry must reproduce, computed here with pandas on the source rows
    (an independent code path from the engine)

Step 3 adds the CONSTRUCTED defects of the raw exports (seeded, labelled on the widget):
  - duplicate re-sends under a variant order key (per-export rates DUP_RATE)
  - customer keys that do not resolve to the customer table (ORPHAN_RATE), with the crosswalk
  - refund adjustments posted as negative lines (NEG_RATE)
The timestamp inversions (carrier pickup logged before payment approval, one missing approval) are
REAL rows in the source, not constructed.

Output: assets/ssc-data.js (window.SSC_DATA = <json>) and materials/ssc-data.json, same payload,
serialised with json.dumps.
"""
import json
import math
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- sibling frame (do not change)
SEED = 20260929
N_REPEAT = 250
EXPORT_SHARE = [0.45, 0.35, 0.20]
FIRST = ["Ana", "Maria", "Joao", "Pedro", "Lucas", "Julia", "Mariana", "Gabriel", "Rafael", "Beatriz",
         "Carlos", "Fernanda", "Paulo", "Camila", "Bruno", "Larissa", "Felipe", "Amanda", "Rodrigo",
         "Leticia", "Marcos", "Patricia", "Thiago", "Aline", "Diego", "Renata", "Eduardo", "Vanessa",
         "Gustavo", "Bianca", "Daniel", "Carolina", "Vinicius", "Tatiana", "Leonardo", "Priscila",
         "Ricardo", "Natalia", "Andre", "Isabela"]
LAST = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira", "Lima",
        "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho", "Almeida", "Lopes", "Soares", "Fernandes",
        "Vieira", "Barbosa", "Rocha", "Dias", "Nascimento", "Andrade", "Moreira", "Nunes", "Marques",
        "Machado", "Mendes", "Freitas"]
EXPECT = {"customers": 8333, "orders": 8614, "lines": 9843, "exports": [3935, 2912, 1767]}

# ---------------------------------------------------------------- this course
DEFECT_SEED = 20261101
EXPORTS = ["Export A", "Export B", "Export C"]
DUP_RATE = [0.01, 0.02, 0.04]      # CONSTRUCTED: re-sent orders under a variant key
ORPHAN_RATE = [0.0, 0.01, 0.05]    # CONSTRUCTED: customer key missing from the customer table
NEG_RATE = [0.0, 0.03, 0.0]        # CONSTRUCTED: refunds posted as a negative line (Export B only)
DAY0 = pd.Timestamp("2016-09-01")

MODEL = {
    # time split: train on orders whose 90-day label window has CLOSED by the end of month T,
    # score the orders placed in month T+1
    "labelDays": 90,
    "trainEnd": "2018-01-31",      # end of month T
    "testStart": "2018-02-01",     # month T+1
    "testEnd": "2018-02-28",
    "features": ["prior orders (log)", "recency of prior order", "order value (log BRL)",
                 "freight share", "installments", "voucher used", "items in order"],
    "leakName": "has_later_order (backfilled)",
    "lr": 1.0, "steps": 1000, "l2": 0.001,
}
GATES = {  # Serai's policy choice, CONSTRUCTED, printed as such on the widget
    "registryAgree": 0.995, "liftMin": 2.0, "genaiPass": 0.70, "genaiAgree": 0.85,
}
PRODUCT = {  # every figure an ASSUMPTION, printed as such on the widget
    "buyers": [40, 160],                             # paying sellers: Serai's 48 brands plus outside sellers
    "pricePerMonth": [150, 350],                     # USD per seller per month for the full pack
    "share": {"registry": 0.40, "model": 0.35, "genai": 0.25},  # share of the price each layer carries
    "buildCost": [150000, 240000],                   # USD, one-off, first year
    "runCostPerBuyerMonth": [20, 35],                # USD
}


def mulberry32(seed):
    a = seed & 0xFFFFFFFF

    def imul(x, y):
        return ((x & 0xFFFFFFFF) * (y & 0xFFFFFFFF)) & 0xFFFFFFFF

    def nxt():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = imul(a ^ (a >> 15), 1 | a)
        t = ((t + imul(t ^ (t >> 7), 61 | t)) & 0xFFFFFFFF) ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return nxt


def load(d):
    ts = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
          "order_delivered_customer_date", "order_estimated_delivery_date"]
    o = pd.read_csv(os.path.join(d, "olist_orders_dataset.csv"), parse_dates=ts)
    c = pd.read_csv(os.path.join(d, "olist_customers_dataset.csv"))
    it = pd.read_csv(os.path.join(d, "olist_order_items_dataset.csv"))
    pay = pd.read_csv(os.path.join(d, "olist_order_payments_dataset.csv"))
    rv = pd.read_csv(os.path.join(d, "olist_order_reviews_dataset.csv"),
                     usecols=["review_id", "order_id", "review_score", "review_answer_timestamp"])
    pr = pd.read_csv(os.path.join(d, "olist_products_dataset.csv"))
    se = pd.read_csv(os.path.join(d, "olist_sellers_dataset.csv"))
    tr = pd.read_csv(os.path.join(d, "product_category_name_translation.csv"))
    return o, c, it, pay, rv, pr, se, tr


def frame(o, c, it):
    """Replay the sibling builder's draws in the same order; return the sorted order frame + exports."""
    o = o[o.order_status == "delivered"].merge(c, on="customer_id")
    per = o.groupby("customer_unique_id").order_id.nunique()
    rep = np.sort(per[per > 1].index.values)
    one = np.sort(per[per == 1].index.values)
    n_one = int(round(N_REPEAT * len(one) / len(rep)))
    rng = np.random.default_rng(SEED)
    pick = np.concatenate([rng.choice(rep, N_REPEAT, replace=False), rng.choice(one, n_one, replace=False)])
    pick = sorted(pick.tolist())
    so = o[o.customer_unique_id.isin(set(pick))].sort_values(
        ["order_purchase_timestamp", "order_id"]).reset_index(drop=True)
    fw = np.array([1 / (k + 1) for k in range(len(FIRST))]); fw /= fw.sum()
    lw = np.array([1 / (k + 1) for k in range(len(LAST))]); lw /= lw.sum()
    for _ in pick:                       # the sibling's synthetic names: replayed only to keep the stream
        rng.choice(len(FIRST), p=fw); rng.choice(len(LAST), p=lw)
    rng.integers(0, 100, len(pick))      # the sibling's synthetic phone digits, same reason
    exp = rng.choice(3, len(so), p=EXPORT_SHARE).tolist()
    li = it[it.order_id.isin(set(so.order_id))]
    got = {"customers": len(pick), "orders": len(so), "lines": len(li),
           "exports": [exp.count(i) for i in range(3)]}
    assert got == EXPECT, f"8,614 frame NOT reproduced: {got} vs {EXPECT}"
    print("frame reproduced:", got)
    return so, exp, pick


def build(d):
    o, c, it, pay, rv, pr, se, tr = load(d)
    so, exp, pick = frame(o, c, it)
    n = len(so)
    oidx = {x: i for i, x in enumerate(so.order_id)}

    # customers renumbered by first appearance (masked; Olist ids never leave this script)
    cmap, cust = {}, []
    for u in so.customer_unique_id:
        if u not in cmap:
            cmap[u] = len(cmap)
        cust.append(cmap[u])

    day = ((so.order_purchase_timestamp.dt.normalize() - DAY0).dt.days).astype(int).tolist()
    hours = lambda a, b: None if pd.isna(a) or pd.isna(b) else int(math.floor((a - b).total_seconds() / 3600))
    appr = [hours(a, p) for a, p in zip(so.order_approved_at, so.order_purchase_timestamp)]
    carr = [hours(cr, a) for cr, a in zip(so.order_delivered_carrier_date, so.order_approved_at)]
    deliv = [None if pd.isna(dl) else int(math.floor((dl - cr).total_seconds() / 86400))
             for dl, cr in zip(so.order_delivered_customer_date, so.order_delivered_carrier_date)]

    p2 = pay[pay.order_id.isin(oidx)]
    inst = p2.groupby("order_id").payment_installments.max()
    vou = p2.groupby("order_id").payment_type.apply(lambda s: int((s == "voucher").any()))
    payv = p2.groupby("order_id").payment_value.sum()
    installments = [int(max(1, inst[x])) for x in so.order_id]
    voucher = [int(vou[x]) for x in so.order_id]

    r2 = rv[rv.order_id.isin(oidx)].sort_values(["order_id", "review_answer_timestamp", "review_id"])
    first_score = r2.groupby("order_id").review_score.first()
    review = [int(first_score[x]) if x in first_score.index else None for x in so.order_id]

    li = it[it.order_id.isin(oidx)].copy()
    li["o"] = li.order_id.map(oidx)
    li = li.sort_values(["o", "order_item_id"]).reset_index(drop=True)
    freq = li.seller_id.value_counts()
    stores = sorted(freq.index, key=lambda s: (-freq[s], s))
    sidx = {x: i for i, x in enumerate(stores)}
    lpo = [0] * n
    for o_ in li.o:
        lpo[o_] += 1
    price = [int(round(v * 100)) for v in li.price]
    freight = [int(round(v * 100)) for v in li.freight_value]
    lstore = li.seller_id.map(sidx).tolist()

    # ---------------------------------------------------------- facts for the gen AI set
    pr = pr.merge(tr, on="product_category_name", how="left")
    pinfo = pr.set_index("product_id")
    sinfo = se.set_index("seller_id")
    pf = li.product_id.value_counts()
    cand = [p for p in sorted(pf.index, key=lambda p: (-pf[p], p))
            if not pd.isna(pinfo.loc[p, "product_category_name_english"]) and not pd.isna(pinfo.loc[p, "product_weight_g"])]
    listings = []
    for k, p in enumerate(cand[:10]):
        row = pinfo.loc[p]
        st = li[li.product_id == p].seller_id.iloc[0]
        listings.append({"id": "SKU-%02d" % (k + 1),
                         "category": str(row.product_category_name_english).replace("_", " "),
                         "weightG": int(row.product_weight_g),
                         "store": int(sidx[st]),
                         "sellerState": str(sinfo.loc[st, "seller_state"]),
                         "lines": int(pf[p])})
    # stores with the most reviewed orders; the engine recomputes their review facts live
    ord_store = li[["o", "seller_id"]].drop_duplicates()
    ord_store = ord_store[[review[o_] is not None for o_ in ord_store.o]]
    rc = ord_store.seller_id.value_counts()
    top_st = sorted(rc.index, key=lambda s: (-rc[s], s))[:10]
    review_stores = [{"id": "Store %d" % (sidx[s] + 1), "store": int(sidx[s])} for s in top_st]

    # ---------------------------------------------------------- reference totals (independent path)
    ref_orders = int(so.order_id.nunique())
    ref_gmv_cents = int(round(li.price.sum() * 100))
    pc = so.groupby("customer_unique_id").order_id.nunique()
    ref = {"orders": ref_orders, "gmvCents": ref_gmv_cents,
           "customers": int(pc.size), "repeaters": int((pc >= 2).sum()),
           "repeatRate": float((pc >= 2).sum() / pc.size),
           "paymentsBRL": round(float(payv.sum()), 2),
           "timestampInversions": int((so.order_delivered_carrier_date < so.order_approved_at).sum()),
           "approvalMissing": int(so.order_approved_at.isna().sum())}
    # check the integer cents path agrees with the float source sum
    assert abs(sum(price) - ref_gmv_cents) <= 1, (sum(price), ref_gmv_cents)
    ref["gmvCents"] = sum(price)

    # ---------------------------------------------------------- constructed defects
    rng = np.random.default_rng(DEFECT_SEED)
    dup, orphan, neg = [], [], []
    for o_ in range(n):
        e = exp[o_]
        u = rng.random(3)
        if u[0] < DUP_RATE[e]:
            dup.append(o_)
        if u[1] < ORPHAN_RATE[e]:
            orphan.append(o_)
        if u[2] < NEG_RATE[e]:
            first = sum(lpo[:o_])
            neg.append([o_, -price[first]])     # a full refund of the order's first line
    print("defects: dup", len(dup), "orphan", len(orphan), "neg", len(neg))

    data = {
        "about": ("Derived and masked from the Brazilian E-Commerce Public Dataset by Olist (CC BY-NC-SA 4.0). "
                  "Same 8,614 delivered orders as learn-ship-ecommerce-enabler-with-phoebe. Serai Commerce is "
                  "constructed; the export split and the raw-export defects are constructed; no review text."),
        "seed": SEED, "defectSeed": DEFECT_SEED, "day0": "2016-09-01",
        "exports": EXPORTS, "nOrders": n, "nLines": len(price), "nCustomers": len(cmap), "nStores": len(stores),
        "cust": cust, "exp": exp, "dayDelta": [day[0]] + [day[i] - day[i - 1] for i in range(1, n)], "apprH": appr, "carrH": carr, "delivD": deliv,
        "inst": installments, "voucher": voucher, "review": review,
        "lpo": lpo, "price": price, "freight": freight, "lstore": lstore,
        "defects": {"dup": dup, "orphan": orphan, "neg": neg,
                    "rates": {"dup": DUP_RATE, "orphan": ORPHAN_RATE, "neg": NEG_RATE}},
        "reference": ref, "model": MODEL, "gates": GATES, "product": PRODUCT,
        "listings": listings, "reviewStores": review_stores,
    }
    return data


def write(data, genai):
    data = dict(data)
    data["genai"] = genai
    body = json.dumps(data, separators=(",", ":"))
    with open(os.path.join(HERE, "ssc-data.json"), "w") as f:
        f.write(body)
    js = ("/* ssc-data.js - generated by materials/build-ssc-data.py with json.dumps. Derived, masked rows from the\n"
          " * Brazilian E-Commerce Public Dataset by Olist (CC BY-NC-SA 4.0). Serai Commerce, the export split,\n"
          " * the raw-export defects and the gen AI outputs are CONSTRUCTED. No review text. */\n"
          "window.SSC_DATA = " + body + ";\n")
    out = os.path.join(HERE, "..", "assets", "ssc-data.js")
    with open(out, "w") as f:
        f.write(js)
    print(f"wrote assets/ssc-data.js ({len(js)} bytes) and materials/ssc-data.json")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    D = build(sys.argv[1])
    print(json.dumps(D["reference"]))
    print(json.dumps(D["listings"], indent=0))
    if "--write" in sys.argv:
        sys.path.insert(0, HERE)
        from ssc_genai_set import GENAI   # the pre-written constructed outputs, hand-authored
        write(D, GENAI)
