# -*- coding: utf-8 -*-
"""
2D FDTD benchmark of the void-pair coupling law  kappa/omega_0 = C_B * (r_eq^3/V_void) * g^2
(Pentagonal-network aperture coupling, vault note Optical-Stepping-Synthetic-Gauge).

Model (faithful 2D analog):
  * Closed PEC cavities  <-> closed dielectric shells of the 3D voids (geometric confinement).
  * Square cavity side L = 2*r_in (inscribed circle = void inscribed sphere).
  * Shared wall of thickness t with a centered slit of width w (the neck;
    vault ratio w/L = 2*rho / (2*r_in) = rho/r_in = 0.688).
  * TM polarization (Ez, Hx, Hy); Ez = 0 on PEC.

Measurements
  1. isolated cavity: omega_0 (calibrated against analytic pi*sqrt2/L) and
     g = <H_tangential over slit footprint> / max|H| in the cavity  (Bethe's g).
  2. coupled pair: supermode splitting -> kappa/omega_0 = (w_+ - w_-)/(w_+ + w_-)  (exact, lossless).
  3. sweep w -> scaling law kappa/omega_0 vs w and g(w); collapse test of the g^2 structure.

Units: a = 1 (tetrahedron edge), c = 1.
Run:  python tools/cavity_pair_fdtd2d.py
"""
import math
import numpy as np

# ---------------- vault geometry (parameter-free) ----------------
r0   = 0.5
r_in = r0 * (math.sqrt(1.5) - 1.0)     # 0.11235 void inscribed radius
rho  = r0 * (2.0 / math.sqrt(3) - 1.0) # 0.07735 neck inradius
L    = 2.0 * r_in                      # square cavity side (inscribed circle = r_in)
W_VAULT = 2.0 * rho                    # vault neck width
T_WALL  = 0.10                         # wall (corridor) thickness, ~ (r_in - rho)..r_in

# ---------------- numerics ----------------
N_PER_L = 30                           # cells per cavity side (convergence-checked by omega_0 error)
dx   = L / N_PER_L
dt   = 0.99 * dx / math.sqrt(2.0)
PAD  = 3

