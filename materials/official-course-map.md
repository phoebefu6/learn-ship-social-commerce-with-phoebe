# Official course map - learn-ship-social-commerce-with-phoebe

Internal build document (the "source map"). Never linked from an audience page.
"Ship It: Social Commerce, End to End" by Phoebe Fu. Approved skeleton 2026-11-01 (Leader 6 + Builder 10,
ship bucket, b10 = the bench). Built 2026-11-01 by the foundations lead.

## The angle in one paragraph

The five layers of a social-commerce data estate, built IN ORDER on one enabler: data engineering (DE),
analytics, machine learning (ML), gen AI, and a packaged data product. Each layer earns its place by what
the next one needs, and the bench shows what skipping one costs. Running case: **Serai Commerce**, the
CONSTRUCTED Southeast Asian social-commerce enabler from learn-ship-ecommerce-enabler-with-phoebe (48
brands, three marketplaces). Its rows are the same **8,614 derived Olist orders** the Enablers bench uses.
Every Serai figure, the export split, the raw-export defects, the gen AI outputs and every product
assumption are constructed and labelled so on the page. No marketplace, platform or vendor is named as a
recommendation: tool classes only; the open standards and open-source libraries the build-alongs use may
be named.

## Files and titles (exact; journey arrays in assets/app.js set by hand to these)

| File | Crumb | Title |
|---|---|---|
| courses/a1-five-layers-one-estate.html | Leader session 1 of 6 | Five layers, one estate |
| courses/a2-sequencing-and-skipping.html | Leader session 2 of 6 | Sequencing and the cost of skipping |
| courses/a3-what-the-model-is-worth.html | Leader session 3 of 6 | What the model is worth |
| courses/a4-gen-ai-a-seller-can-trust.html | Leader session 4 of 6 | Gen AI a seller can trust |
| courses/a5-the-data-product-and-its-price.html | Leader session 5 of 6 | The data product and its price |
| courses/a6-the-12-month-roadmap.html | Leader session 6 of 6 | The 12-month roadmap |
| courses/b1-the-merged-schema.html | Builder session 1 of 10 | The merged schema |
| courses/b2-tests-that-fail-loudly.html | Builder session 2 of 10 | Data-quality tests that fail loudly |
| courses/b3-metric-registry-as-code.html | Builder session 3 of 10 | Building the metric registry |
| courses/b4-cohorts-and-repeat-purchase.html | Builder session 4 of 10 | Cohorts and repeat purchase |
| courses/b5-model-with-a-time-split.html | Builder session 5 of 10 | A repeat-purchase model with a time split |
| courses/b6-the-leakage-hunt.html | Builder session 6 of 10 | The leakage hunt |
| courses/b7-copy-and-summaries-scored.html | Builder session 7 of 10 | Listing copy and review summaries, scored |
| courses/b8-seller-support-agent-evals.html | Builder session 8 of 10 | A seller-support agent and its evals |
| courses/b9-packaging-the-data-product.html | Builder session 9 of 10 | Packaging the data product |
| courses/b10-the-five-layer-value-bench.html | Builder session 10 of 10 | The five-layer value bench |

