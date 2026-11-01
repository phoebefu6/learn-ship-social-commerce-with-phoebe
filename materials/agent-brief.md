# Agent brief - shared by every fan-out page of learn-ship-social-commerce-with-phoebe

Internal build document, filled from `~/.claude/skills/course-builder/references/agent-brief.template.md`
on 2026-11-01. Never link it from an audience page.

You are writing ONE static HTML session page. No servers, no npm. **If your target file already
exists on disk, do not write it; report that and stop.** Write the file, return its path and one
line of coverage. No HTML in your reply.

## Read first, in this order

1. The template page for YOUR track. Copy its structure, classes, SVG grammar and quiz markup
   EXACTLY, including how many options each question has (FOUR, A to D):
   - Leader (a2-a6): `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-ship-social-commerce-with-phoebe/courses/a1-five-layers-one-estate.html`
   - Builder (b2-b9): `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-ship-social-commerce-with-phoebe/courses/b1-the-merged-schema.html`
   - For bench numbers and the widget's wording, also read `.../courses/b10-the-five-layer-value-bench.html`.
2. The source map: every verified number, its evidence tier, per-session coverage, the seams. Use
   ONLY its numbers; never invent a statistic; if a fact is missing, teach the uncertainty.
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-ship-social-commerce-with-phoebe/materials/official-course-map.md`
3. The stylesheet `:root` block for the palette tokens:
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-ship-social-commerce-with-phoebe/assets/style.css`

## Page skeleton (keep every component)

toolbar (crumb EXACTLY "learn-ship-social-commerce-with-phoebe / Leader session N of 6" or
"... / Builder session N of 10", the repo name linked to ../index.html, #toggle-all, #zoom-toggle) ·
masthead (eyebrow "Ship It: Social Commerce, End to End · Leader session N of 6" or "· Builder session
N of 10", h1 with one `<span class="accent">`, .sub, .chip-row with the level chip 🟢 Foundational /
🟡 Intermediate / 🟠 Advanced-practical / 🔴 Advanced plus audience chips and "45 min", .agenda a1-a4)
· main.wrap · section#intro (Part 0: kicker, .lede, .legend pills, .callout.win "★ What you walk out
with tonight.") · 3 Parts, each `section.section#part-N` with section-kicker (klabel "Part N · covers
...", h2, `.tag.concept "N min live"`), a `.lede`, ONE figure, `details.card` accordions (summary:
`.mode.live` or `.mode.self`, title, `.mini`, `.caret ▶`), at least one `.callout.example` with
`span.ex-pill` "Real world" on the page · section#demo-1 Build-along (kicker `.tag.demo "★ 22 min ·
everyone builds"` (leader pages may use 20), .lede, ONE figure, `.steps > .step`, each with a
`.prompt-box.good` carrying a `span.label`; leader build-alongs are worksheets in prompt-boxes, builder
build-alongs are pandas / scikit-learn code with the printed output in a trailing comment ONLY if you
ran it, otherwise write "your numbers will differ" and print nothing invented) · section#exercise
Homework (ol, 4 items) · section#quiz (3 x `.quiz-q data-answer="0-based"`, `p.qtext`, FOUR
`button.qopt` "A · ...", `p.qwhy`; one `p.quiz-score` after the last) · section#official, h2 EXACTLY
"What this session teaches, and where it came from", `.covered > .covered-row` (pill solid ✓ / light
◐ + name + note), then the `.mono` line EXACTLY "Every fact on this page, and its verification tier,
is recorded in the course's source map." · section.cheat#cheatsheet (h3 "Leader session N cheat
sheet <span>· pin this</span>" or "Builder session N cheat sheet ...", .grid-2 of six .cheat-item) ·
`.callout.next` with `.nx-pill` "Next session" · footer.pagefoot · `<script src="../assets/app.js?v=1">`.

Head: the template's social meta block with this page's own title/description/url;
`<title>Leader session N · TITLE - learn ship social commerce with phoebe</title>` (Builder likewise);
`<link rel="stylesheet" href="../assets/style.css?v=1">`. Nothing else external.

