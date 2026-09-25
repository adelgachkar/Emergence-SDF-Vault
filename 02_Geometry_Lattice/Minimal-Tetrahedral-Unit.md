---
title: Minimal Tetrahedral Unit
created: 2026-09-17
tags:
  - sdf/geometry
  - sdf/lattice
status: canonical
license: "MIT"
lang: "en"
zenodo_section: Lattice-Geometry
---

# Minimal Tetrahedral Unit (MTU)

The fundamental spatial simplex in the SDF cellular complex is the regular tetrahedron $\Delta_3$, emerging from the statistical limit of voids ([[Statistical-Void-Limit]]).

## Geometric Invariants

- Vertices: $V = 4$
- Edges: $E = 6$
- Faces: $F = 4$
- Dihedral angle: $\theta_d = \arccos(1/3) \approx 70.528779^\circ$

## Fivefold Incompatibility and Packing

Five regular tetrahedra sharing a common hinge edge subtend an aggregate dihedral angle of:
$$\Sigma \theta = 5 \times \arccos(1/3) \approx 352.643897^\circ \neq 360^\circ$$

The resulting angular deficit $\delta_\theta \approx 7.356105^\circ$ forms the structural root of pentagonal frustration, detailed in [[Pentagonal-Frustration-BerryPhase]] and quantified in [[Pentagonal-Frustration-Numerical-Coupling]].

When adjacent MTUs undergo volumetric strain or close packing, their interactions are mediated through steric exclusion governed by [[Collision-and-Contact-Dynamics]], which couples structural distortion directly to the [[Discrete-Gauge-Connection]].