Title collision check (2026-11-01): `<title>` "Analyst session 7 · Building the metric registry - learn ship
ecommerce enabler with phoebe" exists in the sibling. b3's bare title is identical; the full `<title>`
strings differ by crumb and course suffix. FLAGGED for the main thread (rename b3 to e.g. "Registry
metrics as tested code" or keep, since b3 builds on that sibling page and links to it). No other title,
h1, widget prefix (`ssc-`) or case name (Serai Commerce is shared on purpose) collides.

## Per-session coverage (what each page teaches, and from where)

Leader track (no code; artifact = a one-page five-layer roadmap with a price range):
- **a1 Five layers, one estate.** The five layers and the dependency between them (each layer consumes
  the one below); the raw exports as they arrive; why "start with AI" fails; the scorecard as the
  leader's view. Sources: bench canon (raw vs repaired), NIST AI RMF "measure" (read at source).
- **a2 Sequencing and the cost of skipping.** The anti-lever as a leadership story: skip DE and the
  repeat rate reads 4.61% instead of 3.00%, gen AI facts go stale, 65% of the product price is held.
  Canon: skipDE block.
- **a3 What the model is worth.** Base rate, AUC and lift at the top decile in business words; why
  month T+1 is the only honest number; small-sample humility (24 positives). Kaufman et al. on leakage
  (abstract read at source). Canon: ml normal + leak.
- **a4 Gen AI a seller can trust.** Rubric + golden set, false passes vs false fails; the contested
  conversion claims (Fang et al. vs Cicek et al.) taught as disagreement; NIST confabulation, OWASP
  LLM09 (read at source). Canon: genai block.
- **a5 The data product and its price.** Ranges from stated assumptions; each layer's share of the
  price counts only when its gate passes. Seam: learn-data-product / learn-data-monetisation own pricing
  strategy. Canon: product block.
- **a6 The 12-month roadmap.** Sequencing the five layers into quarters with gates; what to stop doing;
  the go/hold board. Canon: scorecard.

Builder track (build-alongs in Python with pandas and scikit-learn as the open-source libraries; the
bench computes the same numbers in the browser):
- **b1 The merged schema.** Three exports into one schema (orders, lines, payments, review scores,
  timestamps); keys and grain; builds on the sibling's identity gate (b3 there) and three-export schema
  (b2 there), links back, never reteaches. Canon: frame counts.
- **b2 Data-quality tests that fail loudly.** The four checks per export with pass rates; repair vs
  quarantine vs flag; why timestamp inversions are flagged not dropped. Canon: de block.
- **b3 Building the metric registry.** Orders, GMV, repeat rate as tested definitions; registry vs naive
  sum vs reference; builds on the sibling's registry DESIGN (b7 there, a6 there). Canon: registry.
- **b4 Cohorts and repeat purchase.** Monthly cohorts on the repaired frame; repeat within 90 days;
  same-day repeat orders as a real Olist pattern (83 of 197 90-day repeats are same-day). Seam:
  learn-customer-retention, learn-rfm-modeling own retention depth.
- **b5 A repeat-purchase model with a time split.** Features as of purchase; label window must close
  before the cutoff; logistic regression; AUC and lift. scikit-learn docs (read at source). Seam:
  learn-ml-production, learn-model-evaluation, learn-feature-engineering own depth.
- **b6 The leakage hunt.** The backfilled field; train AUC 0.99 vs month T+1 lift 1.65; learn-predict
  separation (Kaufman et al.); review score as a timing trap. Canon: leak block.
- **b7 Listing copy and review summaries, scored.** The rubric as code, the golden set, the 20
  pre-written constructed outputs; facts recomputed from data, so dirty data breaks good copy. Seam:
  learn-ai-evals owns eval method.
- **b8 A seller-support agent and its evals.** One tool-using support agent pattern (order status,
  refund policy, hand-off), golden questions, excessive agency (OWASP LLM06, read at source). Seam:
  learn-ship-internal-ai-assistant owns the assistant pattern; nothing on the bench (constructed
  examples only, labelled).
- **b9 Packaging the data product.** What ships: tables, metric definitions, scores, copy assistant;
  SLAs as tests; the price range. Seam: learn-data-product, learn-data-monetisation.
- **b10 The five-layer value bench.** Everything above, computed live.

## Seams (absolute links; pick this side out loud, never reteach)

- https://phoebefu6.github.io/learn-ship-ecommerce-enabler-with-phoebe/ owns the business model, the
  identity gate, the metric registry DESIGN and the Stop/Hold/Love/Buy metric. b1-b4 link back.
- https://phoebefu6.github.io/learn-live-commerce-analytics-with-phoebe/ owns stream video and speech
  analytics.
- https://phoebefu6.github.io/learn-ml-production-with-phoebe/,
  https://phoebefu6.github.io/learn-model-evaluation-with-phoebe/,
  https://phoebefu6.github.io/learn-feature-engineering-with-phoebe/ own ML depth; we ship one model
  and hunt its leakage.
- https://phoebefu6.github.io/learn-ai-evals-with-phoebe/ and
  https://phoebefu6.github.io/learn-ship-internal-ai-assistant-with-phoebe/ own eval method and the
  assistant pattern; b7-b8 apply them to seller copy and a support agent.
- https://phoebefu6.github.io/learn-data-product-with-phoebe/ and
  https://phoebefu6.github.io/learn-data-monetisation-with-phoebe/ own product strategy and pricing;
  b9 and a5 package one product.
- Retention depth: https://phoebefu6.github.io/learn-customer-retention-with-phoebe/

## The data (build route, what is real, what is constructed)

Builder: `materials/build-ssc-data.py <olist-csv-dir> --write` (python3 -I). Source: Brazilian
E-Commerce Public Dataset by Olist, Kaggle, CC BY-NC-SA 4.0 (read at source via the Kaggle API
metadata, 2026-11-01: "100k orders from 2016 to 2018 made at multiple marketplaces in Brazil"; "This
is real commercial data, it has been anonymised"; the satisfaction survey is sent once the customer
receives the product or the estimated delivery date is due). No-login route
`kagglehub.dataset_download("olistbr/brazilian-ecommerce")`; copied into the scratch dir before reading.

**Step 1, the Enablers frame, ASSERTED.** The builder replays learn-ship-ecommerce-enabler's draws
(delivered orders; numpy default_rng(20260929); 250 of the 2,801 repeat customers plus one-timers at
the real 2,801 : 90,557 ratio; the sibling's synthetic name and phone draws replayed only to keep the
stream; then the 45/35/20 export split) and asserts: **8,333 customers, 8,614 orders, 9,843 lines,
exports 3,935 / 2,912 / 1,767.** MATCHED on 2026-11-01 (identical to the sibling's shipped
enabler-sample.js: same counts, same per-export counts).

**Step 2, added for this course (derived, masked; no Olist id leaves the builder):** purchase day
(running delta), approval offset (hours), carrier minus approval (hours, floor, so an inversion stays
negative), delivery minus carrier (days), max installments, voucher used, first review SCORE per order
(no review text is read into the output), lines per order, price and freight in cents, store renumbered
by frequency; facts for 10 listings (category from the translation table, weight in grams, seller
state) and 10 stores.

**Step 3, constructed raw-export defects (seed 20261101), labelled on the widget:**
- re-sent orders under a variant key: rates A 1% / B 2% / C 4% -> **152 duplicates**
- customer keys missing from the customer table: A 0% / B 1% / C 5% -> **113 orphans** (repaired
  through the crosswalk)
- refunds posted as a negative line, Export B 3% -> **64 negative lines** (quarantined to adjustments)
- REAL, not constructed: **122 orders whose carrier pickup is logged before payment approval, 1 with no
  approval timestamp** (flagged and kept; they do not change any metric)

Shipped: `assets/ssc-data.js` 358,037 bytes before the gen AI set was finalised; final size in the
canon section. Same payload in `materials/ssc-data.json`. json.dumps only.

## Builder-side counts quoted on b1 (data builder exploration, 2026-11-01)

Serai sample: 8,991 payment rows for 8,614 orders (credit card 6,655, boleto 1,697, voucher 479, debit
card 160); 8,585 review rows covering 8,546 orders, 39 orders with more than one review, 68 with none;
90-day repeat orders 197, of which 83 are same-day; 8.10% of orders delivered after the estimate.
Full public file (b1 build-along, run from scratch, outputs verified): 96,478 delivered orders, 93,358
people, 110,197 lines, 100,756 payment rows, 96,361 reviews; 2,875 orders with more than one payment
row, 525 with more than one review, 646 with none; item value BRL 13,221,498.11; lines joined to
payments before rolling up BRL 13,813,828.71 (+4.48%).

## Reference totals (builder, pandas on the source rows; an independent path from the engine)

8,614 orders · GMV BRL 1,197,842.24 (item price, no freight; 119,784,224 cents) · 8,333 customers ·
250 repeat customers · repeat rate 3.0001% (250 / 8,333) · payments BRL 1,393,663.67 · 122 timestamp
inversions · 1 missing approval.

## Canon (python ssc_reference.py vs node on assets/ssc-live.js: AGREE on 454 values, REL 1e-9;
planted 0.1% fault on normal/ml/lift caught; engine selfTest 10/10, planted fault fails 3 properties)

