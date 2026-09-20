---
title: "Radiation Q Bounds (Chu–Harrington) and Reactive Storage"
paper_id: "Chu-Harrington-Antenna-Q-Bounds"
created: 2026-09-20
tags:
  - literature/grounding
  - physics/antenna-theory
  - physics/reactive-energy
  - sdf/tier2
  - radiative-leakage
status: active
license: CC-BY-4.0
zenodo_section: Literature-Grounding
---

# Literature Grounding: Chu–Harrington Radiation Q Bounds

## 1. Key Conceptual Anchors

* **Stored reactive vs. radiated power (Chu, 1948):** For any antenna of radius $a$, the ratio of non-radiating (reactive) energy to radiated power per radian — the radiation $Q$ — has a hard lower bound:
  $$Q_{\text{rad}} = \frac{\omega W_{\text{reactive}}}{P_{\text{rad}}} \;\ge\; \frac{1}{(ka)^3} \quad (ka \ll 1)$$
  with refinements and exact spherical-mode formulations by Harrington (1959) and Collin–Rothschild.
* **Near/far-field decomposition:** The far field carries $P_{\text{rad}} \sim 1/r^2$, while the near field stores reactive energy and transfers angular momentum (SAM/OAM) without net power flow — the canonical decomposition matching the $S_r \sim 1/r^2$, $S_\varphi \sim 1/r^3$ split in SDF.
* **Dispersion-bound connection:** Yaghjian & Best (2005) and subsequent work tie $Q$ to frequency derivatives of the stored energy, the same Kramers–Kronig logic SDF uses for its delay bound.

**References:** Chu, *J. Appl. Phys.* **19**, 1163 (1948), DOI: 10.1063/1.1695040; Harrington, *J. Res. NBS* **64D**, 1 (1959); Yaghjian & Best, *IEEE Trans. Antennas Propag.* **53**, 714 (2005).

## 2. Cross-Vault Mappings to SDF Framework

* [[Radiative-Phase-Leak-and-Dissipation]]: the $S_r/S_\varphi$ leakage split is exactly the Chu near/far decomposition; the compensation condition $\mathcal{D}_i(\omega) \approx 0$ is a network balance of stored vs. leaked reactive energy.
* [[Hysteresis-Cost-TimeDelay]]: $W_{\text{reactive}}$ (Chu) ↔ reactive phase-debt storage (SDF); both bound reorganization latency through dispersion relations.
* [[Bandgap-Phase-Recycling]]: in the small-loop limit ($ka \ll 1$), $Q \to \infty$ forces radiation suppression — the classical mechanism that SDF reinterprets as dark-mode formation inside the bandgap.
* [[Pentagonal-Frustration-Numerical-Coupling]]: the five-tetrahedral loop plays the role of the electrically small radiator; $\ell^*$ is its effective $a$.

## 3. Formal Bridge & Divergences

SDF can state a direct analog: $Q_{\text{SDF}} \equiv \omega \, \mathcal{E}_{\text{reactive}}^{\text{loop}} / P_{\text{leak}}$, bounded below by loop geometry. **What SDF adds:** the stored energy is not passive near-field energy but topological Berry-phase debt with a rearrangement latency $\tau_d$, giving the new bound $\tau_d \ge (1/\Delta\omega)\,\partial\theta_{\text{Berry}}/\partial\omega$. **What is borrowed:** the bound structure itself is classical antenna theory, not new physics.