First `details.card` in the FIRST Part is `open`; no other. Sentence case headings. Warm
practitioner voice, concrete, never dry. Inside prompt-boxes escape `&` `<` `>`. 450 to 650 lines
is guidance about depth, never a target: never collapse whitespace, dissolve a list into a
paragraph, or drop a component to fit.

## Hard rules (a violation is rework)

- NEVER an em dash or en dash, anywhere (prose, code, aria-labels, comments). Hyphen only.
- No meta text: never "this course", "in this course", "the course teaches", "banned here". State
  the professional norm directly with its reason. The two exact estate phrases above are the only
  self-references; "session 5" cross-references are fine.
- Attribution "by Phoebe Fu". Never "built with" a tool.
- Every number comes from the map or is labelled constructed. For constructed data print "your
  numbers will differ", never invented outputs as if run. Bench numbers must be ones the b10 widget
  prints (see the canon section of the map); quote them in the widget's format (2.90%, 3.71x, 0.7894).
- Contested or missing evidence: teach the disagreement; never resolve what the literature has not.
  Gen AI conversion uplift and "AI-written listings sell more": Fang et al. (read at source,
  abstract: no detectable impact to 16.3% by workflow) vs Cicek et al. (reported, a press release; it
  is about MENTIONING AI in copy). Never quote an uplift as a forecast.