Run: `python3 -I materials/compare-ladder.py` (exit 0). Full canon: materials/canon-node.json.

**Rung 0, raw exports (naive sum of the files):** 8,766 order rows; naive GMV (price + freight +
adjustments) BRL 1,408,548.98; naive repeat rate 2.90% (247 / 8,506 export-local customers).
Agreement with reference: orders 98.27%, GMV 85.04%, repeat 96.79%.

**Rung 1, DE checks on the raw exports (pass rate per check):**

| Export | Rows | Keys unique | Customer key resolves | Timestamps ordered | Amounts >= 0 (lines) |
|---|---|---|---|---|---|
| A | 3,972 | 99.07% (37 fail) | 100.00% | 98.49% (60) | 100.00% of 4,527 |
| B | 2,971 | 98.01% (59) | 99.29% (21) | 98.75% (37) | 98.16% (64 of 3,477) |
| C | 1,823 | 96.93% (56) | 94.73% (96) | 98.35% (30) | 100.00% of 2,079 |

Blocking failures 333 (keys + keys-resolve + amounts) of 8,766 rows. Repair: 152 dropped, 113 resolved,
64 quarantined; 0 blocking after repair; timestamp flags kept.

**Rung 2, registry on the repaired frame:** 8,614 orders, BRL 1,197,842.24, 250 / 8,333 = 3.00% repeat.
Agreement with reference 100.00% on all three (the repair restores the source exactly; this is a
measured property, not a definition: the reference comes from the builder).