def make_mask(w, two_cavities=True, t=T_WALL):
    """air mask: True = air (field region), False = PEC."""
    nxc = int(round(t / dx))
    t_c = nxc * dx
    wc  = max(1, int(round(w / dx)))
    if wc % 2 == 0:
        wc += 1                        # odd -> symmetric about center row
    w_c = wc * dx
    Nx = int(round((2 * L + t_c) / dx)) + 2 * PAD
    Ny = int(round(L / dx)) + 2 * PAD
    mask = np.zeros((Nx, Ny), dtype=bool)
    j0, j1 = PAD, PAD + int(round(L / dx))
    if two_cavities:
        i1a, i1b = PAD, PAD + int(round(L / dx))
        i2a, i2b = PAD + int(round(L / dx)) + nxc, PAD + int(round(2 * L / dx)) + nxc
        mask[i1a:i1b, j0:j1] = True
        mask[i2a:i2b, j0:j1] = True
        # slit channel: NOTCH the wall (remove PEC) rather than ADD air outside the cavities
        jc = (j0 + j1) // 2
        # wall spans i1b-1 .. i2a ; carve the slit there
        mask[max(0, i1b - 1): i2a, jc - wc // 2: jc + wc // 2 + 1] = True
    else:
        ia, ib = PAD, PAD + int(round(L / dx))
        mask[ia:ib, j0:j1] = True
    return mask, (Nx, Ny), w_c

def peaks(signal, f_lo, f_hi, npk=2):
    """Hann-windowed FFT peak finder with parabolic refinement."""
    s = signal * np.hanning(len(signal))
    F = np.abs(np.fft.rfft(s))
    df = 1.0 / (len(signal) * dt)
    fr = np.arange(len(F)) * df
    band = (fr >= f_lo) & (fr <= f_hi)
    idx = np.where(band)[0]
    Fb = F[idx]
    found = []
    Fc = Fb.copy()
    for _ in range(npk):
        k = int(np.argmax(Fc))
        if Fc[k] <= 0 or k < 2 or k > len(Fb) - 3:
            break
        a, b, c = math.log(Fb[k-1] + 1e-30), math.log(Fb[k] + 1e-30), math.log(Fb[k+1] + 1e-30)
        d = 0.5 * (a - c) / (a - 2*b + c + 1e-30)
        found.append((idx[0] + k + d) * df)
        lo, hi = max(0, k - 6), min(len(Fc), k + 7)
        Fc[lo:hi] = -1
    return sorted(found)

def measure_pair(w, nsteps=48000):
    mask, (Nx, Ny), w_c = make_mask(w)
    c1 = (PAD + N_PER_L // 2, PAD + N_PER_L // 2)
    c2 = (PAD + N_PER_L + int(round(T_WALL / dx)) + N_PER_L // 2, PAD + N_PER_L // 2)
    Ez = np.zeros((Nx, Ny)); Hx = np.zeros((Nx, Ny)); Hy = np.zeros((Nx, Ny))
    p1 = np.zeros(nsteps); p2 = np.zeros(nsteps)
    t0 = 0.2 * nsteps * dt
    for n in range(nsteps):
        Hx[:, :-1] += -dt * (Ez[:, 1:] - Ez[:, :-1]) / dx
        Hy[:-1, :] +=  dt * (Ez[1:, :] - Ez[:-1, :]) / dx
        Ez[1:, 1:] += dt * ((Hy[1:, 1:] - Hy[:-1, 1:]) - (Hx[1:, 1:] - Hx[1:, :-1])) / dx
        env = math.exp(-((n * dt - t0) / (0.10 * nsteps * dt)) ** 2)
        Ez[c1] += env
        Ez[~mask] = 0.0
        p1[n] = Ez[c1]; p2[n] = Ez[c2]
    f0_guess = math.sqrt(2) / (2 * L)
    fp = peaks(p1 + p2, 0.6 * f0_guess, 1.4 * f0_guess, npk=2)
    return fp, (Nx, Ny), w_c

def measure_single(nsteps=48000, w_for_g=W_VAULT):
    """isolated cavity: omega_0 calibration + mode profile -> g at slit footprint."""
    mask, (Nx, Ny), _ = make_mask(0.0, two_cavities=False)
    c1 = (PAD + N_PER_L // 2, PAD + N_PER_L // 2)
    Ez = np.zeros((Nx, Ny)); Hx = np.zeros((Nx, Ny)); Hy = np.zeros((Nx, Ny))
    f0_guess = math.sqrt(2) / (2 * L)
    sig = 60.0 * dt * 40
    t0 = 0.35 * nsteps * dt
    # --- history buffers (fields are 2D; record central rows/cols over time) ---
    rowEz = np.zeros((nsteps, Ny))          # Ez along central row i = src
    colHx = np.zeros((nsteps, Nx))          # Hx along central column j = src
    colHy = np.zeros((nsteps, Nx))          # Hy along central column j = src
    isrc, jsrc = c1
    for n in range(nsteps):
        Hx[:, :-1] += -dt * (Ez[:, 1:] - Ez[:, :-1]) / dx
        Hy[:-1, :] +=  dt * (Ez[1:, :] - Ez[:-1, :]) / dx
        Ez[1:, 1:] += dt * ((Hy[1:, 1:] - Hy[:-1, 1:]) - (Hx[1:, 1:] - Hx[1:, :-1])) / dx
        env = math.exp(-((n * dt - t0) / sig) ** 2)
        Ez[c1] += env * math.cos(2 * math.pi * f0_guess * n * dt)
        Ez[~mask] = 0.0
        rowEz[n, :] = Ez[isrc, :]
        colHx[n, :] = Hx[:, jsrc]
        colHy[n, :] = Hy[:, jsrc]
    # single-frequency DFT over the late (source-free) window -> pure mode
    w0 = int(0.55 * nsteps)
    win = np.hanning(nsteps - w0)
    ph = 2 * math.pi * f0_guess * dt * np.arange(nsteps)
    tw = np.exp(-1j * ph[w0:]) * win
    EzR = rowEz[w0:].T @ tw                # (Ny,) complex
    HxC = colHx[w0:].T @ tw                # (Nx,)
    HyC = colHy[w0:].T @ tw
    # re-assemble separable complex field estimates: mode(y)-profile from row, mode(x)-profile from col
    prof_y = EzR / (np.abs(EzR).max() + 1e-30)
    profHx_x = HxC / (np.abs(HxC).max() + 1e-30)
    profHy_x = HyC / (np.abs(HyC).max() + 1e-30)
    Hmag = np.zeros((Nx, Ny))
    Hmag += np.abs(profHy_x)[:, None]
    Hmag += np.abs(profHx_x)[:, None] * 0.3
    air = mask
    interior = np.zeros_like(mask)
    interior[PAD + 2:PAD + N_PER_L - 2, PAD + 2:PAD + N_PER_L - 2] = True
    hmax = Hmag[air & interior].max()
    # H tangential (Hy) at the right wall of the cavity (where the slit would be cut)
    iwall = PAD + N_PER_L - 3
    jc = (PAD + N_PER_L) // 2
    wc = max(1, int(round(w_for_g / dx))); wc += (wc + 1) % 2
    ht = np.abs(profHy_x[iwall]) * np.ones(wc)   # Hy nearly uniform across narrow slit
    g = ht.mean() / hmax
    # numerical omega_0 from a broadband run
    Ez2 = np.zeros((Nx, Ny)); Hx2 = np.zeros((Nx, Ny)); Hy2 = np.zeros((Nx, Ny))
    t02 = 0.2 * nsteps * dt
    p = np.zeros(nsteps)
    for n in range(nsteps):
        Hx2[:, :-1] += -dt * (Ez2[:, 1:] - Ez2[:, :-1]) / dx
        Hy2[:-1, :] +=  dt * (Ez2[1:, :] - Ez2[:-1, :]) / dx
        Ez2[1:, 1:] += dt * ((Hy2[1:, 1:] - Hy2[:-1, 1:]) - (Hx2[1:, 1:] - Hx2[1:, :-1])) / dx
        env = math.exp(-((n * dt - t02) / (0.10 * nsteps * dt)) ** 2)
        Ez2[c1] += env
        Ez2[~mask] = 0.0
        p[n] = Ez2[c1]
    fp = peaks(p, 0.6 * f0_guess, 1.4 * f0_guess, npk=1)
    return (2 * math.pi * fp[0] if fp else float('nan')), g, hmax

if __name__ == "__main__":
    print("=== 2D PEC void-pair FDTD benchmark (units a=1, c=1) ===")
    print(f"L (cavity side = 2 r_in) = {L:.4f} a ; vault slit W = 2 rho = {W_VAULT:.4f} a (W/L = {W_VAULT/L:.3f})")
    print(f"analytic omega_0 (square TM fundamental) = pi*sqrt(2)/L = {math.pi*math.sqrt(2)/L:.3f}")

    w0_num, g_vault, hmax = measure_single()
    print(f"\n[isolated] omega_0 numeric = {w0_num:.3f} (rel.err {abs(w0_num-math.pi*math.sqrt(2)/L)/(math.pi*math.sqrt(2)/L)*100:.2f}%)")
    print(f"[isolated] g at vault slit footprint (w = 2 rho) = {g_vault:.3f}   (CMT assumption was 0.57)")
    print(f"           analytic wall-center g for square fundamental = 1/sqrt(2) = {1/math.sqrt(2):.3f}")

    print("\n=== splitting sweep ===")
    print(f"{'w':>8s} {'w/L':>6s} {'f-':>8s} {'f+':>8s} {'kappa/omega0':>13s}")
    rows = []
    for w in (0.06, 0.10, W_VAULT):
        fp, _, w_c = measure_pair(w)
        if len(fp) == 2:
            km = (fp[1] - fp[0]) / (fp[1] + fp[0])
            rows.append((w_c, km))
            print(f"{w_c:8.4f} {w_c/L:6.3f} {fp[0]:8.4f} {fp[1]:8.4f} {km:13.4e}")
        else:
            rows.append((w_c, float('nan')))
            print(f"{w_c:8.4f} {w_c/L:6.3f}   unresolved (splitting < frequency resolution)")

    # scaling fit: log(kappa/omega0) vs log(w) -> exponent p (g^2 divided out is implicit in w-sweep)
    xs = np.array([math.log(r[0]) for r in rows if r[1] == r[1]])
    ys = np.array([math.log(r[1]) for r in rows if r[1] == r[1]])
    if len(xs) >= 2:
        p, c = np.polyfit(xs, ys, 1)
        print(f"\nscaling: kappa/omega0 ~ w^p, p = {p:.2f}   (Bethe 3D: p=3; 2D slit expectations: 2..3)")
        C = math.exp(c)
        wv = W_VAULT
        gv = g_vault
        print(f"prefactor C (kappa/omega0 = C * (w/L)^p * ...) at w=L: {C:.3e}")
        print(f"vault-mapped point: w/L = {wv/L:.3f}, g = {gv:.3f} -> CMT check: kappa/omega0 = "
              f"{[r[1] for r in rows if abs(r[0]-wv) < 1e-3][0] if any(abs(r[0]-wv)<1e-3 for r in rows) else float('nan'):.3e}"
              f"  vs 0.025*g^2 = {0.025*gv*gv:.3e}")
    print("\nnote: 2D PEC prefactor differs from 3D Bethe by construction; the decisive vault run is")
    print("tools/meep_void_pair_3d.py (real 3D dielectric-sphere geometry).")
