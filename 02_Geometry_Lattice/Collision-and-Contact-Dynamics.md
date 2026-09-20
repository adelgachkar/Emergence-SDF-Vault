---
title: Collision and Contact Dynamics
created: 2026-09-17
tags:
  - sdf/geometry
  - sdf/lattice
  - sdf/collision
status: canonical-reviewed
license: CC-BY-4.0
zenodo_section: Lattice-Geometry
---

# Collision and Contact Dynamics

## 1. Hard-Core and Penetration Potential

In the discrete cellular substrate emerging from [[Vacuum-Foam-Boundary]], dense packings of tetrahedral elements ([[Minimal-Tetrahedral-Unit]]) exhibit finite-volume exclusion. The phenomenological contact potential between adjacent vertices $i$ and $j$ separated by distance $r_{ij}$ is defined by:

$$V_{\text{contact}}(r_{ij}) = \begin{cases} +\infty & r_{ij} \le a_0 \\ V_0 \exp\left(-\frac{r_{ij} - a_0}{\lambda_d}\right) & r_{ij} > a_0 \end{cases}$$

where:
- $a_0$: Effective hard-core boundary cut-off radius.
- $\lambda_d$: Characteristic spatial decay length of microscopic contact strain.
- $V_0$: Contact stiffness amplitude scale.

## 2. Dynamic Frustration and Berry Phase Ingestion

When external volumetric compression forces tetrahedral cells past their steric relaxation threshold, the microscopic collision dynamics converts mechanical stress into a discrete gauge potential via [[Discrete-Gauge-Connection]]. 

The steric hindrance around a fivefold quasi-axis cannot close without angular defect, feeding the geometric Berry phase:
$$\Delta \phi_{\text{Berry}} = \oint_{\mathcal{C}} \mathbf{A}_{\text{discrete}} \cdot d\boldsymbol{\ell}$$

This angular deficit is directed into the frustration loop formulated in [[Pentagonal-Frustration-BerryPhase]] and bounded numerically in [[Pentagonal-Frustration-Numerical-Coupling]].

## 3. Topological Stress Damping & Shielding

The contact energy does not diverge asymptotically into singular shockwaves; instead, it is absorbed by topological circulation and hysteresis loss, preventing unphysical singularities as formalized in [[Saturation-Singularity-Avoidance]].