**Rung 3, model (logistic regression, 7 features, lr 1.0, 1,000 steps, L2 0.001, weights from 0;
label = another order within 90 days; train = orders up to 2017-11-02 so the window closes by
2018-01-31 = end of month T; score month T+1 = February 2018):**
train 2,744 orders, 60 positives, train AUC 0.6248 (in-sample, top-decile lift 2.49); month T+1 574
orders, 24 positives, base rate 4.18%, AUC 0.7894, top decile 58 orders with 9 positives, **lift 3.71**.
Honest limit: 24 positives, so one hit moves lift by 0.41. Train AUC below test AUC is small-sample
noise in a weak, noisy training label, not a sign of a good model.

**Rung 4, gen AI scoring (20 pre-written constructed outputs, rubric vs golden):** 15 of 20 pass
(75%); rubric agrees with the golden verdict on 18 of 20 (90%); 1 false pass (L8, a wrong ships-from
claim the rubric does not check), 1 false fail (L4, weight written as 1.75 kg, which the rubric cannot
read). Live review facts on the repaired frame, e.g. Store 2: 153 reviews, mean 3.9, 18% one or two
stars; Store 6: 101 reviews, 3.5, 24%.

**Rung 5, scorecard (gates are Serai's constructed policy: registry agreement >= 99.5%, top-decile
lift >= 2.0, gen AI pass >= 70% and golden agreement >= 85%; DE = zero blocking failures after
repair):** all four layers live, product share 100%. Product ASSUMPTIONS: 40 to 160 paying sellers,
USD 150 to 350 per seller per month, share of price registry 40% / model 35% / gen AI 25%, build USD
150,000 to 240,000, run USD 20 to 35 per seller per month. First-year revenue USD 72,000 to 672,000,
cost USD 159,600 to 307,200, **net USD -235,200 to +512,400**.

**Anti-lever, skip the DE layer (registry, model and gen AI facts run on the raw exports):**
registry 8,766 orders, BRL 1,209,566.40, repeat 384 / 8,337 = **4.61%**; agreement orders 98.27%, GMV
99.03%, **repeat 65.14%** (min). Model: train 2,795 rows with 108 "positives" (duplicates look like
same-day repeats), train AUC 0.6075, month T+1 AUC 0.7707, **lift 3.30** (8 hits; honest nuance: the
ranking barely moves, one hit of 24, because re-sends mostly add noise; the registry and gen AI take
the damage). Gen AI: **7 of 20 pass (35%), agreement 50%**, 9 false fails: every good review summary
now quotes the true count while the raw frame says otherwise (Store 2 reads 155 reviews). Live layers:
model only; share 35%; **net USD -282,000 to +75,600**.

**Break button, the backfilled field `has_later_order`:** train AUC **0.9913** (top-decile train lift
9.98); month T+1 AUC 0.6394, **lift 1.65** (4 hits), under the 2.0 gate; product share 65%; net USD
-260,400 to +277,200. Both together: month T+1 AUC 0.4922, lift 1.24; share 0%; net USD -307,200 to
-159,600.

## Verified facts and evidence tiers

READ AT SOURCE (2026-11-01):
- Olist dataset description and licence (Kaggle API metadata for olistbr/brazilian-ecommerce): CC
  BY-NC-SA 4.0; "100k orders from 2016 to 2018 made at multiple marketplaces in Brazil"; "real
  commercial data, it has been anonymised"; an order may have multiple items, each fulfilled by a
  distinct seller; survey sent after delivery or when the estimated date is due.
- scikit-learn TimeSeriesSplit: "Provides train/test indices to split time-ordered data, where other
  cross-validation methods are inappropriate, as they would lead to training on future data and
  evaluating on past data." Also: "successive training sets are supersets of those that come before them."
- scikit-learn linear models, logistic regression: "implemented as a linear model for classification
  rather than regression"; "Regularization is applied by default, which is common in machine learning
  but not in statistics." (The engine mirrors this with a small L2 term.)
- scikit-learn roc_auc_score: "Compute Area Under the Receiver Operating Characteristic Curve (ROC AUC)
  from prediction scores."
