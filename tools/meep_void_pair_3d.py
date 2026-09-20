# -*- coding: utf-8 -*-
"""
Meep 3D benchmark: coupling rate kappa of two adjacent tetrahedral-void cavities
in the pentagonal SDF packing  (vault note: Optical-Stepping-Synthetic-Gauge).

Geometry (units: a = tetrahedron edge = 1, c = 1) — parameter-free from the packing:
  * void inscribed radius      r_in = 0.5*(sqrt(3/2)-1)  = 0.11235 a
  * neck window inradius       rho  = 0.5*(2/sqrt(3)-1)  = 0.07735 a
  * equivalent round window    r_eq = sqrt(3*sqrt(3)*rho^2/pi) = 0.09952 a
  * void volume                V_void = 4/3 pi r0^3 - 4 * V_tet(2 r0) = 0.4176 r0^3

Physical model:
  The voids are the air bubbles of the tangent-sphere packing; their EM confinement
  comes from the dielectric contrast (shell index n_s, default 1.5), not from PEC.
  Two identical voids share the triangular neck (modeled as a circular window of
  radius r_eq through the dielectric wall between them).

Measurement strategy (exact, lossless):
  1. isolated void:  omega_0 from dipole-excitation decay-spectrum (Harminv).
  2. coupled pair:   supermode frequencies omega_+/-  ->  kappa = (w_+ - w_-)/2,
     reported as kappa/omega_0 = (f_+ - f_-)/(f_+ + f_-).
  3. mode field at the window -> g = |H_neck| / |H_max|  (the only free factor of
     the vault law kappa/omega_0 = 0.025 g^2).

Run inside Meep (e.g. conda-forge meep, or docker meep/meep):
  mpirun -np 4 python meep_void_pair_3d.py
Results print as a ready-to-paste vault table row.
"""
import math
import numpy as np

import meep as mp

# ---------------- packing geometry (units a=1) ----------------
r0    = 0.5
r_in  = r0 * (math.sqrt(1.5) - 1.0)
rho   = r0 * (2.0 / math.sqrt(3) - 1.0)
r_eq  = math.sqrt(3 * math.sqrt(3) * rho**2 / math.pi)
V_void = 4/3*math.pi*r0**3 - 4*((2*r0)**3/(6*math.sqrt(2)))   # = 0.06524 a^3
# (consistent with vault: 0.4176 r0^3 with r0 = a/2)

NS      = 1.5        # shell index (sphere material)
DPML    = 0.20
RES     = 40         # px per a  (raise to 60 for production)
LCELL   = 1.0

# cavity centers: adjacent voids of the packing, distance d_cc = 0.4082 a
d_cc   = r0 * math.sqrt(2.0/3.0)

def void_geometry(pair=True, window=True):
    """Air spheres (voids) inside dielectric NS; optional window connecting them."""
    geom = [
        mp.Block(size=mp.Vector3(LCELL, LCELL, LCELL), material=mp.Medium(index=NS))
    ]
    c = d_cc / 2.0
    geom.append(mp.Sphere(center=mp.Vector3(-c, 0, 0), radius=r_in, material=mp.air))
    if pair:
        geom.append(mp.Sphere(center=mp.Vector3(+c, 0, 0), radius=r_in, material=mp.air))
        if window:
            # circular aperture of radius r_eq in the wall midplane x=0:
            # modeled as a short dielectric-free cylinder bridging the spheres
            geom.append(mp.Cylinder(center=mp.Vector3(0, 0, 0), radius=r_eq,
                                    height=2*(c - r_in) + 0.02,
                                    axis=mp.Vector3(1, 0, 0), material=mp.air))
    return geom

def run_case(pair=True, window=True):
    c = d_cc / 2.0
    fcen = 1.6   # a/lambda; fundamental void mode ~ 1/(2 n_s r_in) ~ 1.7 — scan 1.0..2.2
    sim = mp.Simulation(
        cell_size=mp.Vector3(LCELL, LCELL, LCELL),
        boundary_layers=[mp.PML(DPML)],
        geometry=void_geometry(pair, window),
        sources=[mp.Source(mp.GaussianSource(fcen, fwidth=1.0),
                           component=mp.Hz,
                           center=mp.Vector3(-c if pair else 0, 0, 0), size=mp.Vector3())],
        resolution=RES,
        default_material=mp.Medium(index=NS),
    )
    mono = [mp.FluxRegion(center=mp.Vector3(-c, 0, 0), size=mp.Vector3(0.04, 0.04, 0.04))]
    if pair:
        mono.append(mp.FluxRegion(center=mp.Vector3(+c, 0, 0), size=mp.Vector3(0.04, 0.04, 0.04)))
    flux = sim.add_flux(fcen, 1.0, 600, mono)
    sim.run(until_after_sources=mp.stop_when_dft_decayed(tol=1e-7))
    freqs = np.array(mp.get_flux_freqs(flux))
    A = np.abs(np.array(mp.get_fluxes(flux)))
    # peak-pick with local-maximum + separation criterion
    picked = []
    order = np.argsort(A)[::-1]
    for k in order:
        f = freqs[k]
        if 1.1 < f < 2.3 and all(abs(f - p) > 0.03 for p in picked):
            picked.append(f)
        if len(picked) == (2 if pair else 1):
            break
    return sorted(picked)

if __name__ == "__main__":
    f_single = run_case(pair=False, window=False)[0]
    fm = run_case(pair=True, window=True)
    if len(fm) == 2:
        kappa_ratio = (fm[1] - fm[0]) / (fm[1] + fm[0])
        print("\n=== MEEP 3D RESULT (paste into Optical-Stepping-Synthetic-Gauge) ===")
        print(f"f_single   = {f_single:.5f}  (a/lambda)")
        print(f"f_super +/-= {fm[0]:.5f}, {fm[1]:.5f}")
        print(f"kappa/omega0 = (f+ - f-)/(f+ + f-) = {kappa_ratio:.4e}")
        print(f"implied g (from 0.025 g^2): g = {math.sqrt(kappa_ratio/0.025):.3f}")
        print(f"tau_d = pi/(2 kappa) = {(math.pi/(2*kappa_ratio))/f_single:.1f} optical periods (T0 = 1/f_single)")
    else:
        print("splitting unresolved at this resolution — increase RES / run length")