- Citations in the exact form of the map's appendix; anything marked reported is "reported".
- NEVER "lottery" or "lotteries"; say the mechanism ("decided by row order", "arbitrary", "a
  random draw"). A verbatim quoted title in curly quotes is the only exception.
- Default to the English word. A Chinese term that is genuinely a name carries its English in
  brackets right after it, every occurrence.
- No marketplace, platform or vendor named as a recommendation: tool classes only. Open standards
  and the open-source libraries the build-alongs use (pandas, scikit-learn, Python) may be named.
  Olist may be named as the data source only.
- Titles, widget ids and class names must not collide with siblings. Banned: the sibling Enablers
  titles ("Seven domains", "Three exports, one schema", "The identity gate", "Stop, Hold, Love, Buy",
  "The enabler bench"), the `tw-` and `ssc-` prefixes (ssc- is the bench's), the word "bench" in any
  page other than b10's headings. Figure prefixes are per page (below).
- Serai Commerce is constructed: say "constructed" on every page where it first appears. The orders
  are real derived Olist rows (CC BY-NC-SA 4.0); never quote or paraphrase review TEXT (scores only).
- Light surfaces only: no dark band, no dark code box you add, no dark figure panel.

## Figure grammar (hand-drawn, every figure)

Palette, ONLY these hexes (no invented greys): ink `#1A2232` · muted `#4E5869` · faint-text
`#5C6577` · faint `#CDD2DC` · hairline `#E6E9EF` · primary amber `#966E08` (strokes, hachure, fills
with NO text on them) · deep `#6A4C04` (every accent text, values) · mid `#C49A35` · soft `#E8D29A` ·
tint `#FBF5E6` · ink-blue contrast `#A9C4EA` (fill ONLY, ink text on it, the one thing the figure is
about) · ink-blue deep `#1D3A66` · ink-blue tint `#EDF3FB` · paper `#FDFBF6` · `#FFFFFF` · universal
reds `#991B1B` `#FEF2F2` `#FCA5A5` only for a wrong-way panel or a failing value.

- `<figure class="zoomable">` > `<svg viewBox="0 0 880 H" role="img" aria-label="the data, not the
  shape">` > `<defs>` + `<style>` + content, then `<figcaption>🔍 Click to zoom - takeaway</figcaption>`.
  Grow H, never W.
- Prefix unique per figure, used for every class and id: page code + letter, e.g. `a2a`, `a2b`,
  `b5c`, `b9d` (so `a2aSk`, `a2aHc`, `a2aAr`, `.a2aH`).
- `<defs>` holds three things with the figure prefix P: a wobble filter `id="PSk"`
  (`feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="<int>"` +
  `feDisplacementMap scale="2.4" xChannelSelector="R" yChannelSelector="G"`, `x="-3%" y="-3%"
  width="106%" height="106%"`), a hachure pattern `id="PHc"` (7x7 userSpaceOnUse, rotate(-38), one
  `#966E08` line, opacity .5), an open arrowhead `id="PAr"` (path `M1 1 L9 5 L1 9`, fill none,
  `#1A2232` stroke 1.6). ALL shapes sit inside ONE `<g filter="url(#PSk)" fill="none"
  stroke="#1A2232" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">`; rects carry a
  tiny rotation (-4 to 4 degrees for hand-placed items, under 1 for panels). Fills: white, tint, the
  hachure for "the pile" or "the data" (never under text), and the ink-blue ONLY for the one thing
  the figure is about. One doodle anchor per figure, simple strokes, never a mascot. Text classes:
  `.PH` 800 12px ink heading · `.PL` 600 11-12px ink label · `.PS` 400 11px muted · `.PB` 800 11px
  `#1D3A66` · `.PV` 800 16-20px `#6A4C04` value · `.PW` 800 12px white on a deep fill · `.PA` 700 11px
  `#6A4C04` axis caption · `.PN` 400 12px muted note. Hand-stacked items must not overlap as painted
  rects (the gate flags a pile: draw a second outline as a path, not a rect).
- ALL `<text>` outside any filtered group, sans stack, never below 10.5px.
- Fit (owner: `diagram-kit.md`): max chars ≈ (box width - 20) / 7 at 12px, 6.4px/char at 11px;
  full-width note under 110 chars; 40px between neighbouring point labels; bottom note 22px below the
  last row, H clears it by 8px. A dashed guide line must not cross a label. When in doubt, shorten.
- Floor: one figure per Part plus one in the build-along. Draw the MECHANISM (a re-send becoming a
  fake repeat customer; a check splitting rows into pass, repair, quarantine, flag; the label window
  closing before the cutoff; a backfilled column known only in hindsight; a rubric reading facts from
  rows; a price share switched off by a failed gate), never a metaphor literally, never decoration.

## Voice and honesty

Every Part gets a real-world story from the map's sources or Olist's real quirks (multi-seller
orders, same-day repeat orders, the 122 timestamp inversions, multiple reviews per order).
Constructed cases say "constructed" on the page: Serai Commerce, its 48 brands, Exports A/B/C, the
re-sends, orphan keys and refund lines, the 20 gen AI outputs and golden verdicts, Serai's gates, all
product figures. The bench model is real logistic regression; the gen AI text is pre-written; say so.
Small numbers: the model's month T+1 has 24 positives; one hit moves lift by 0.41. Say it.

## Cross-links (absolute URLs)

- Enablers (business model, identity gate, registry DESIGN, Stop/Hold/Love/Buy): https://phoebefu6.github.io/learn-ship-ecommerce-enabler-with-phoebe/ (b1-b4 link back; its b2 three-exports page `courses/b2-three-exports-one-schema.html`, b3 identity gate `courses/b3-the-identity-gate.html`, b7 registry `courses/b7-registry-as-code.html`, a6 `courses/a6-metric-registry-before-ipo.html`)
- Stream analytics: https://phoebefu6.github.io/learn-live-commerce-analytics-with-phoebe/
- ML depth: https://phoebefu6.github.io/learn-ml-production-with-phoebe/ · https://phoebefu6.github.io/learn-model-evaluation-with-phoebe/ · https://phoebefu6.github.io/learn-feature-engineering-with-phoebe/
- Evals and the assistant pattern: https://phoebefu6.github.io/learn-ai-evals-with-phoebe/ · https://phoebefu6.github.io/learn-ship-internal-ai-assistant-with-phoebe/
- Product and pricing: https://phoebefu6.github.io/learn-data-product-with-phoebe/ · https://phoebefu6.github.io/learn-data-monetisation-with-phoebe/
- Retention depth: https://phoebefu6.github.io/learn-customer-retention-with-phoebe/
- Hub: https://phoebefu6.github.io/learn-with-phoebe/

## Footer chain(s) and session titles

Leader: a1 Five layers, one estate → a2 Sequencing and the cost of skipping → a3 What the model is
worth → a4 Gen AI a seller can trust → a5 The data product and its price → a6 The 12-month roadmap.
Builder: b1 The merged schema → b2 Data-quality tests that fail loudly → b3 The metric registry as
code → b4 Cohorts and repeat purchase → b5 A repeat-purchase model with a time split → b6 The leakage
hunt → b7 Listing copy and review summaries, scored → b8 A seller-support agent and its evals → b9
Packaging the data product → b10 The five-layer value bench.
Footer left: "Leader session N of 6 · learn-ship-social-commerce-with-phoebe · by Phoebe Fu &nbsp;·&nbsp; 📚 <a href="https://phoebefu6.github.io/learn-with-phoebe/">Learn with Phoebe ↗</a>"
Footer right: "← Prev: <title>" and "Next: <title> →" (a6: "← Prev" and "Course home").

Files (exact):
a2-sequencing-and-skipping.html · a3-what-the-model-is-worth.html · a4-gen-ai-a-seller-can-trust.html
· a5-the-data-product-and-its-price.html · a6-the-12-month-roadmap.html · b2-tests-that-fail-loudly.html
· b3-metric-registry-as-code.html · b4-cohorts-and-repeat-purchase.html · b5-model-with-a-time-split.html
· b6-the-leakage-hunt.html · b7-copy-and-summaries-scored.html · b8-seller-support-agent-evals.html
· b9-packaging-the-data-product.html (all in `courses/`).

Session titles (exact, sentence case, one accent span in h1): as in the chains above. b3's bare
title equals the Enablers Analyst session 7 title; keep it unless the main thread renames it, and
link to that page in b3's intro as the design it builds on.

---

## Per-page outlines (one agent per file; numbers are canon, quote only these)

### a2 · Sequencing and the cost of skipping (🟡 Intermediate)
Part 1 "Build order is a dependency, not a preference": figure a2a decision-tree (fund layer N? only
if N-1 passes its gate). Cards: the dependency table; the demo-first roadmap and when it is fine.
Part 2 "What skipping DE costs, layer by layer": figure a2b the cascade (re-send → registry 3.00% to
4.61%, agreement 65.14%; model labels 60 to 108 positives, lift 3.71x to 3.30x; Store 2 153 to 155
reviews, gen AI 15 to 7 of 20). Honest nuance card: the model survived. Part 3 "Pricing the skip":
figure a2c bar-numbers of live price share (100% / 35%) and net range (-USD 235,200 to USD 512,400 vs
-USD 282,000 to USD 75,600). Build-along: a sequencing worksheet (layer, gate, earliest quarter,
what is held if it slips). Quiz: why the registry broke before the model; which layer to fund first;
reading a skipped-layer scorecard. Covered: bench canon; NIST AI RMF "measure/manage".

### a3 · What the model is worth (🟡 Intermediate)
Part 1 "Base rate first": figure a3a gauge of base rate 4.18% in month T+1 (574 orders, 24 repeats)
against the top decile (9 of 58 = lift 3.71x). Part 2 "Only the next month counts": figure a3b
timeline of the split (train orders up to 2017-11-02, label window closes 2018-01-31, score February
2018); training AUC 0.6248 vs month T+1 0.7894 and why that ordering is noise here; scikit-learn
TimeSeriesSplit quote. Part 3 "A model that looks perfect": figure a3c before-after train AUC 0.9913
vs lift 1.65x with the leak; Kaufman et al. definition. Build-along: a "what is this model worth"
sheet: base rate, lift, repeats found per 100 contacts, cost per contact as an ASSUMPTION the reader
supplies. Small-number honesty (one hit = 0.41 lift). Seam: model-evaluation course.

### a4 · Gen AI a seller can trust (🟠 Advanced-practical)
Part 1 "A rubric and a golden set": figure a4a the two-layer check (rubric over outputs; golden
verdict over the rubric); 15 of 20 pass, 90% agreement. Part 2 "False pass, false fail": figure a4b
quadrant rubric x golden with L8 (false pass: ships-from claim not checked) and L4 (false fail: 1.75
kg); NIST confabulation and OWASP LLM09 overreliance. Part 3 "Does AI-written copy sell more?":
figure a4c overlap / two-study comparison: Fang et al. (randomized platform experiments, effects from
no detectable impact to 16.3% by workflow, abstract read at source; ~2% for descriptions only as
reported, versions differ) vs Cicek et al. (reported: survey experiments, mentioning AI lowered
purchase intent, more for high-risk products). Teach the disagreement, resolve neither. Also: with DE
skipped, 7 of 20 pass and agreement 50% because facts come from dirty rows. Build-along: write a
rubric for one listing type (required facts, banned claims, length) and five golden verdicts. Seam:
learn-ai-evals.

### a5 · The data product and its price (🟠 Advanced-practical)
Part 1 "Ranges from stated assumptions": figure a5a the range build-up (40 to 160 sellers x USD 150
to 350 a month x 12; build USD 150,000 to 240,000; run USD 20 to 35 a seller a month; revenue USD
72,000 to 672,000; cost USD 159,600 to 307,200; net -USD 235,200 to USD 512,400). Part 2 "Price by live
layers": figure a5b stacked share (registry 40%, model 35%, gen AI 25%) switched off by gates; leak
-> 65%, skip DE -> 35%, both -> 0%. Part 3 "The assumption that decides the sign": figure a5c a
tornado-style hand-drawn bar of which input moves the low end most (compute by hand from the stated
ranges ONLY; label it arithmetic on assumptions). Build-along: a one-page price sheet. Seams:
learn-data-product, learn-data-monetisation own pricing strategy; link, never reteach.

### a6 · The 12-month roadmap (🟠 Advanced-practical)
Part 1 "Four quarters, five gates": figure a6a timeline of layers into quarters with gates (a plan
shape, constructed for Serai, no new numbers). Part 2 "What to stop doing": figure a6b before-after
(demo-first vs gate-first roadmap). Part 3 "The go/hold board": figure a6c the scorecard from the
bench (all live; DE skipped; leak). NIST AI RMF govern/map/measure/manage as the frame. Build-along:
the 12-month roadmap on one page from the a1 estate sheet. Contested: none new; refer to a4's
disagreement. Last leader page: footer "← Prev: The data product and its price" and "Course home".

### b2 · Data-quality tests that fail loudly (🟡 Intermediate)
Part 1 "Four checks per export": figure b2a heatmap of pass rates (A 99.07 / 100.00 / 98.49 /
100.00; B 98.01 / 99.29 / 98.75 / 98.16; C 96.93 / 94.73 / 98.35 / 100.00). Part 2 "Repair,
quarantine or flag": figure b2b a check splitting rows into four bins (152 dropped, 113 resolved via
crosswalk, 64 quarantined, 122 inversions + 1 missing approval flagged and kept). Part 3 "Fail loudly":
figure b2c a pipeline that stops (blocking 333 vs 0 after repair). Build-along: pandas tests on the
b1 fact table from the public Olist file (keys unique, FK resolves, timestamps ordered, amounts >= 0);
run them or say "your numbers will differ". Seam: data-quality depth in learn-dataops.

### b3 · Building the metric registry (🟡 Intermediate)
Intro links to the Enablers registry design (b7 and a6 there). Part 1 "One definition each": figure
b3a definitions card (orders = distinct order keys; GMV = item price, no freight; repeat = customers
with 2+ orders / customers). Part 2 "Registry, naive, reference": figure b3b three-way bars (8,614 /
8,766 / 8,614; BRL 1,197,842.24 / 1,408,548.98 / 1,197,842.24; 3.00% / 2.90% / 3.00%). Part 3 "The
registry on dirty rows": figure b3c repeat rate 4.61%, agreement 65.14%; why a definition cannot fix a
bad row. Build-along: registry functions with tests in Python (pytest-style asserts).

### b4 · Cohorts and repeat purchase (🟡 Intermediate)
Part 1 "Monthly cohorts": figure b4a a cohort grid shape (draw the mechanism; quote only numbers you
compute in the build-along and print, else none). Part 2 "Repeat within 90 days": figure b4b timeline
of a customer's orders with the 90-day window; 197 sample orders followed by another within 90 days.
Part 3 "Same-day repeats": figure b4c 83 of 197 are same-day: split orders or real repeats? teach the
ambiguity. Real repeat rate 3.0% (250 of 8,333). Seams: learn-customer-retention, learn-rfm-modeling.

### b5 · A repeat-purchase model with a time split (🟠 Advanced-practical)
Part 1 "Features as of purchase": figure b5a the seven features on a timeline (all known at purchase;
review score excluded and why). Part 2 "The label window closes before the cutoff": figure b5b the
split (train to 2017-11-02, window to 2018-01-31, score February 2018). Part 3 "AUC and lift":
figure b5c bars train AUC 0.6248, month T+1 AUC 0.7894, lift 3.71x, base 4.18%. scikit-learn quotes
(logistic regression as a linear model for classification; regularization by default;
TimeSeriesSplit). Build-along: scikit-learn LogisticRegression on the public file with a time split;
your numbers will differ from the bench (different sample, solver). Seams: ML courses.

### b6 · The leakage hunt (🟠 Advanced-practical)
Part 1 "A field from the future": figure b6a has_later_order known in hindsight vs 0 at scoring;
train AUC 0.9913, lift 1.65x. Part 2 "Learn-predict separation": figure b6b Kaufman et al. definition
as a mechanism (every feature stamped with the time it became known). Part 3 "Timing traps":
figure b6c review score arrives after delivery; 83 same-day repeats happen before any review exists.
Weights: leak 1.389 vs at most 0.255 elsewhere (the widget prints the weights). Both levers: AUC
0.4922. Build-along: a leak audit table for a feature store (feature, time known, time needed).

### b7 · Listing copy and review summaries, scored (🟠 Advanced-practical)
Part 1 "The rubric as code": figure b7a three checks (required facts, banned claims, length 25-70 /
20-60 words). Part 2 "Facts come from rows": figure b7b Store 2: 153 reviews, 3.9, 18% (clean) vs 155
(raw); 15 to 7 of 20. Part 3 "Checking the checker": figure b7c golden agreement 90%, L4 false fail,
L8 false pass. Build-along: the rubric in Python over a few outputs YOU write (label them
constructed). OWASP LLM09 automatic validation. Seam: learn-ai-evals.

### b8 · A seller-support agent and its evals (🔴 Advanced)
NOT on the bench. Part 1 "Narrow tools": figure b8a agent with three tools (order status lookup,
refund policy lookup, hand-off) and nothing that writes. Part 2 "Golden questions": figure b8b a
golden set split (answerable, needs a human, must refuse); constructed examples only, labelled.
Part 3 "Excessive agency": figure b8c OWASP LLM06 root causes (excessive functionality, permissions,
autonomy) and prevention (minimise extensions, require user approval). Build-along: an eval harness
in plain Python over a constructed golden set; your numbers will differ. Seams:
learn-ship-internal-ai-assistant, learn-ai-evals.

### b9 · Packaging the data product (🔴 Advanced)
Part 1 "What ships": figure b9a the pack (registry tables, repeat list, copy drafts) each with its
gate. Part 2 "Tests as service levels": figure b9b the b2 checks and registry agreement as SLAs.
Part 3 "The price range": figure b9c revenue/cost/net ranges and the live share (canon from a5).
Build-along: a product spec page (contents, definitions, freshness, licence: derived Olist data is
CC BY-NC-SA, so a commercial product would need its own data; say so). Seams: learn-data-product,
learn-data-monetisation.
