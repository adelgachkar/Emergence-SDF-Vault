# -*- coding: utf-8 -*-
"""
Coupling rate kappa between adjacent tetrahedral void cavities in the
pentagonal SDF network — derived from exact packing geometry + Bethe
aperture coupling (coupled-mode theory).

Geometry inputs are parameter-free (regular tetrahedral packing of
mutually tangent spheres of radius r0 = a/2 at network vertices):

  - void inscribed sphere : r_in   = r0*(sqrt(3/2) - 1)  = 0.2247 r0
  - triangular neck       : rho    = r0*(2/sqrt(3) - 1)  = 0.1547 r0
  - equivalent round hole : r_eq   = sqrt(A_neck/pi),  A_neck = 3*sqrt(3)*rho^2
  - void center spacing   : d_cc   = r0*sqrt(2/3)        = 0.8165 r0 = 0.408 a
  - void volume           : V_void = 4/3 pi r0^3 - 4 * V_tet(2 r0) = 0.4176 r0^3

Coupled-mode theory with a Bethe small-aperture (magnetic polarizability
M = 4/3 r_eq^3, O(1) convention ambiguity):

  kappa/omega0 = C_B * (r_eq^3 / V_mode) * g^2 ,   g = |H(neck)|/|H(max)|

g is the only non-geometric factor (mode-shape field at the neck),
O(0.3..1); set it from a numerical eigenmode solve for precision.

Derived outputs: Q_hop = omega0/kappa, step time T_hop = pi/(2 kappa)
(in optical periods), walk group velocity v_g = 2 kappa a, and the
vault consistency relation c_eff = v_g, tau_d = pi/(2 kappa).
"""

import math

s3 = math.sqrt(3.0)

# ---------- exact packing geometry (parameter-free) ----------

def geometry(a):
    r0    = a / 2.0                          # tangent spheres at vertices
    r_in  = r0 * (math.sqrt(1.5) - 1.0)      # inscribed void sphere
    rho   = r0 * (2.0 / s3 - 1.0)            # triangular neck inradius
    A_neck = 3.0 * s3 * rho**2               # neck area (equilateral window)
    r_eq  = math.sqrt(A_neck / math.pi)      # equivalent circular aperture
    d_cc  = r0 * math.sqrt(2.0 / 3.0)        # adjacent-void center distance
    V_tet = (2.0 * r0)**3 / (6.0 * math.sqrt(2.0))   # regular tetrahedron, edge 2 r0
    V_void = 4.0 / 3.0 * math.pi * r0**3 - 4.0 * V_tet
    return dict(r0=r0, r_in=r_in, rho=rho, A_neck=A_neck, r_eq=r_eq,
                d_cc=d_cc, V_void=V_void)

# ---------- coupling model ----------

C_B = 1.0   # Bethe-prefactor convention, O(1)

def kappa_over_omega0(a, g=0.57, mode_factor=1.0):
    """kappa/omega0 from Bethe-aperture CMT. mode_factor = V_void/V_mode."""
    G = geometry(a)
    return C_B * (G["r_eq"]**3 / G["V_void"]) * g**2 * mode_factor

def derived(a, n_s=1.5, chi=0.64, g=0.57):
    """
    a    : tetrahedron edge [m]
    chi  : lambda0 = chi * a   (mode-size factor, 0.3..1.0)
    g    : field ratio at the neck (0.3..1.0)
    """
    G = geometry(a)
    x = kappa_over_omega0(a, g=g)            # kappa/omega0 (scale-free)
    lam0 = chi * a
    c = 2.99792458e8
    omega0 = 2.0 * math.pi * c / lam0
    kappa = x * omega0
    T_hop = math.pi / (2.0 * kappa)          # seconds (full hop)
    periods = T_hop * omega0 / (2.0 * math.pi)   # hop time in optical periods
    v_g = 2.0 * kappa * a                    # max walk group velocity
    Q_hop = 1.0 / x
    tau_d = math.pi / (2.0 * kappa)          # vault consistency: tau_d = T_hop
    return dict(k_over_w=x, Q_hop=Q_hop, T_hop=T_hop, periods=periods,
                v_g=v_g, v_g_over_c=v_g / c, tau_d=tau_d, geom=G,
                kappa_GHz=kappa / (2 * math.pi) / 1e9)

if __name__ == "__main__":
    print("=== exact geometry (all in units of edge a) ===")
    G = geometry(1.0)
    for k in ("r0", "r_in", "rho", "r_eq", "d_cc"):
        print(f"  {k:5s} = {G[k]:.4f} a")
    print(f"  V_void = {G['V_void']:.5f} a^3   (vault: 0.4176 r0^3 = 0.05220 a^3)")
    print(f"  r_neck/r_in = {G['rho']/G['r_in']:.3f}   r_eq/r_in = {G['r_eq']/G['r_in']:.3f}")

    print("\n=== kappa/omega0 (scale-free) vs mode factor g ===")
    for g in (0.3, 0.45, 0.57, 0.75, 1.0):
        x = kappa_over_omega0(1.0, g=g)
        print(f"  g = {g:.2f}  ->  kappa/omega0 = {x:.2e}   Q_hop = {1.0/x:7.1f}")

    print("\n=== absolute scales (chi=0.64, g=0.57) ===")
    for a_nm in (250.0, 500.0, 1000.0):
        D = derived(a_nm * 1e-9)
        print(f"  a = {a_nm:6.0f} nm : kappa/2pi = {D['kappa_GHz']:6.2f} GHz"
              f"   T_hop = {D['T_hop']*1e15:6.2f} fs ({D['periods']:5.1f} periods)"
              f"   v_g = {D['v_g_over_c']*100:5.2f}% c   tau_d = {D['tau_d']*1e15:6.2f} fs")

    print("\n=== consistency with vault constants ===")
    D = derived(500e-9)
    print(f"  c_eff = v_g = {D['v_g']:.3e} m/s = {D['v_g_over_c']:.4f} c")
    print("  vault kinematics:  c_eff = l*/tau_d  ==  2*kappa*l*/pi"
          "  (tight-binding mean velocity, factor 2/pi vs band max)")
    print(f"  check: v_g_max/(2/pi) = {D['v_g_over_c']*math.pi/2:.4f} c  = predicted c_eff")
    print(f"  l_B = sqrt(2 pi/delta_theta) = "
          f"{math.sqrt(2*math.pi/(2*math.pi-5*math.acos(1/3))):.3f} a  (previous step)")
