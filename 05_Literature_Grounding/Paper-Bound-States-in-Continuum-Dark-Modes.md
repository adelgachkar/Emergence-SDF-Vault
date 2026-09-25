---
title: "Bound States in the Continuum and Dark-Mode Energy Storage"
paper_id: "BIC-Dark-Modes-Storage"
created: 2026-09-20
tags:
  - literature/grounding
  - physics/bic
  - physics/dark-modes
  - sdf/tier2
  - bandgap-recycling
status: active
license: "MIT"
lang: "en"
zenodo_section: Literature-Grounding
---

# Literature Grounding: Bound States in the Continuum (BIC) & Dark Modes

## 1. Key Conceptual Anchors

* **Non-radiating states inside the continuum:** von Neumann & Wigner (1929) showed localized states can exist embedded in a continuous spectrum; modern photonics realizes them as **BICs** — perfectly confined modes that coexist with open radiation channels yet cannot leak.
* **Mechanisms:** symmetry-protected decoupling (polarization vorticity in momentum space) and Friedrich–Wintgen interference between resonances.
* **Energy signature:** zero radiative loss with finite internal circulation — the defining observable is suppressed radiation at real frequencies.

**References:** Hsu, Zhen, Stone, Joannopoulos & Soljačić, *Rev. Mod. Phys.* **88**, 015003 (2016), DOI: 10.1103/RevModPhys.88.015003; Hsu et al., *Nature* **499**, 188 (2013), DOI: 10.1038/nature12289; von Neumann & Wigner, *Phys. Z.* **30**, 467 (1929).

## 2. Cross-Vault Mappings to SDF Framework

* [[Bandgap-Phase-Recycling]]: SDF dark modes ($\nabla \cdot \mathbf{S}_{\text{rad}} = 0$ with $\mathbf{S}_{\text{reactive}} \neq 0$) are structurally BIC-like: energy circulation without radiation channels. The SDF bandgap window $\omega_{\text{lower}} < \omega < \omega_{\text{upper}}$ plays the role of the BIC continuum-separation condition.
* [[Topological-Knot-Soliton-Emergence]]: condensation of trapped reactive energy into topological structures parallels the use of high-Q BIC resonators to reach nonlinear/condensation thresholds with low input power.
* [[Kinetic-Stability-and-Dispersion]]: the anti-tachyonic stiffness bound is the dynamical-stability condition that keeps the trapped mode on the real-frequency axis.
* [[Radiative-Phase-Leak-and-Dissipation]]: BIC theory quantifies the *suppression* side of the leak/compensation balance that SDF states as $\mathcal{D}_i(\omega) \approx 0$.

## 3. Formal Bridge & Divergences

**Bridge:** both frameworks describe open systems whose eigenstates decouple from the radiating continuum; SDF's frustration loop supplies a *geometric* decoupling mechanism (5-fold holonomy deficit) analogous to symmetry protection. **Divergence:** BICs are linear wave phenomena with a fully developed theory (polarization vortices, Q scaling); SDF must reproduce these observables — e.g., a polarization-vortex signature of the frustrated loop — to claim equivalence rather than analogy.
