#!/usr/bin/env python3
"""Write index.html for learn-ship-social-commerce-with-phoebe. Internal build script.

The knowledge-map data is serialised with json.dumps (never string interpolation).
Usage: python3 -I materials/build_landing.py
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
G, Y, O, R = "#34D399", "#FBBF24", "#FB923C", "#F87171"

LEADER = [
    ("a1-five-layers-one-estate.html", "🧱", "Five layers, one estate", G,
     "Data engineering, analytics, ML, gen AI and a data product, each defined by what it consumes from the layer below. 8,766 rows arrive for 8,614 real orders.",
     ["The five layers", "Raw is quietly wrong", "The scorecard"], "▶ Start here"),
    ("a2-sequencing-and-skipping.html", "🪜", "Sequencing and the cost of skipping", Y,
     "Build order as a leadership decision. Skip the bottom layer and the repeat rate, the review summaries and most of the product's price go with it.",
     ["Build in order", "What skipping costs", "The honest nuance"], None),
    ("a3-what-the-model-is-worth.html", "🎯", "What the model is worth", Y,
     "Base rate, AUC and lift in business words, judged on the month the model never saw, with the humility a small month demands.",
     ["Lift over base rate", "The next month only", "Small numbers"], None),
    ("a4-gen-ai-a-seller-can-trust.html", "✍️", "Gen AI a seller can trust", O,
     "A rubric, a golden set, false passes and false fails, and the contested claims about AI-written listings taught as a disagreement.",
     ["Rubric and golden set", "False pass, false fail", "Contested uplift"], None),
    ("a5-the-data-product-and-its-price.html", "🏷️", "The data product and its price", O,
     "Revenue and cost as ranges from stated assumptions, and a price that only counts the layers whose gates pass.",
     ["Ranges, not points", "Price by live layers", "The deciding assumption"], None),
    ("a6-the-12-month-roadmap.html", "🗓️", "The 12-month roadmap", O,
     "The five layers sequenced into quarters with gates, what to stop doing, and the board you take to the steering meeting.",
     ["Quarters and gates", "What to stop", "The go/hold board"], "the decision"),
]
BUILDER = [
    ("b1-the-merged-schema.html", "🗂️", "The merged schema", G,
     "Five tables with declared grains and an order-level fact table, built in pandas on the public Olist file, and the join that inflates item value by 4.48%.",
     ["Grain first", "Map, normalise, stamp", "Roll up, then join"], "▶ Start here"),
    ("b2-tests-that-fail-loudly.html", "🚨", "Data-quality tests that fail loudly", Y,
     "Keys unique, customer keys resolve, timestamps in order, amounts not negative: pass rates per export, and a repair, quarantine or flag rule for each.",
     ["Four checks", "Pass rate per export", "Repair or flag"], None),
    ("b3-metric-registry-as-code.html", "📏", "Building the metric registry", Y,
     "Orders, GMV and repeat rate as tested definitions, checked against a naive sum and a reference total.",
     ["One definition each", "Registry vs naive", "Control totals"], None),
    ("b4-cohorts-and-repeat-purchase.html", "🔁", "Cohorts and repeat purchase", Y,
     "Monthly cohorts on the repaired rows, repeat within 90 days, and the same-day repeat orders hiding in the real data.",
     ["Monthly cohorts", "Repeat in 90 days", "Same-day repeats"], None),
    ("b5-model-with-a-time-split.html", "📈", "A repeat-purchase model with a time split", O,
     "Features as of purchase, a label window that closes before the cutoff, logistic regression, AUC and lift on the next month.",
     ["Features as of purchase", "The time split", "AUC and lift"], None),
    ("b6-the-leakage-hunt.html", "🕵️", "The leakage hunt", O,
     "A backfilled field that makes training look perfect and the next month fall apart, and the learn-predict separation that stops it.",
     ["A field from the future", "Learn-predict separation", "Timing traps"], None),
    ("b7-copy-and-summaries-scored.html", "🧾", "Listing copy and review summaries, scored", O,
     "The rubric as code over twenty pre-written outputs, facts recomputed from rows, and a golden set that checks the checker.",
     ["Rubric as code", "Facts from rows", "Checking the checker"], None),
    ("b8-seller-support-agent-evals.html", "🤝", "A seller-support agent and its evals", O,
     "One support agent with narrow tools, golden questions, a hand-off, and the excessive-agency risks its evals must catch.",
     ["Narrow tools", "Golden questions", "Excessive agency"], None),
    ("b9-packaging-the-data-product.html", "📦", "Packaging the data product", O,
     "What ships: tables, definitions, scores and the copy assistant, with tests as the service levels and a price range on top.",
     ["What ships", "Tests as SLAs", "The price range"], None),
    ("b10-the-five-layer-value-bench.html", "🎛️", "The five-layer value bench", R,
     "All five layers computed live on 8,614 real orders, an anti-lever that skips data engineering, and a break button that leaks a field from the future.",
     ["Six rungs", "Skip the DE layer", "The leaked field"], "the capstone"),
]
SHORT = {
    "a1": "Five layers", "a2": "Sequencing", "a3": "Model worth", "a4": "Trusted gen AI", "a5": "Product price",
    "a6": "12-month roadmap", "b1": "Merged schema", "b2": "Loud tests", "b3": "Registry as code", "b4": "Cohorts",
    "b5": "Time-split model", "b6": "Leakage hunt", "b7": "Scored copy", "b8": "Support agent", "b9": "Packaging",
    "b10": "Value bench",
}


def cards(rows, track):
    out = []
    for i, (f, icon, title, diff, blurb, _c, pill) in enumerate(rows):
        n = i + 1
        cnum = f"{track} session {n}" + (" · start here" if n == 1 else "")
        meta = f'\n        <span class="meta"><span class="pill amber">{html.escape(pill)}</span></span>' if pill else ""
        out.append(f'''      <a class="course-card" href="courses/{f}" style="--diff:{diff}">
        <span class="cicon">{icon}</span>
        <span class="cnum">{cnum}</span>
        <h3>{html.escape(title)}</h3>
        <p>{html.escape(blurb)}</p>{meta}
      </a>''')
    return "\n".join(out)


def mindmap():
    sessions = []
    for rows in (LEADER, BUILDER):
        for f, _i, _t, diff, _b, concepts, _p in rows:
            key = f.split("-")[0]
            sessions.append({"label": SHORT[key], "href": "courses/" + f, "color": diff,
                             "concepts": [{"label": c, "href": "courses/" + f} for c in concepts]})
    return {"title": "Social Commerce,\nEnd to End", "centerColor": "#6A4C04", "sessions": sessions}


def path(label, steps, note):
    parts = []
    for i, (code, f) in enumerate(steps):
        if i:
            parts.append('        <span class="parr">→</span>')
        parts.append(f'        <a class="pstep" href="courses/{f}">{code}</a>')
    return (f'      <div class="path"><b>{label}</b>\n' + "\n".join(parts) +
            f'\n        <span style="font-size:.82rem;color:var(--muted)">{note}</span>\n      </div>')


def main():
    donor_style = open(os.path.join(HERE, "landing-style.css")).read()
    L = {r[0][:2]: r[0] for r in LEADER}
    B = {r[0].split("-")[0]: r[0] for r in BUILDER}
    paths = "\n".join([
        path("💼 I fund the roadmap", [("L1", L["a1"]), ("L2", L["a2"]), ("L5", L["a5"]), ("L6", L["a6"])],
             "the layers, the order, the price, the plan"),
        path("📊 I own the numbers", [("B1", B["b1"]), ("B2", B["b2"]), ("B3", B["b3"]), ("B4", B["b4"])],
             "schema, tests, registry, cohorts"),
        path("🤖 I build the models", [("B5", B["b5"]), ("B6", B["b6"]), ("B7", B["b7"]), ("B8", B["b8"]), ("B10", B["b10"])],
             "model, leak hunt, scored gen AI, the agent, then the bench"),
    ])
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- social:start -->
<meta name="description" content="Sixteen sessions on one social-commerce data estate, built in order: data engineering, analytics, machine learning, gen AI and a packaged data product, on 8,614 real Olist orders under a constructed enabler, with a five-layer bench computed in your browser. Free, by Phoebe Fu.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Learn with Phoebe">
<meta property="og:title" content="Ship It: Social Commerce, End to End - Learn with Phoebe">
<meta property="og:description" content="Five layers of a social-commerce data estate, each earning its place by what the next one needs.">
<meta property="og:url" content="https://phoebefu6.github.io/learn-ship-social-commerce-with-phoebe/">
<meta property="og:image" content="https://phoebefu6.github.io/learn-ship-social-commerce-with-phoebe/assets/og-cover.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Ship It: Social Commerce, End to End - Learn with Phoebe">
<meta name="twitter:description" content="Skip the bottom layer and the repeat rate reads 4.61% instead of 3.00%. Five layers, built in order.">
<meta name="twitter:image" content="https://phoebefu6.github.io/learn-ship-social-commerce-with-phoebe/assets/og-cover.png">
<!-- social:end -->
<title>Ship It: Social Commerce, End to End - Learn with Phoebe</title>
<link rel="stylesheet" href="assets/style.css?v=1">
<style>
{donor_style}</style>
</head>
<body>

<header class="masthead">
  <div class="wrap">
    <div class="eyebrow">Learn with Phoebe · Let's Ship It End to End</div>
    <h1>Ship It: <span class="accent">Social Commerce, End to End</span></h1>
    <p class="sub">One social-commerce data estate, built in the order its layers depend on each other. Serai Commerce, a constructed Southeast Asian enabler running 48 brands across three marketplaces, receives one export per marketplace; underneath are 8,614 real orders from the public Olist dataset. Six leader sessions decide what to build, in what order, what a model and a copy assistant are worth, and what the data product can charge. Ten builder sessions build it: the merged schema, tests that fail loudly, Building the metric registry, cohorts, a repeat-purchase model and its leak hunt, scored listing copy and review summaries, a seller-support agent with evals, the packaged product, and a five-layer bench computed in your browser.</p>
    <div class="stats-row">
      <div class="stat"><b data-count="16">16</b><span>sessions, two tracks</span></div>
      <div class="stat"><b data-count="8614">8,614</b><span>real orders</span></div>
      <div class="stat"><b data-count="5">5</b><span>layers, built in order</span></div>
      <div class="stat"><b data-count="20">20</b><span>gen AI outputs scored</span></div>
      <div class="stat"><b data-count="45">45</b><span>min per session</span></div>
    </div>
  </div>
</header>

<main class="wrap">

  <section class="section">
    <div class="paths" style="margin-top:0">
      <h2>Leader track 🧭 <span style="font-size:.85rem;font-weight:600;color:var(--muted)">· six sessions, no code</span></h2>
      <p class="plede">For whoever funds, sequences or signs off a commerce data roadmap. Decide the layers, their order, what each is worth, and the price of the product on top.</p>
    </div>

    <div class="course-grid">
{cards(LEADER, "Leader")}
    </div>
  </section>

  <section class="section">
    <div class="paths" style="margin-top:0">
      <h2>Builder track 🔧 <span style="font-size:.85rem;font-weight:600;color:var(--muted)">· ten sessions, Python and the browser</span></h2>
      <p class="plede">Serai's estate built layer by layer in the order the data flows, from three raw exports to a bench that runs all five layers at once.</p>
    </div>

    <div class="course-grid">
{cards(BUILDER, "Builder")}
    </div>

    <div class="diff-legend">
      <span><i style="background:#34D399"></i>start here</span>
      <span><i style="background:#FBBF24"></i>foundations</span>
      <span><i style="background:#FB923C"></i>hands-on</span>
      <span><i style="background:#F87171"></i>capstone</span>
    </div>
  </section>

  <section class="section">
    <div class="paths">
      <h2>Choose your path 🗺️</h2>
      <p class="plede">Three doors into the same estate. Each starts at the layer its reader is answerable for.</p>
{paths}
    </div>
  </section>

  <section class="section">
    <div class="paths" style="margin-top:0">
      <h2>Your passport 🎫</h2>
      <p class="plede">Clear all three quiz questions in a session and it gets stamped. Sixteen stamps across both tracks, and they live in this browser only.</p>
    </div>
    <div class="pp-strip"></div>
  </section>

  <section class="section">
    <div class="paths" style="margin-top:0">
      <h2>What is real here 🧾</h2>
      <p class="plede">A course about trustworthy numbers should be exact about which of its own are measured.</p>
    </div>
    <table class="clean">
      <tr><th>Claim</th><th>Status</th></tr>
      <tr><td>Serai Commerce, its brands, its three exports and their defects</td><td>Constructed, continued from the Social Commerce Enablers course and labelled wherever it appears. No real company's data is shown</td></tr>
      <tr><td>The orders, lines, prices, freight, timestamps and review scores</td><td>Real: 8,614 delivered orders from the Brazilian E-Commerce Public Dataset by Olist (CC BY-NC-SA 4.0), derived and masked; the same sample the Enablers course uses. No review text is used</td></tr>
      <tr><td>Every check, metric, model score and rubric verdict on the bench</td><td>Computed live in your browser on those rows. An independent Python reference matches every number on the ladder</td></tr>
      <tr><td>The listing copy and review summaries</td><td>Pre-written and constructed, because a browser cannot run a language model. The facts they are checked against are computed</td></tr>
      <tr><td>Gates, prices, costs and buyer counts</td><td>Serai's constructed policy and stated assumptions, shown as ranges and labelled on the widget</td></tr>
      <tr><td>Leakage, time-ordered splits, ROC AUC, NIST and OWASP</td><td>Read at source: Kaufman et al. (2012), the scikit-learn documentation, NIST AI 100-1 and AI 600-1, and the OWASP Top 10 for LLM Applications 2025</td></tr>
      <tr><td>Whether AI-written listings sell more</td><td>Contested, and taught as a disagreement between a randomized platform study and survey experiments. No uplift figure is offered as a forecast</td></tr>
    </table>
  </section>

  <section class="section mm-section">
    <h2>The knowledge map 🧠</h2>
    <p class="mm-lede">Both tracks at a glance - hover a session to spotlight its concepts, click any node to jump in.</p>
    <div class="mm-wrap"><div id="mindmap"></div></div>
  </section>

  <footer class="pagefoot">
    <span>learn-ship-social-commerce-with-phoebe · by Phoebe Fu &nbsp;·&nbsp; 📚 <a href="https://phoebefu6.github.io/learn-with-phoebe/">Learn with Phoebe ↗</a></span>
    <span>Pairs with <a href="https://phoebefu6.github.io/learn-ship-ecommerce-enabler-with-phoebe/">Social Commerce Enablers ↗</a> and <a href="https://phoebefu6.github.io/learn-data-product-with-phoebe/">Data Products ↗</a></span>
  </footer>

</main>

<script>
window.MINDMAP_DATA = {json.dumps(mindmap(), indent=2, ensure_ascii=False)};
</script>
<script src="assets/mindmap.js?v=1"></script>
<script src="assets/app.js?v=1"></script>
</body>
</html>
'''
    with open(os.path.join(HERE, "..", "index.html"), "w") as f:
        f.write(page)
    print("wrote index.html")


if __name__ == "__main__":
    main()
