# -*- coding: utf-8 -*-
"""Test the CDME DOCX hypothesis:  log10(m) ~ a + b * log10(k_eff)

Three operational definitions of k_eff for Standard Model particles:

  Plan A (DOCX):   k_eff = winding/homotopy number assigned in the document
                   (leptons k=1, proton k=3, ...). Very few distinct values,
                   near-zero information content.
  Plan B (Gen):    k_eff = generation index n (1,2,3) within each charge family.
  Plan C (khat):   k_eff = khat(m) = ceil((m / m_e)^(1/4))  -- the smallest
                   integer k such that a naive Skyrme-type scaling
                   m ~ C * k^4 (with C fixed by the electron) can reach m.
                   Single calibrated parameter, applied to ALL masses.

Data: PDG 2024 masses (MeV/c^2), lepton masses exact to PDG precision.
"""
import numpy as np

# ---------------- PDG 2024 data (MeV) ----------------
PARTICLES = [
    # name,        mass_MeV,     family,  gen,  k_docx,  k_hat
    ("e",          0.51099895,   "lepton", 1, 1, 1),
    ("mu",       105.6583755,    "lepton", 2, 1, 4),
    ("tau",     1776.86,         "lepton", 3, 1, 8),
    ("u",         2.16,          "quark",  1, 1, 2),
    ("d",         4.67,          "quark",  1, 1, 2),
    ("s",        93.5,           "quark",  2, 1, 4),
    ("c",      1273.0,           "quark",  2, 1, 7),
    ("b",      4183.0,           "quark",  3, 1, 9),
    ("t",     172760.0,          "quark",  3, 1, 23),
    ("p(proton)", 938.272,       "baryon", 1, 3, 7),
    ("W",       80433.5,         "gauge",  1, 1, 20),
    ("Z",       91193.9,         "gauge",  1, 1, 21),
    ("Higgs",  125250.0,         "gauge",  1, 1, 23),
]
NAMES   = [p[0] for p in PARTICLES]
M       = np.array([p[1] for p in PARTICLES])
FAMILY  = [p[2] for p in PARTICLES]
GEN     = np.array([p[3] for p in PARTICLES], float)
K_DOCX  = np.array([p[4] for p in PARTICLES], float)
KHAT    = np.array([p[5] for p in PARTICLES], float)

def powerlaw_fit(k, m):
    """log10(m) = a + b*log10(k)  -> returns a, b, m_hat, R2, s, AIC"""
    x = np.log10(k); y = np.log10(m)
    b, a = np.polyfit(x, y, 1)
    yhat = a + b * x
    resid = y - yhat
    ss_res = float(np.sum(resid**2)); ss_tot = float(np.sum((y - y.mean())**2))
    r2 = 1 - ss_res / ss_tot
    n = len(y); s = np.sqrt(ss_res / n)
    aic = n * np.log(ss_res / n) + 2 * 2  # 2 params
    return a, b, 10**yhat, r2, s, aic

def exponential_fit(k, m):
    """log10(m) = a + b*k"""
    x = np.asarray(k, float); y = np.log10(m)
    b, a = np.polyfit(x, y, 1)
    yhat = a + b * x
    resid = y - yhat
    ss_res = float(np.sum(resid**2)); ss_tot = float(np.sum((y - y.mean())**2))
    r2 = 1 - ss_res / ss_tot
    n = len(y); s = np.sqrt(ss_res / n)
    aic = n * np.log(ss_res / n) + 2 * 2
    return a, b, 10**yhat, r2, s, aic

def structural_ceiling(y):
    """R2 an a+bx line can possibly reach on log10(m) given the targets x."""
    y = np.asarray(y, float)
    ss_tot = float(np.sum((y - y.mean())**2))
    # best possible: monotone ordering already perfect -> use rank-perfect line
    order = np.argsort(y)
    x_sorted = np.linspace(0, 1, len(y))
    y_sorted = y[order]
    ss_res = float(np.sum((y_sorted - np.linspace(y_sorted[0], y_sorted[-1], len(y_sorted)))**2))
    return 1 - ss_res / ss_tot

def report(tag, k, res, masses, names):
    a, b, mhat, r2, s, aic = res
    print(f"\n--- {tag} ---")
    print(f"  fit:  log10(m) = {a:.3f} + {b:.3f} * log10(k_eff)")
    print(f"  R2 = {r2:.4f}   s (resid std, dex) = {s:.3f}   AIC = {aic:.1f}")
    print(f"  worst offenders:")
    ratio_err = np.abs(np.log10(mhat) - np.log10(masses))
    idx = np.argsort(-ratio_err)[:4]
    for i in idx:
        print(f"    {names[i]:9s}  m={masses[i]:>10.2f} MeV   pred={mhat[i]:>10.2f} MeV   err={10**ratio_err[i]:>7.1f}x")

print("=" * 72)
print("HYPOTHESIS: log10(m) = a + b*log10(k_eff)   [PDG 2024 masses]")
print("=" * 72)

y = np.log10(M)
print(f"\nStructural ceiling for ANY 2-parameter linear predictor on this target: R2_max ~ {structural_ceiling(y):.3f}")

# Plan A
resA = powerlaw_fit(K_DOCX, M)
report("PLAN A: k_eff = DOCX assignment (1,1,1,1,1,1,1,1,1,3,1,1,1)", K_DOCX, resA, M, NAMES)
# note: degenerate x -> polyfit on constant x is ill-defined except via the single k=3 point
print("  NOTE: only 2 distinct k values (1 and 3) -> model has NO information to")
print("        distinguish e/mu/tau/W/Z/Higgs/top (all k=1, masses span 5.4 dex).")

# Plan B
resB = powerlaw_fit(GEN, M)
report("PLAN B: k_eff = generation index (1..3)", GEN, resB, M, NAMES)
resB2 = exponential_fit(GEN, M)
report("PLAN B': log10(m) = a + b*gen  (geometric in generation)", GEN, resB2, M, NAMES)

# Plan C
resC = powerlaw_fit(KHAT, M)
report("PLAN C: k_eff = khat = ceil((m/m_e)^(1/4))  [single-parameter calibration]", KHAT, resC, M, NAMES)
resC2 = exponential_fit(KHAT, M)
report("PLAN C': log10(m) = a + b*khat", KHAT, resC2, M, NAMES)

# Plan C restricted: exclude the calibration anchor (electron) to test predictive (not descriptive) power
mask = np.array([n != "e" for n in NAMES])
resC3 = powerlaw_fit(KHAT[mask], M[mask])
report("PLAN C'' (honest out-of-sample, electron excluded from fit):", KHAT[mask], resC3, M[mask], [n for n in NAMES if n != 'e'])

print("\n" + "=" * 72)
print("BASELINE COMPARISON (no topology at all):")
r2_order = 1 - np.var(np.log10(M)[1:] - np.log10(M)[:-1]) / np.var(np.log10(M))
print(f"  naive 'generation/geometric ladder' R2 on same 13 points already: see Plan B' above")
print(f"  spread of log10(m) itself: {np.log10(M).min():.2f} .. {np.log10(M).max():.2f} dex")
print("=" * 72)
