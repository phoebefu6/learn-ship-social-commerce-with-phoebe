/* ssc-live.js - the five-layer value bench for learn-ship-social-commerce-with-phoebe
 *
 * Serai Commerce is CONSTRUCTED. The rows are REAL but derived and masked: the same 8,614 delivered
 * Olist orders as learn-ship-ecommerce-enabler-with-phoebe (Brazilian E-Commerce Public Dataset by
 * Olist, CC BY-NC-SA 4.0), built by materials/build-ssc-data.py into assets/ssc-data.js.
 *
 * COMPUTED LIVE, every click, on the shipped rows:
 *   DE        four checks per export: order keys unique after normalising, customer keys resolve,
 *             timestamps ordered (purchase <= approval <= carrier <= delivery), amounts >= 0.
 *             Repairs: drop re-sent duplicates, resolve keys through the crosswalk, move negative
 *             lines to an adjustments table. Timestamp inversions are flagged and kept.
 *   Analytics the registry's orders, GMV (item price, no freight) and repeat rate, against a naive
 *             sum of the export files, and both against the reference totals the builder computed
 *             from the source rows on a separate code path.
 *   ML        logistic regression by full-batch gradient descent (weights start at 0, fixed learning
 *             rate, steps and L2; features standardised on the training rows). Label: the customer
 *             orders again within 90 days. Train on orders whose label window closed by the end of
 *             month T; score month T+1 against what customers actually did. AUC (Mann-Whitney, ties
 *             averaged) and lift in the top decile against the base rate.
 *   Gen AI    the rubric (required facts present, banned claims absent, length) run over a
 *             PRE-WRITTEN constructed set of listing copy and review summaries (a browser cannot run
 *             a language model), against a hand-labelled golden verdict per output.
 *   Product   revenue and cost as RANGES from stated ASSUMPTIONS; a layer's share of the price
 *             counts only when its gate (Serai's constructed policy) passes.
 * Anti-lever: skip the DE layer (registry, model and gen AI facts run on the raw exports).
 * Break button: add a backfilled field that is only known after the next order.
 *
 * materials/ssc_reference.py is an independent pure-Python reference; materials/compare-ladder.py
 * checks that it and this file print the same canon over the whole ladder.
 */
