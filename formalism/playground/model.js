// Pathwise convolutional-utility model with felt news. Port of formalism/pathwise.py, plus the
// direct (non-recursive) model. Deterministic announcements; certainty-equivalent forecasts.
(function (root) {
  "use strict";

  // Anticipation a·α^j, memory m·μ^j, news k_n(j) = n·ν^j (γ·n·ν^j for j ≥ 1 with Kőszegi–Rabin's γ).
  function kernels(p) {
    const kf = new Float64Array(p.T), kb = new Float64Array(p.T), kn = new Float64Array(p.T);
    const gamma = p.gamma == null ? 1 : p.gamma;
    for (let j = 1; j < p.T; j++) {
      kf[j] = p.a * Math.pow(p.al, j);
      kb[j] = p.m * Math.pow(p.mu, j);
      kn[j] = gamma * p.n * Math.pow(p.nu, j);
    }
    kn[0] = p.n;
    return { kf, kb, kn };
  }

  // Forecast at time t of base utility on [0, T). t = -1 is the prior.
  function forecastU(p, t) {
    const u = new Float64Array(p.T).fill(p.base);
    for (const ev of p.events) {
      const s = ev.at;
      if (s < 0 || s >= p.T) continue;
      const cancelled = ev.cancel != null && ev.cancel <= Math.min(t, s);
      if (cancelled) continue;
      if (s <= t || (ev.announce != null && ev.announce <= t)) u[s] += ev.value;
    }
    return u;
  }

  // LU with partial pivoting on an n x n row-major Float64Array; returns a solver.
  function luSolver(M, n) {
    const piv = new Int32Array(n);
    for (let i = 0; i < n; i++) piv[i] = i;
    for (let k = 0; k < n; k++) {
      let best = k, bv = Math.abs(M[k * n + k]);
      for (let i = k + 1; i < n; i++) {
        const v = Math.abs(M[i * n + k]);
        if (v > bv) { bv = v; best = i; }
      }
      if (bv < 1e-14) return null;
      if (best !== k) {
        for (let j = 0; j < n; j++) {
          const tmp = M[k * n + j]; M[k * n + j] = M[best * n + j]; M[best * n + j] = tmp;
        }
        const tp = piv[k]; piv[k] = piv[best]; piv[best] = tp;
      }
      const d = M[k * n + k];
      for (let i = k + 1; i < n; i++) {
        const f = (M[i * n + k] /= d);
        if (f !== 0) for (let j = k + 1; j < n; j++) M[i * n + j] -= f * M[k * n + j];
      }
    }
    return function (rhs) {
      const x = new Float64Array(n);
      for (let i = 0; i < n; i++) x[i] = rhs[piv[i]];
      for (let i = 0; i < n; i++) { let s = x[i]; for (let j = 0; j < i; j++) s -= M[i * n + j] * x[j]; x[i] = s; }
      for (let i = n - 1; i >= 0; i--) { let s = x[i]; for (let j = i + 1; j < n; j++) s -= M[i * n + j] * x[j]; x[i] = s / M[i * n + i]; }
      return x;
    };
  }

  // A on the remaining life [t, T): row i, column j holds the weight of position j in position i.
  function echoMatrix(kf, kb, n) {
    const A = new Float64Array(n * n);
    for (let i = 0; i < n; i++)
      for (let j = 0; j < n; j++)
        A[i * n + j] = j > i ? kf[j - i] : j < i ? kb[i - j] : 0;
    return A;
  }

  // All roots of h(s) = s - sum_j nu_j phi(x0_j + s g_j - prev_j). h is piecewise linear with kinks
  // where a revision changes sign, so its roots are found exactly, interval by interval.
  function newsRoots(x0, g, xPrev, t, kn, n, phi) {
    // Revisions below rounding noise are no news (past the threshold, any bad news has no felt state).
    const d = new Float64Array(n);
    for (let j = 0; j < n; j++) { const r = x0[j] - xPrev[t + j]; d[j] = Math.abs(r) < 1e-9 * (1 + Math.abs(x0[j])) ? 0 : r; }
    const h = (s) => { let v = s; for (let j = 0; j < n; j++) v -= kn[j] * phi(d[j] + s * g[j]); return v; };
    const br = [];
    for (let j = 0; j < n; j++) if (kn[j] !== 0 && Math.abs(g[j]) > 1e-15) br.push(-d[j] / g[j]);
    br.sort((p, q) => p - q);
    const pts = [];
    if (br.length === 0) pts.push(-1, 1); else { pts.push(br[0] - 1); for (const b of br) pts.push(b); pts.push(br[br.length - 1] + 1); }
    const roots = [];
    const add = (r) => { if (!roots.some((q) => Math.abs(q - r) < 1e-9 * (1 + Math.abs(r)))) roots.push(r); };
    // left ray, finite intervals, right ray: h is linear on each
    const seg = (l, r) => {
      const hl = h(l), hr = h(r);
      if (hl === 0) add(l);
      if (hr === 0) add(r);
      if (hl * hr < 0) add(l - hl * (r - l) / (hr - hl));
    };
    const ray = (x, dir) => {   // h linear beyond x; slope from two points on the ray
      const hx = h(x), h2 = h(x + dir), slope = (h2 - hx) * dir;
      if (hx === 0) { add(x); return; }
      const r = x - hx / slope;
      if (slope !== 0 && (r - x) * dir > 0) add(r);
    };
    ray(pts[0], -1);
    for (let i = 0; i + 1 < pts.length; i++) seg(pts[i], pts[i + 1]);
    ray(pts[pts.length - 1], 1);
    return roots.sort((p, q) => p - q);
  }

  function simulate(p) {
    const T = p.T, { kf, kb, kn } = kernels(p);
    const lam = p.lam, phi = (x) => (x >= 0 ? x : lam * x);
    const e = new Float64Array(T), fHist = new Float64Array(T);
    const comp = { base: new Float64Array(T), anticipation: new Float64Array(T),
                   memory: new Float64Array(T), news: new Float64Array(T) };
    let M = 0;
    for (let j = 1; j < T; j++) M += kf[j] + kb[j];
    const out = { e, comp, M, maxLoop: 0, failAt: null, failLoop: null, multiAt: [] };

    // Forecast path of felt experience on [t, T) for a given forecast of u, with news s at t.
    // Returns x0 (path with s = 0) and g (the path's response to a unit of news at t).
    function pathAt(t, uh) {
      const n = T - t, A = echoMatrix(kf, kb, n);
      const memPast = new Float64Array(n);
      const past = p.recursive ? e : fHist;
      for (let k = 0; k < n; k++) {
        let s = 0;
        for (let q = 0; q < t; q++) {
          const lag = k + 1 + q;
          if (lag < T) s += past[t - 1 - q] * kb[lag];
        }
        memPast[k] = s;
      }
      const x0 = new Float64Array(n), g = new Float64Array(n);
      if (p.recursive) {
        const IA = new Float64Array(n * n);
        for (let i = 0; i < n * n; i++) IA[i] = -A[i];
        for (let i = 0; i < n; i++) IA[i * n + i] += 1;
        const solve = luSolver(IA, n);
        if (!solve) return null;
        const rhs = new Float64Array(n);
        for (let i = 0; i < n; i++) rhs[i] = uh[t + i] + memPast[i];
        x0.set(solve(rhs));
        const e0 = new Float64Array(n); e0[0] = 1;
        g.set(solve(e0));
      } else {
        // Direct: x = (I + A) f + memory of past f; future news forecast as zero.
        for (let i = 0; i < n; i++) {
          let s = uh[t + i] + memPast[i];
          for (let j = 0; j < n; j++) s += A[i * n + j] * uh[t + j];
          x0[i] = s;
          g[i] = (i === 0 ? 1 : 0) + A[i * n + 0];
        }
      }
      return { x0, g };
    }

    let uPrev = forecastU(p, -1);
    let first = pathAt(0, uPrev);
    let xPrev = new Float64Array(T);
    if (first) xPrev.set(first.x0);

    for (let t = 0; t < T; t++) {
      const uh = forecastU(p, t), n = T - t;
      const pa = pathAt(t, uh);
      if (!pa) { out.failAt = t; break; }
      const { x0, g } = pa;
      let s = 0;
      if (p.over === "u") {
        for (let j = 0; j < n; j++) s += kn[j] * phi(uh[t + j] - uPrev[t + j]);
      } else {
        let loop = 0;
        for (let j = 0; j < n; j++) loop += kn[j] * Math.abs(g[j]);
        loop *= lam;
        out.maxLoop = Math.max(out.maxLoop, loop);
        const roots = newsRoots(x0, g, xPrev, t, kn, n, phi);
        if (roots.length === 0) { out.failAt = t; out.failLoop = loop; break; }
        if (roots.length > 1) out.multiAt.push(t);
        s = roots[roots.length - 1];   // the better felt state when there are two
      }
      const x = new Float64Array(n);
      for (let i = 0; i < n; i++) x[i] = x0[i] + s * g[i];
      e[t] = x[0];
      fHist[t] = uh[t] + s;
      comp.base[t] = uh[t];
      comp.news[t] = s;
      let ant = 0;
      if (p.recursive) for (let j = 1; j < n; j++) ant += kf[j] * x[j];
      else for (let j = 1; j < n; j++) ant += kf[j] * uh[t + j];
      comp.anticipation[t] = ant;
      comp.memory[t] = x[0] - uh[t] - s - ant;
      xPrev = new Float64Array(T); xPrev.set(x, t);
      uPrev = uh;
    }
    out.T = out.failAt == null ? T : out.failAt;
    let sum = 0;
    for (let t = 0; t < out.T; t++) sum += e[t];
    out.lifeSum = sum;
    return out;
  }

  const api = { simulate, forecastU };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.ConvModel = api;
})(typeof window !== "undefined" ? window : this);
