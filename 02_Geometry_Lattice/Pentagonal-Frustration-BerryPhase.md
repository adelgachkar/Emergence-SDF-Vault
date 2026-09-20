---
title: Pentagonal Frustration Berry Phase
created: 2026-09-17
tags:
  - sdf/geometry
  - sdf/topology
  - sdf/berry-phase
status: canonical
license: CC-BY-4.0
zenodo_section: Lattice-Geometry
---

# Pentagonal Frustration and Induced Berry Phase

## Angular Gap and Holonomy

The angular gap $\delta_\theta = 2\pi - 5\arccos(1/3) \approx 0.128388\text{ rad}$ induces anholonomy when parallel-transporting spatial frames across five contiguous tetrahedral faces:

$$\gamma_B = \oint_{\mathcal{C}_5} \mathbf{A}_{\text{discrete}} \cdot d\mathbf{l} = \iint_{\mathcal{S}} \mathbf{F} \cdot d\mathbf{S} \neq 0$$

## Gauge Field Ingestion

Through the [[Discrete-Gauge-Connection]], the geometric deficit is converted into an effective connection 1-form. The frustrated loop functions as a topological phase accumulator, as detailed in [[Pentagonal-Frustration-Numerical-Coupling]].

The macroscopic stabilization of this topological singularity is grounded in established synthetic-gauge and optical-metric theory ([[Paper-Optical-Metric-Topological-Photonics]]: Harper–Hofstadter flux, lowest-band Chern number $C=1$, Gordon metric), ensuring robust coarse-graining into the continuum action.

- One-way (chiral) continuation: [[Bandgap-Phase-Recycling]], [[Optical-Stepping-Synthetic-Gauge]].
- The earlier anchoring to arXiv:2309.12847 has been withdrawn — that source addresses electromagnetic angular-momentum transfer and does not support discrete gauge-connection dynamics (see verification note in [[Paper-2309.12847v1]]).