(function (root) {
  "use strict";

  /* ---------- frames ---------- */
  function prep(D) {
    if (D._start) return D;
    var s = [], k = 0, dd = 0;
    D.day = D.dayDelta.map(function (x) { dd += x; return dd; });
    for (var o = 0; o < D.nOrders; o++) { s.push(k); k += D.lpo[o]; }
    D._start = s;
    D._orphan = {}; D.defects.orphan.forEach(function (o) { D._orphan[o] = 1; });
    D._dup = {}; D.defects.dup.forEach(function (o) { D._dup[o] = 1; });
    D._neg = {}; D.defects.neg.forEach(function (p) { D._neg[p[0]] = p[1]; });
    return D;
  }

  function lineIdx(D, o) {
    var out = [];
    for (var i = 0; i < D.lpo[o]; i++) out.push(D._start[o] + i);
    return out;
  }

  /* The asserted frame: one row per real order, resolved customer key, no adjustments. */
  function cleanFrame(D) {
    prep(D);
    var rows = [];
    for (var o = 0; o < D.nOrders; o++) rows.push({ o: o, dup: 0, ck: D.cust[o], exp: D.exp[o], lines: lineIdx(D, o), adj: [] });
    return rows;
  }

  /* The raw exports as they arrive: re-sends right after the original under a variant key, unresolved
     customer keys (negative = not in the customer table), refunds posted as negative lines. */
  function rawFrame(D) {
    prep(D);
    var rows = [];
    for (var o = 0; o < D.nOrders; o++) {
      var ck = D._orphan[o] ? -(o + 1) : D.cust[o];
      var adj = (D._neg[o] !== undefined) ? [D._neg[o]] : [];
      rows.push({ o: o, dup: 0, ck: ck, exp: D.exp[o], lines: lineIdx(D, o), adj: adj });
      if (D._dup[o]) rows.push({ o: o, dup: 1, ck: ck, exp: D.exp[o], lines: lineIdx(D, o), adj: [] });
    }
    return rows;
  }

  function tsOrdered(D, o) {
    var a = D.apprH[o], c = D.carrH[o], d = D.delivD[o];
    return a !== null && c !== null && d !== null && a >= 0 && c >= 0 && d >= 0;
  }

  /* ---------- DE: four checks per export ---------- */
  function deChecks(D, rows) {
    var per = [0, 1, 2].map(function () { return { rows: 0, keyFail: 0, fkFail: 0, tsFail: 0, lines: 0, amtFail: 0 }; });
    rows.forEach(function (r) {
      var p = per[r.exp];
      p.rows += 1;
      if (r.dup) p.keyFail += 1;
      if (r.ck < 0) p.fkFail += 1;
      if (!tsOrdered(D, r.o)) p.tsFail += 1;
      r.lines.forEach(function (li) { p.lines += 1; if (D.price[li] < 0 || D.freight[li] < 0) p.amtFail += 1; });
      r.adj.forEach(function (c) { p.lines += 1; if (c < 0) p.amtFail += 1; });
    });
    var out = per.map(function (p) {
      return { rows: p.rows, lines: p.lines, keyFail: p.keyFail, fkFail: p.fkFail, tsFail: p.tsFail, amtFail: p.amtFail,
        keys: 1 - p.keyFail / p.rows, fk: 1 - p.fkFail / p.rows, ts: 1 - p.tsFail / p.rows, amt: 1 - p.amtFail / p.lines };
    });
    var blocking = 0, rowsAll = 0;
    out.forEach(function (p) { blocking += p.keyFail + p.fkFail + p.amtFail; rowsAll += p.rows; });
    return { exports: out, blocking: blocking, rowsAll: rowsAll };
  }

  function repair(D, rows) {
    var out = [], quarantined = 0, dropped = 0, resolved = 0;
    rows.forEach(function (r) {
      if (r.dup) { dropped += 1; return; }
      var ck = r.ck;
      if (ck < 0) { ck = D.cust[r.o]; resolved += 1; }
      var adj = [];
      r.adj.forEach(function (c) { if (c < 0) quarantined += 1; else adj.push(c); });
      out.push({ o: r.o, dup: 0, ck: ck, exp: r.exp, lines: r.lines, adj: adj });
    });
    return { rows: out, dropped: dropped, resolved: resolved, quarantined: quarantined };
  }

  /* ---------- Analytics: registry vs naive vs reference ---------- */
  function registry(D, rows) {
    var gmv = 0, per = {}, cust = 0, rep = 0;
    rows.forEach(function (r) {
      r.lines.forEach(function (li) { gmv += D.price[li]; });
      r.adj.forEach(function (c) { gmv += c; });
      per[r.ck] = (per[r.ck] || 0) + 1;
    });
    Object.keys(per).forEach(function (k) { cust += 1; if (per[k] >= 2) rep += 1; });
    return { orders: rows.length, gmvCents: gmv, customers: cust, repeaters: rep, repeatRate: rep / cust };
  }

  function naive(D, rows) {
    var tot = 0, cust = 0, rep = 0;
    [0, 1, 2].forEach(function (e) {
      var per = {};
      rows.forEach(function (r) {
        if (r.exp !== e) return;
        per[r.ck] = (per[r.ck] || 0) + 1;
      });
      Object.keys(per).forEach(function (k) { cust += 1; if (per[k] >= 2) rep += 1; });
    });
    rows.forEach(function (r) {
      r.lines.forEach(function (li) { tot += D.price[li] + D.freight[li]; });
      r.adj.forEach(function (c) { tot += c; });
    });
    return { orders: rows.length, gmvCents: tot, customers: cust, repeaters: rep, repeatRate: rep / cust };
  }

  function agree(x, ref) {
    var a = Math.abs(x), b = Math.abs(ref);
    if (a === 0 && b === 0) return 1;
    return Math.min(a, b) / Math.max(a, b);
  }

  function agreement(m, ref) {
    var o = agree(m.orders, ref.orders), g = agree(m.gmvCents, ref.gmvCents), r = agree(m.repeatRate, ref.repeatRate);
    return { orders: o, gmv: g, repeat: r, min: Math.min(o, g, r) };
  }

  /* ---------- ML: features, time split, logistic regression ---------- */
  function dayOf(iso) { return Math.round((Date.parse(iso + "T00:00:00Z") - Date.parse("2016-09-01T00:00:00Z")) / 86400000); }

  /* One feature row per frame row, as of the purchase. Rows are in purchase order already. */
  function featureRows(D, rows) {
    var M = D.model, last = {}, count = {}, n = rows.length, out = new Array(n), nextOf = new Array(n), seen = {};
    for (var i = n - 1; i >= 0; i--) {             // walk backwards: the next row of the same customer
      var ck = rows[i].ck;
      nextOf[i] = (seen[ck] === undefined) ? -1 : seen[ck];
      seen[ck] = i;
    }
    for (i = 0; i < n; i++) {
      var r = rows[i], o = r.o, d = D.day[o];
      var prior = count[r.ck] || 0, rec = 0;
      if (prior > 0) rec = 1 / (1 + (d - last[r.ck]));
      var val = 0, fr = 0;
      r.lines.forEach(function (li) { val += D.price[li]; fr += D.freight[li]; });
      r.adj.forEach(function (c) { val += c; });
      var v = Math.max(val, 0) / 100;
      var x = [Math.log(1 + prior), rec, Math.log(1 + v), fr / (fr + Math.max(val, 0) + 1), D.inst[o], D.voucher[o], r.lines.length];
      var nx = nextOf[i], y = (nx >= 0 && D.day[rows[nx].o] - d <= M.labelDays) ? 1 : 0;
      out[i] = { o: o, dup: r.dup, day: d, x: x, y: y, later: nx >= 0 ? 1 : 0 };
      count[r.ck] = prior + 1;
      last[r.ck] = d;
    }
    return out;
  }

  function sigmoid(z) { return 1 / (1 + Math.exp(-z)); }

  function fit(X, y, M) {
    var m = X.length, k = X[0].length, mu = [], sd = [], j, i, s;
    for (j = 0; j < k; j++) {
      s = 0; for (i = 0; i < m; i++) s += X[i][j];
      mu.push(s / m);
      s = 0; for (i = 0; i < m; i++) s += (X[i][j] - mu[j]) * (X[i][j] - mu[j]);
      var v = Math.sqrt(s / m);
      sd.push(v > 0 ? v : 1);
    }
    var Z = X.map(function (row) { return row.map(function (x, jj) { return (x - mu[jj]) / sd[jj]; }); });
    var w = [], b = 0;
    for (j = 0; j < k; j++) w.push(0);
    for (var step = 0; step < M.steps; step++) {
      var g = [], gb = 0;
      for (j = 0; j < k; j++) g.push(0);
      for (i = 0; i < m; i++) {
        var z = b;
        for (j = 0; j < k; j++) z += w[j] * Z[i][j];
        var e = sigmoid(z) - y[i];
        gb += e;
        for (j = 0; j < k; j++) g[j] += e * Z[i][j];
      }
      b -= M.lr * gb / m;
      for (j = 0; j < k; j++) w[j] -= M.lr * (g[j] / m + M.l2 * w[j]);
    }
    return { w: w, b: b, mu: mu, sd: sd };
  }

  function score(model, x) {
    var z = model.b;
    for (var j = 0; j < x.length; j++) z += model.w[j] * (x[j] - model.mu[j]) / model.sd[j];
    return sigmoid(z);
  }

  function auc(s, y) {
    var idx = s.map(function (_, i) { return i; });
    idx.sort(function (a, b) { return s[a] - s[b] || a - b; });
    var ranks = new Array(s.length), i = 0;
    while (i < idx.length) {
      var j = i;
      while (j + 1 < idx.length && s[idx[j + 1]] === s[idx[i]]) j++;
      var r = (i + j) / 2 + 1;
      for (var t = i; t <= j; t++) ranks[idx[t]] = r;
      i = j + 1;
    }
    var np = 0, sum = 0;
    for (i = 0; i < y.length; i++) if (y[i]) { np += 1; sum += ranks[i]; }
    var nn = y.length - np;
    if (!np || !nn) return null;
    return (sum - np * (np + 1) / 2) / (np * nn);
  }

  function liftTop(s, y, frac) {
    var idx = s.map(function (_, i) { return i; });
    idx.sort(function (a, b) { return s[b] - s[a] || a - b; });
    var n = Math.ceil(s.length * frac), hit = 0, pos = 0;
    for (var i = 0; i < idx.length; i++) { if (y[idx[i]]) pos += 1; if (i < n && y[idx[i]]) hit += 1; }
    var base = pos / s.length;
    return { n: n, hits: hit, positives: pos, base: base, lift: base > 0 ? (hit / n) / base : null };
  }

  function mlLayer(D, rows, truthRows, leak) {
    var M = D.model, F = featureRows(D, rows), T = featureRows(D, truthRows);
    var trainCut = dayOf(M.trainEnd) - M.labelDays, t0 = dayOf(M.testStart), t1 = dayOf(M.testEnd);
    var Xtr = [], ytr = [];
    F.forEach(function (f) {
      if (f.day > trainCut) return;
      var x = f.x.slice();
      if (leak) x.push(f.later);                  // backfilled with hindsight: known for history only
      Xtr.push(x); ytr.push(f.y);
    });
    var model = fit(Xtr, ytr, M);
    var strain = Xtr.map(function (x) { return score(model, x); });
    // month T+1: one row per real order, features as the pipeline computed them, truth from the clean frame
    var firstRow = {};
    F.forEach(function (f) { if (!f.dup && firstRow[f.o] === undefined) firstRow[f.o] = f; });
    var ste = [], yte = [];
    T.forEach(function (t) {
      if (t.day < t0 || t.day > t1) return;
      var x = firstRow[t.o].x.slice();
      if (leak) x.push(0);                        // at scoring time the next order has not happened
      ste.push(score(model, x)); yte.push(t.y);
    });
    var lt = liftTop(ste, yte, 0.1), ltr = liftTop(strain, ytr, 0.1);
    return { nTrain: Xtr.length, trainPos: ytr.reduce(function (a, b) { return a + b; }, 0),
      trainAuc: auc(strain, ytr), trainLift: ltr.lift,
      nTest: ste.length, testPos: lt.positives, base: lt.base, testAuc: auc(ste, yte),
      topN: lt.n, topHits: lt.hits, lift: lt.lift,
      weights: model.w.map(function (v) { return v; }), bias: model.b };
  }

  /* ---------- Gen AI: rubric over the pre-written set ---------- */
  function storeFacts(D, rows, store) {
    var n = 0, sum = 0, low = 0;
    rows.forEach(function (r) {
      var sc = D.review[r.o];
      if (sc === null) return;
      var has = false;
      r.lines.forEach(function (li) { if (D.lstore[li] === store) has = true; });
      if (!has) return;
      n += 1; sum += sc; if (sc <= 2) low += 1;
    });
    return { reviews: n, mean: n ? (Math.round(sum / n * 10) / 10).toFixed(1) : "0.0", lowPct: n ? Math.round(low / n * 100) : 0 };
  }

  function wordCount(t) { return String(t).split(/\s+/).filter(function (w) { return w.length > 0; }).length; }

  function requiredFor(D, rows, item) {
    if (item.kind === "listing") {
      var L = D.listings.filter(function (l) { return l.id === item.ref; })[0];
      return [L.category, L.weightG + " g"];
    }
    var S = D.reviewStores.filter(function (s) { return s.id === item.ref; })[0];
    var f = storeFacts(D, rows, S.store);
    return [f.reviews + " reviews", f.mean, f.lowPct + "%"];
  }

  function rubric(D, rows, item) {
    var G = D.genai, text = item.text, low = text.toLowerCase();
    var req = requiredFor(D, rows, item), missing = req.filter(function (r) { return low.indexOf(String(r).toLowerCase()) < 0; });
    var banned = G.banned.filter(function (b) { return new RegExp(b.re, "i").test(text); }).map(function (b) { return b.label; });
    var lim = G.length[item.kind], wc = wordCount(text), lenOk = wc >= lim[0] && wc <= lim[1];
    return { id: item.id, kind: item.kind, required: req, missing: missing, banned: banned, words: wc, lenOk: lenOk,
      pass: missing.length === 0 && banned.length === 0 && lenOk, golden: item.golden };
  }

  function genaiLayer(D, rows) {
    var res = D.genai.items.map(function (it) { return rubric(D, rows, it); });
    var pass = 0, agreeN = 0, fp = 0, fn = 0;
    res.forEach(function (r) {
      if (r.pass) pass += 1;
      if (r.pass === r.golden) agreeN += 1;
      else if (r.pass) fp += 1; else fn += 1;
    });
    return { n: res.length, pass: pass, passRate: pass / res.length, agree: agreeN / res.length,
      falsePass: fp, falseFail: fn, verdicts: res.map(function (r) { return r.pass ? 1 : 0; }) };
  }

  /* ---------- Product: ranges from ASSUMPTIONS, gated by the layers ---------- */
  function productLayer(D, live) {
    var P = D.product, share = 0;
    if (live.registry) share += P.share.registry;
    if (live.model) share += P.share.model;
    if (live.genai) share += P.share.genai;
    var buyersLo = P.buyers[0], buyersHi = P.buyers[1];
    var revLo = buyersLo * P.pricePerMonth[0] * 12 * share, revHi = buyersHi * P.pricePerMonth[1] * 12 * share;
    var costLo = P.buildCost[0] + buyersLo * P.runCostPerBuyerMonth[0] * 12;
    var costHi = P.buildCost[1] + buyersHi * P.runCostPerBuyerMonth[1] * 12;
    return { share: share, buyers: [buyersLo, buyersHi], revenue: [revLo, revHi], cost: [costLo, costHi],
      net: [revLo - costHi, revHi - costLo] };
  }

  /* ---------- one full run ---------- */
  function run(D, opt) {
    opt = opt || {};
    prep(D);
    var G = D.gates, clean = cleanFrame(D), raw = rawFrame(D);
    var de = deChecks(D, raw), rep = repair(D, raw);
    var active = opt.skipDE ? raw : rep.rows;
    var deAfter = deChecks(D, active);
    var reg = registry(D, active), nai = naive(D, raw);
    var regAgree = agreement(reg, D.reference), naiAgree = agreement(nai, D.reference);
    var ml = mlLayer(D, active, clean, !!opt.leak);
    var gen = genaiLayer(D, active);
    var deOk = deAfter.blocking === 0;
    var live = {
      de: deOk,
      registry: deOk && regAgree.min >= G.registryAgree,
      model: ml.lift !== null && ml.lift >= G.liftMin,
      genai: gen.passRate >= G.genaiPass && gen.agree >= G.genaiAgree
    };
    var prod = productLayer(D, live);
    return { de: de, repair: { dropped: rep.dropped, resolved: rep.resolved, quarantined: rep.quarantined },
      deAfter: { blocking: deAfter.blocking, rows: deAfter.rowsAll }, registry: reg, naive: nai,
      registryAgree: regAgree, naiveAgree: naiAgree, ml: ml, genai: gen, live: live, product: prod };
  }

  function ladder(D) {
    return { normal: run(D, {}), skipDE: run(D, { skipDE: true }), leak: run(D, { leak: true }),
      skipDEleak: run(D, { skipDE: true, leak: true }) };
  }

  /* Properties that must hold on the shipped data; selfTest(D, true) plants a fault (one extra re-send
     slipped past the repair) and at least one property must then FAIL. */
  function properties(D, L, plant) {
    var n = L.normal, s = L.skipDE, k = L.leak;
    var cleanReg = n.registry;
    if (plant) cleanReg = registry(D, cleanFrame(D).concat([{ o: 0, dup: 1, ck: D.cust[0], exp: D.exp[0], lines: lineIdx(D, 0), adj: [] }]));
    return [
      ["repaired frame reproduces the reference orders", cleanReg.orders === D.reference.orders],
      ["repaired frame reproduces the reference GMV to the cent", cleanReg.gmvCents === D.reference.gmvCents],
      ["repaired frame reproduces the reference repeat customers", cleanReg.repeaters === D.reference.repeaters],
      ["no blocking DE failure after repair", n.deAfter.blocking === 0],
      ["skipping DE lowers registry agreement", s.registryAgree.min < n.registryAgree.min],
      ["skipping DE lowers month T+1 lift", s.ml.lift < n.ml.lift],
      ["the leak raises training AUC", k.ml.trainAuc > n.ml.trainAuc],
      ["the leak lowers month T+1 lift", k.ml.lift < n.ml.lift],
      ["AUC of a perfect ranking is 1", auc([0.1, 0.2, 0.9, 0.8], [0, 0, 1, 1]) === 1],
      ["the rubric can fail an output", n.genai.pass < n.genai.n]
    ];
  }

  function selfTest(D, plant) {
    var P = properties(D, ladder(D), !!plant), held = P.filter(function (p) { return p[1]; }).length;
    return { held: held, total: P.length, pass: held === P.length, failed: P.filter(function (p) { return !p[1]; }).map(function (p) { return p[0]; }) };
  }

  /* ---------- the widget (browser only) ---------- */
  var RUNGS = [
    { id: 0, label: "0 · Raw exports" }, { id: 1, label: "1 · + DE checks" }, { id: 2, label: "2 · + registry" },
    { id: 3, label: "3 · + model" }, { id: 4, label: "4 · + gen AI scoring" }, { id: 5, label: "5 · Scorecard" }
  ];
  function esc(x) {
    return String(x).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }
  function pct(x, dp) { return (x * 100).toFixed(dp === undefined ? 2 : dp) + "%"; }
  function fmt(n) { return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }
  function brl(c) { return "BRL " + (c / 100).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ","); }
  function usd(x) { return (x < 0 ? "-USD " : "USD ") + fmt(Math.abs(x)); }
  function kind(k) { return '<span class="ssc-kind is-' + k + '">' + k + "</span>"; }
  function metric(label, value, unit, k) {
    return '<div class="ssc-metric"><span class="ssc-mlabel">' + esc(label) + '</span><span class="ssc-mvalue">' + value +
      '</span><span class="ssc-munit">' + esc(unit) + "</span>" + kind(k) + "</div>";
  }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; return e; }

  var D, ui = {}, state = { rung: 0, skip: false, leak: false }, cache = {};

  function current() {
    var k = (state.skip ? "s" : "n") + (state.leak ? "l" : "");
    if (!cache[k]) cache[k] = run(D, { skipDE: state.skip, leak: state.leak });
    return cache[k];
  }

  function block(title, inner) { return '<div class="ssc-block"><h5 class="ssc-bh">' + title + "</h5>" + inner + "</div>"; }

  function render() {
    var R = current(), G = D.gates, M = D.model, html = "";
    ui.rbtn.forEach(function (b, i) { b.classList.toggle("is-on", i === state.rung); });
    ui.skipBtn.classList.toggle("is-on", state.skip);
    ui.skipBtn.textContent = state.skip ? "DE layer skipped: restore it" : "Skip the DE layer";
    ui.leakBtn.classList.toggle("is-on", state.leak);
    ui.leakBtn.textContent = state.leak ? "Remove the leaked field" : "Break it: add has_later_order, a field only known after the next order";

    var n = R.naive, na = R.naiveAgree, ref = D.reference;
    html += block("Rung 0 · the raw exports, summed as they arrive",
      '<div class="ssc-metrics">' +
      metric("Order rows", fmt(n.orders), "three export files; reference " + fmt(ref.orders) + " orders (" + pct(na.orders) + " agreement)", "measured") +
      metric("Naive GMV", brl(n.gmvCents), "price + freight + adjustments; reference " + brl(ref.gmvCents) + " (" + pct(na.gmv) + ")", "measured") +
      metric("Naive repeat rate", pct(n.repeatRate), fmt(n.repeaters) + " of " + fmt(n.customers) + " export-local customers; reference " + pct(ref.repeatRate) + " (" + pct(na.repeat) + ")", "measured") +
      "</div>");

    if (state.rung >= 1) {
      var rows = R.de.exports.map(function (e, i) {
        return "<tr><td><strong>" + esc(D.exports[i]) + "</strong></td><td>" + fmt(e.rows) + "</td><td>" + pct(e.keys) + "</td><td>" + pct(e.fk) +
          "</td><td>" + pct(e.ts) + "</td><td>" + pct(e.amt) + "</td></tr>";
      }).join("");
      var rep = state.skip ? '<p class="ssc-bad">DE layer skipped: ' + fmt(R.de.blocking) + " blocking failures flow straight into the registry, the model and the gen AI facts.</p>" :
        '<p class="ssc-note">Repair: ' + fmt(R.repair.dropped) + " re-sends dropped, " + fmt(R.repair.resolved) + " customer keys resolved through the crosswalk, " +
        fmt(R.repair.quarantined) + " negative lines moved to adjustments. Blocking failures after repair: " + fmt(R.deAfter.blocking) + ". Timestamp flags are kept: they are real rows and change no metric.</p>";
      html += block("Rung 1 · four data-quality checks per export",
        '<div class="ssc-tablewrap"><table class="clean ssc-table"><thead><tr><th>Export</th><th>Rows</th><th>Keys unique</th><th>Customer key resolves</th><th>Timestamps ordered</th><th>Amounts &ge; 0</th></tr></thead><tbody>' +
        rows + "</tbody></table></div>" + rep + kind("measured") + " " + kind("constructed") + '<span class="ssc-knote"> pass rates are measured; the re-sends, orphan keys and refund lines are constructed defects; the timestamp inversions are real</span>');
    }

    if (state.rung >= 2) {
      var g = R.registry, ra = R.registryAgree;
      html += block("Rung 2 · the registry, the naive sum and the reference",
        '<div class="ssc-tablewrap"><table class="clean ssc-table"><thead><tr><th>Metric</th><th>Registry' + (state.skip ? " (on raw)" : "") + "</th><th>Naive sum</th><th>Reference</th><th>Registry agreement</th></tr></thead><tbody>" +
        "<tr><td>Orders</td><td>" + fmt(g.orders) + "</td><td>" + fmt(n.orders) + "</td><td>" + fmt(ref.orders) + "</td><td>" + pct(ra.orders) + "</td></tr>" +
        "<tr><td>GMV (item price)</td><td>" + brl(g.gmvCents) + "</td><td>" + brl(n.gmvCents) + "</td><td>" + brl(ref.gmvCents) + "</td><td>" + pct(ra.gmv) + "</td></tr>" +
        "<tr><td>Repeat rate</td><td>" + pct(g.repeatRate) + "</td><td>" + pct(n.repeatRate) + "</td><td>" + pct(ref.repeatRate) + "</td><td>" + pct(ra.repeat) + "</td></tr>" +
        "</tbody></table></div>" +
        '<p class="ssc-note">Reference = totals the builder computed from the source rows on a separate code path. In production you never see it; you see only the gap between registry and naive sum.</p>');
    }

    if (state.rung >= 3) {
      var m = R.ml;
      html += block("Rung 3 · repeat-purchase model, trained to month T, scored on month T+1",
        '<div class="ssc-metrics">' +
        metric("Training AUC", m.trainAuc.toFixed(4), fmt(m.nTrain) + " orders up to " + M.trainEnd + " minus the 90-day label window, " + m.trainPos + " labelled repeats", "measured") +
        metric("Month T+1 AUC", m.testAuc.toFixed(4), fmt(m.nTest) + " orders in February 2018, " + m.testPos + " real repeats", "measured") +
        metric("Top-decile lift", m.lift.toFixed(2) + "x", m.topHits + " repeats in the top " + m.topN + " against a base rate of " + pct(m.base), "measured") +
        "</div>" +
        (state.leak ? '<p class="ssc-bad">Leak named: <strong>' + esc(M.leakName) + "</strong> is filled in with hindsight for history, so training sees the answer (AUC " + m.trainAuc.toFixed(4) +
          "). At scoring time the next order has not happened, the field is 0 for everyone, and the ranking falls to lift " + m.lift.toFixed(2) + "x.</p>" : "") +
        '<p class="ssc-note">Logistic regression by gradient descent, weights from zero, learning rate ' + M.lr + ", " + M.steps + " steps, L2 " + M.l2 +
        ". Features as of purchase: " + esc(M.features.join(", ")) + (state.leak ? ", plus the leaked field" : "") + ". Weights on the standardised features: " +
        m.weights.map(function (w) { return w.toFixed(3); }).join(", ") + ". With " + m.testPos + " positives one hit moves lift by " + (1 / m.topN / m.base).toFixed(2) + ".</p>");
    }

    if (state.rung >= 4) {
      var q = R.genai, items = D.genai.items, actRows = state.skip ? rawFrame(D) : repair(D, rawFrame(D)).rows;
      var list = items.map(function (it, i) {
        var v = q.verdicts[i] === 1, good = it.golden;
        var tag = v === good ? "" : (v ? ' <span class="ssc-tag is-bad">false pass</span>' : ' <span class="ssc-tag is-bad">false fail</span>');
        var req = requiredFor(D, actRows, it).join(" · ");
        if (it.kind === "listing") req += " · seller state " + D.listings.filter(function (l) { return l.id === it.ref; })[0].sellerState + " (not checked)";
        return "<tr><td>" + esc(it.id) + "</td><td>" + esc(it.kind) + "</td><td>" + esc(it.ref) + "</td><td>" + esc(req) + "</td><td>" + (v ? "pass" : "fail") + "</td><td>" + (good ? "fit to publish" : "reject") + tag + "</td></tr>";
      }).join("");
      html += block("Rung 4 · 20 pre-written outputs, scored by the rubric against a golden verdict",
        '<div class="ssc-metrics">' +
        metric("Rubric pass rate", pct(q.passRate, 0), q.pass + " of " + q.n + " outputs clear required facts, banned claims and length", "measured") +
        metric("Agreement with golden", pct(q.agree, 0), q.falsePass + " false pass, " + q.falseFail + " false fail", "measured") +
        "</div>" +
        '<div class="ssc-tablewrap"><table class="clean ssc-table"><thead><tr><th>Output</th><th>Kind</th><th>About</th><th>Required facts, live</th><th>Rubric</th><th>Golden</th></tr></thead><tbody>' + list + "</tbody></table></div>" +
        '<p class="ssc-note">' + kind("constructed") + " The text is pre-written: a browser cannot run a language model. The facts it is checked against are recomputed live from the " +
        (state.skip ? "raw exports, so the summaries written from clean facts now fail." : "repaired rows.") + "</p>");
    }

    if (state.rung >= 5) {
      var L = R.live, P = R.product, S = D.product.share;
      var row = function (name, ok, detail) { return "<tr><td><strong>" + name + "</strong></td><td>" + detail + '</td><td><span class="ssc-tag ' + (ok ? "is-good" : "is-bad") + '">' + (ok ? "live" : "held") + "</span></td></tr>"; };
      html += block("Rung 5 · the five-layer scorecard",
        '<div class="ssc-tablewrap"><table class="clean ssc-table"><thead><tr><th>Layer</th><th>Measured</th><th>Gate</th></tr></thead><tbody>' +
        row("DE", L.de, fmt(R.deAfter.blocking) + " blocking failures left") +
        row("Analytics", L.registry, "registry agreement " + pct(R.registryAgree.min) + " (gate " + pct(G.registryAgree, 1) + ")") +
        row("ML", L.model, "month T+1 lift " + R.ml.lift.toFixed(2) + "x (gate " + G.liftMin.toFixed(1) + "x)") +
        row("Gen AI", L.genai, "pass " + pct(R.genai.passRate, 0) + ", golden agreement " + pct(R.genai.agree, 0) + " (gates " + pct(G.genaiPass, 0) + ", " + pct(G.genaiAgree, 0) + ")") +
        row("Product", P.share > 0, "price share live " + pct(P.share, 0) + " (registry " + pct(S.registry, 0) + ", model " + pct(S.model, 0) + ", gen AI " + pct(S.genai, 0) + ")") +
        "</tbody></table></div>" +
        '<div class="ssc-metrics">' +
        metric("First-year revenue", usd(P.revenue[0]) + " to " + usd(P.revenue[1]), fmt(P.buyers[0]) + " to " + fmt(P.buyers[1]) + " paying sellers x USD " + D.product.pricePerMonth[0] + " to " + D.product.pricePerMonth[1] + " a month x live share", "assumption") +
        metric("First-year cost", usd(P.cost[0]) + " to " + usd(P.cost[1]), "build USD " + fmt(D.product.buildCost[0]) + " to " + fmt(D.product.buildCost[1]) + " + run USD " + D.product.runCostPerBuyerMonth[0] + " to " + D.product.runCostPerBuyerMonth[1] + " per seller a month", "assumption") +
        metric("First-year net", usd(P.net[0]) + " to " + usd(P.net[1]), "low revenue minus high cost, to high revenue minus low cost", "assumption") +
        "</div>");
    }
    ui.body.innerHTML = html;

    var R0 = cache.n || run(D, {});
    var v;
    if (state.rung < 5) v = '<div class="ssc-verdict is-ok"><strong>Rung ' + state.rung + " of 5.</strong> " + ["The files as they land: no checks, no definitions.", "The checks run; nothing downstream yet.", "Metrics with one definition each.", "One model, judged on the month it never saw.", "Gen AI judged by a rubric, and the rubric judged by a golden set."][state.rung] + "</div>";
    else if (!state.skip && !state.leak) v = '<div class="ssc-verdict is-good"><strong>All five layers live.</strong> Net first-year range ' + usd(R.product.net[0]) + " to " + usd(R.product.net[1]) + ", every figure from stated assumptions.</div>";
    else v = '<div class="ssc-verdict is-bad"><strong>' + (state.skip && state.leak ? "Skipped DE and a leak." : state.skip ? "DE layer skipped." : "Leaked field in training.") + "</strong> Live share of the price falls from " + pct(R0.product.share, 0) + " to " + pct(R.product.share, 0) +
      "; net range " + usd(R.product.net[0]) + " to " + usd(R.product.net[1]) + ".</div>";
    ui.verdict.innerHTML = v;
  }

  function init() {
    var host = document.getElementById("ssc-bench");
    if (!host || !root.SSC_DATA) return;
    D = root.SSC_DATA; prep(D);
    var p = el("div", "ssc-panel");
    p.appendChild(el("h4", null, "The five-layer value bench · Serai Commerce (constructed) on " + fmt(D.nOrders) + " real orders"));
    p.appendChild(el("p", "ssc-intro", fmt(D.nOrders) + " delivered orders, " + fmt(D.nLines) + " lines and " + fmt(D.nCustomers) + " customers, derived and masked from the public Olist dataset, split into three constructed marketplace exports. Every number below is computed in your browser on those rows each time you click."));
    var rr = el("div", "ssc-row"); rr.appendChild(el("span", "ssc-rlabel", "Rung"));
    ui.rbtn = RUNGS.map(function (r) {
      var b = el("button", "ssc-chip", esc(r.label)); b.type = "button";
      b.addEventListener("click", function () { state.rung = r.id; render(); });
      rr.appendChild(b); return b;
    });
    p.appendChild(rr);
    var ar = el("div", "ssc-row"); ar.appendChild(el("span", "ssc-rlabel", "Anti-lever"));
    ui.skipBtn = el("button", "ssc-chip is-anti"); ui.skipBtn.type = "button";
    ui.skipBtn.addEventListener("click", function () { state.skip = !state.skip; render(); });
    ar.appendChild(ui.skipBtn); p.appendChild(ar);
    ui.leakBtn = el("button", "ssc-break"); ui.leakBtn.type = "button";
    ui.leakBtn.addEventListener("click", function () { state.leak = !state.leak; render(); });
    p.appendChild(ui.leakBtn);
    ui.verdict = el("div"); p.appendChild(ui.verdict);
    ui.body = el("div", "ssc-body"); p.appendChild(ui.body);
    var st = selfTest(D), sp = selfTest(D, true);
    p.appendChild(el("p", "ssc-hint", "Self-test on load: " + st.held + " of " + st.total + " properties hold" + (st.failed.length ? " (failing: " + esc(st.failed.join("; ")) + ")" : "") +
      "; with a planted fault (one re-send slipped past the repair) " + (sp.pass ? "nothing failed, so do not trust this bench." : sp.total - sp.held + " properties fail, as they should.") +
      " Gates are Serai's own constructed policy, not a standard. Product figures are assumptions, not a price list."));
    p.appendChild(el("p", "ssc-attr", "Data: derived and masked from the Brazilian E-Commerce Public Dataset by Olist, Kaggle, licensed CC BY-NC-SA 4.0. No review text is used. Serai Commerce, the export split, the raw-export defects and the gen AI outputs are constructed."));
    host.appendChild(p);
    render();
    root.SSC_LIVE = {
      setRung: function (i) { state.rung = i; render(); },
      setSkip: function (b) { state.skip = !!b; render(); },
      setLeak: function (b) { state.leak = !!b; render(); },
      current: function () { return current(); },
      selfTest: function () { return selfTest(D); }
    };
  }

  var api = { prep: prep, cleanFrame: cleanFrame, rawFrame: rawFrame, deChecks: deChecks, repair: repair,
    registry: registry, naive: naive, agreement: agreement, featureRows: featureRows, fit: fit, auc: auc,
    liftTop: liftTop, mlLayer: mlLayer, storeFacts: storeFacts, genaiLayer: genaiLayer, productLayer: productLayer,
    run: run, ladder: ladder, selfTest: selfTest };

  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.SSC_ENGINE = api;
  if (typeof document !== "undefined") {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
    else init();
  }
})(typeof window !== "undefined" ? window : this);
