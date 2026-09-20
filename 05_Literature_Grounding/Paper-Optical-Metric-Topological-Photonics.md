---
title: "Paper-Optical-Metric-Topological-Photonics"
aliases:
  - "Optical Metric Grounding"
  - "Synthetic Gauge Photonics References"
created: 2026-09-20
tags:
  - literature/grounding
  - optical-metric
  - topological-photonics
  - coupled-resonators
zenodo_section: "Literature-Grounding"
status: "active"
license: "CC-BY-4.0"
---

# Paper Grounding: Optical Metric, Synthetic Gauge and Stepping Photonics

This note indexes the established literature that grounds the optical-geodesics, synthetic-gauge and stepping chain of the vault ([[Optical-Stepping-Synthetic-Gauge]], [[Vacuum-Noise-Register-and-Ratchet]], [[Phase-Debt-Oscillator]]).

## 1. Key Conceptual Anchors

- **Gordon optical metric** — W. Gordon, *Ann. Phys. (Leipzig)* **377**, 421 (1923): rays in a stationary medium are null geodesics of $ds^2 = (c^2/n^2)dt^2 - d\vec x^{\,2}$; the basis for treating the $\tau_d$-field as a refractive-index field.
- **Transformation optics** — U. Leonhardt, *Science* **312**, 1777 (2006); J. B. Pendry, D. Schurig, D. R. Smith, *Science* **312**, 1780 (2006): any geometry (including disclination/cosmic-string deficits) is optically implementable; grounds the $\delta\theta$ kink prediction.
- **Harper–Hofstadter problem** — P. G. Harper, *Proc. Phys. Soc. A* **68**, 874 (1955); D. R. Hofstadter, *Phys. Rev. B* **14**, 2239 (1976): lattice with flux per plaquette; grounds $\ell_B = a\sqrt{2\pi/\delta\theta}$ and the lowest-band Chern number $C=1$ (one chiral edge mode).
- **Topological photonics** — F. D. M. Haldane, S. Raghu, *Phys. Rev. Lett.* **100**, 013904 (2008); M. C. Rechtsman *et al.*, *Nature* **496**, 196 (2013); L. Lu, J. D. Joannopoulos, M. Soljačić, *Nature Photonics* **8**, 821 (2014): one-way photonic modes robust to disorder.
- **Synthetic gauge fields for photons** — K. Fang *et al.*, *Nature Photonics* **6**, 682 (2012): engineered per-plaquette photon phase — the technological embodiment of the $\delta\theta$ flux.
- **Coupled-resonator optical waveguides (CROW)** — A. Yariv, Y. Xu, R. K. Lee, A. Scherer, *Opt. Lett.* **24**, 711 (1999): light steps hop-by-hop between defect cavities; the stepping clock $T_{\text{hop}} = \pi/2\kappa$.
- **Bethe aperture theory** — H. A. Bethe, *Phys. Rev.* **66**, 163 (1944): diffraction/coupling through small apertures, polarizability $M \propto r^3$; grounds the neck-coupling law $\kappa/\omega_0 = 0.025\,g^2$.
- **Kramers escape** — H. A. Kramers, *Physica* **7**, 284 (1940): noise as trigger over a barrier; grounds the trigger-vs-energy split and the 1.3% jitter of the debt cycle.
- **Rate-and-state friction** — J. H. Dieterich, *J. Geophys. Res.* **84**, 2161 (1979); A. Ruina, *J. Geophys. Res.* **88**, 10359 (1983): state-variable accumulation → instability → reset cycles; macroscopic analogue of the phase-debt oscillator.

## 2. Cross-Vault Mappings

- [[Optical-Stepping-Synthetic-Gauge]]: CROW stepping, Hofstadter flux $\delta\theta$, Bethe neck coupling, Gordon metric.
- [[Bandgap-Phase-Recycling]]: one-way chiral continuation of dark modes.
- [[Phase-Debt-Oscillator]]: Kramers-triggered relaxation cycle; rate-and-state analogue.
- [[Phase-Retuning-Piecewise-Laws]]: universality/crossover reading of retuned effective laws.

## 3. Formal Bridge and Divergences

What the vault borrows: the **structure** of the bounds and clocks (metric, flux, aperture scaling, escape statistics). What the vault must still add to be physics rather than analogy: (i) a numerical eigenmode solution fixing $g$ in $\kappa/\omega_0 = 0.025\,g^2$ — **partially done (2026-09-20): 2D FDTD proxy (`tools/cavity_pair_fdtd2d.py`) confirms the $w^3$-type splitting law and brackets $g \approx 0.7\text{–}0.9$; the decisive 3D run is `tools/meep_void_pair_3d.py`**; (ii) a field equation on the lattice showing the antiphase release channel at $\Phi = \pi$; (iii) an experiment separating seed from motor (pump-off test). Each is already stated as a falsifiable target in the mapped notes.

## 4. Reference Notes

All identifiers above are standard-literature citations verified against common bibliographic records; volume/page data should be re-verified against DOIs before external publication.