- Kaufman, Rosset, Perlich and Stitelman (2012), abstract (repository record of the TKDD paper):
  leakage is "the introduction of information about the data mining target that should not be
  legitimately available to mine from"; the paper proposes a "learn-predict separation" and ways to
  detect leakage when the modeler cannot control data collection. Full text not read: only the
  abstract may be quoted.
- NIST AI 600-1 (2024), section 2: "Confabulation: The production of confidently stated but erroneous
  or false content (known colloquially as 'hallucinations' or 'fabrications') by which users may be
  misled or deceived." Information Integrity is risk 8 of 12.
- NIST AI RMF 1.0 core: "the Core is composed of four functions: govern, map, measure, and manage";
  MEASURE uses quantitative, qualitative or mixed methods to analyse, assess, benchmark and monitor AI
  risk.
- OWASP Top 10 for LLM Applications 2025: LLM09 Misinformation, "Misinformation occurs when LLMs
  produce false or misleading information that appears credible"; overreliance "occurs when users place
  excessive trust in LLM-generated content, failing to verify its accuracy"; prevention includes
  automatic validation of key outputs. LLM06 Excessive Agency: root causes excessive functionality,
  excessive permissions, excessive autonomy; prevention includes minimising extensions and requiring
  user approval for high-impact actions.
- Fang, Yuan, Zhang, Donati and Sarvary, "Generative AI and Sales Productivity: Field Experiments in
  Online Retail", arXiv 2510.12049 (v6, revised 29 Jun 2026), abstract: randomized field experiments on
  a cross-border e-commerce platform; effects "ranging from no detectable impact to 16.3%" depending on
  GenAI's marginal contribution; gains "primarily through higher conversion rates rather than larger
  cart values".

REPORTED (secondary or not opened in full; say "reported" on the page):
- Fang et al. earlier version / summaries: AI product descriptions about +2% sales (v1 figure 2.05%);
  the 16.3% belongs to a pre-sale chatbot workflow, not to listing copy. Quote only as reported, and
  only with "versions differ".
- Cicek, Gursoy and Lu (2024), Journal of Hospitality Marketing & Management: experimental surveys of
  more than 1,000 US adults; "products described as using artificial intelligence were less popular",
  more so for high-risk products (Washington State University press release; paper not read). This is
  about MENTIONING AI in product copy, not about AI-written copy: say so.

THE DISAGREEMENT (a4, b7): randomized platform experiments find small-to-zero sales effects for AI
listing work and larger ones elsewhere; survey experiments find that mentioning AI lowers purchase
intent. Different questions, settings and outcomes; neither settles whether Serai's sellers would sell
more with AI-written copy. Teach both; resolve neither; measure on your own catalogue.

## Not covered (honest list)

- Identity resolution across exports (the sibling owns it; this course uses its resolved key).
- Stream video and speech analytics (learn-live-commerce-analytics).
- Model deployment, monitoring, feature stores, hyperparameter search (ML siblings).
- Running a real language model; the gen AI outputs are pre-written and constructed.
- Any conversion-uplift number as a forecast for Serai; any vendor or marketplace recommendation.
- Review TEXT analytics: the licence forbids shipping it here, so summaries work from scores only.
- Pricing strategy theory (learn-data-monetisation).

## Citation appendix (exact forms for pages)

- Olist (2018). Brazilian E-Commerce Public Dataset by Olist. Kaggle, CC BY-NC-SA 4.0. https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
- scikit-learn developers. TimeSeriesSplit; LogisticRegression (Linear Models user guide); roc_auc_score. https://scikit-learn.org/stable/
- Kaufman, S., Rosset, S., Perlich, C. and Stitelman, O. (2012). Leakage in data mining: formulation, detection, and avoidance. ACM TKDD 6(4), article 15. https://doi.org/10.1145/2382577.2382579
- NIST (2023). AI RMF 1.0, NIST AI 100-1. https://doi.org/10.6028/NIST.AI.100-1
- NIST (2024). Generative AI Profile, NIST AI 600-1. https://doi.org/10.6028/NIST.AI.600-1
- OWASP (2025). OWASP Top 10 for LLM Applications 2025. https://genai.owasp.org/llm-top-10/
- Fang, L., Yuan, Z., Zhang, K., Donati, D. and Sarvary, M. (2026). Generative AI and Sales Productivity: Field Experiments in Online Retail. arXiv 2510.12049. https://arxiv.org/abs/2510.12049
- Cicek, M., Gursoy, D. and Lu, L. (2024). Journal of Hospitality Marketing & Management (reported via Washington State University press release, 2024-07-30).
