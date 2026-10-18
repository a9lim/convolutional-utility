// Pathwise convolutional-utility model with felt news, linear in every channel. Port of
// formalism/pathwise.py at lam = 1, with biphasic memory (notes/adaptation.md): the memory kernel is
// m·μ^j − c·γ^j, afterglow minus adaptation. Recursive: echoes and news are about experienced
// utility (the canonical model). Direct: echoes of the felt base f = u + N, news about base utility.
// Deterministic announcements; certainty-equivalent forecasts.
(function (root) {
  "use strict";

  // Anticipation a·α^j, afterglow m·μ^j, adaptation c·γ^j, news k_n(j) = n·ν^j.
  function kernels(p) {
    const T = p.T;
    const kf = new Float64Array(T), kg = new Float64Array(T), kd = new Float64Array(T);
    const kb = new Float64Array(T), kn = new Float64Array(T);
    for (let j = 1; j < T; j++) {
      kf[j] = p.a * Math.pow(p.al, j);
      kg[j] = p.m * Math.pow(p.mu, j);
      kd[j] = p.c * Math.pow(p.ga, j);
      kb[j] = kg[j] - kd[j];
      kn[j] = p.n * Math.pow(p.nu, j);
    }
    kn[0] = p.n;
    return { kf, kg, kd, kb, kn };
  }

  // Forecast at time t of base utility on [0, T); t = -1 is the prior. An event adds its value to
  // each of its periods [at, at + dur). It is known from its announcement, or from its start if
  // unannounced; a cancellation drops the periods not yet lived.
  function forecastU(p, t) {
    const u = new Float64Array(p.T).fill(p.base);
    for (const ev of p.events) {
      if (!(ev.at <= t || (ev.announce != null && ev.announce <= t))) continue;
      const end = Math.min(p.T, ev.at + (ev.dur == null ? 1 : ev.dur));
      for (let s = Math.max(0, ev.at); s < end; s++) {
        if (ev.cancel != null && ev.cancel <= Math.min(t, s)) continue;
        u[s] += ev.value;
      }
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

  // Recursive echoes are well-founded for every lifespan iff 1 − K(z) has no zeros on the unit
  // circle and winding number zero; for a nonnegative kernel this is M < 1 (notes/adaptation.md).
  function echoSymbol(p) {
    const geo = (w, r, th) => {          // w r e^{iθ} / (1 − r e^{iθ})
      const nr = w * r * Math.cos(th), ni = w * r * Math.sin(th);
      const dr = 1 - r * Math.cos(th), di = -r * Math.sin(th), dd = dr * dr + di * di;
      return [(nr * dr + ni * di) / dd, (ni * dr - nr * di) / dd];
    };
    const N = 4096;
    let minAbs = Infinity, turn = 0, prev = null;
    for (let i = 0; i <= N; i++) {
      const th = (2 * Math.PI * i) / N;
      const f = geo(p.a, p.al, th), g = geo(p.m, p.mu, -th), d = geo(p.c, p.ga, -th);
      const re = 1 - (f[0] + g[0] - d[0]), im = -(f[1] + g[1] - d[1]);
      minAbs = Math.min(minAbs, Math.hypot(re, im));
      const arg = Math.atan2(im, re);
      if (prev != null) {
        let da = arg - prev;
        if (da > Math.PI) da -= 2 * Math.PI;
        if (da < -Math.PI) da += 2 * Math.PI;
        turn += da;
      }
      prev = arg;
    }
    return { minAbs, winding: Math.round(turn / (2 * Math.PI)) };
  }

  function simulate(p) {
    const T = p.T, rec = p.recursive, { kf, kg, kd, kb, kn } = kernels(p);
    const e = new Float64Array(T), f = new Float64Array(T);
    const past = rec ? e : f;
    const comp = { base: new Float64Array(T), anticipation: new Float64Array(T), afterglow: new Float64Array(T),
                   adaptation: new Float64Array(T), news: new Float64Array(T) };
    const A = (p.a * p.al) / (1 - p.al), G = (p.m * p.mu) / (1 - p.mu), h = (p.c * p.ga) / (1 - p.ga);
    const sym = echoSymbol(p);
    const out = { e, comp, A, G, h, M: A + G - h, wellFounded: sym.minAbs > 1e-6 && sym.winding === 0,
                  kappa: new Float64Array(T), unstableAt: [], failAt: null };

    // Forecast path of felt experience on [t, T) for a given forecast of u, with news s at t:
    // x0 is the path at s = 0 and g its response to a unit of news at t.
    function pathAt(t, uh) {
      const n = T - t, Am = echoMatrix(kf, kb, n);
      const memPast = new Float64Array(n);
      for (let k = 0; k < n; k++) {
        let s = 0;
        for (let q = 0; q < t; q++) {
          const lag = k + 1 + q;
          if (lag < T) s += past[t - 1 - q] * kb[lag];
        }
        memPast[k] = s;
      }
      const x0 = new Float64Array(n), g = new Float64Array(n);
      if (rec) {
        const IA = new Float64Array(n * n);
        for (let i = 0; i < n * n; i++) IA[i] = -Am[i];
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
          for (let j = 0; j < n; j++) s += Am[i * n + j] * uh[t + j];
          x0[i] = s;
          g[i] = (i === 0 ? 1 : 0) + Am[i * n];
        }
      }
      return { x0, g };
    }

    let uPrev = forecastU(p, -1);
    const first = pathAt(0, uPrev);
    let xPrev = new Float64Array(T);
    if (first) xPrev.set(first.x0);

    for (let t = 0; t < T; t++) {
      const uh = forecastU(p, t), n = T - t;
      const pa = pathAt(t, uh);
      if (!pa) { out.failAt = t; break; }
      const { x0, g } = pa;
      let s = 0;
      if (!rec) {
        for (let j = 0; j < n; j++) s += kn[j] * (uh[t + j] - uPrev[t + j]);
      } else {
        // s = k_n·(d + s g): the revision's direct news amplified by 1/(1 − κ), κ = k_n·g (N4).
        let kd0 = 0, kap = 0;
        for (let j = 0; j < n; j++) { kd0 += kn[j] * (x0[j] - xPrev[t + j]); kap += kn[j] * g[j]; }
        out.kappa[t] = kap;
        if (Math.abs(1 - kap) < 1e-12) {
          if (Math.abs(kd0) > 1e-12) { out.failAt = t; break; }
        } else s = kd0 / (1 - kap);
        if (kap >= 1) out.unstableAt.push(t);   // the felt state exists but is unstable, news felt backwards
      }
      const x = new Float64Array(n);
      for (let i = 0; i < n; i++) x[i] = x0[i] + s * g[i];
      e[t] = x[0];
      f[t] = uh[t] + s;
      comp.base[t] = uh[t];
      comp.news[t] = s;
      let ant = 0, glow = 0, adapt = 0;
      for (let j = 1; j < n; j++) ant += kf[j] * (rec ? x[j] : uh[t + j]);
      for (let j = 1; j <= t; j++) { glow += kg[j] * past[t - j]; adapt -= kd[j] * past[t - j]; }
      comp.anticipation[t] = ant;
      comp.afterglow[t] = glow;
      comp.adaptation[t] = adapt;
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
