# Shamir Secret Sharing

This repository provides a **minimal, deterministic implementation of
Shamir’s Secret Sharing scheme** over \(GF(256)\).

It focuses exclusively on the **cryptographic core**: splitting a secret
into shares and reconstructing it from a threshold subset. No operational,
procedural, or governance concerns are included.

---

## Command Line Interface

This repository includes a minimal command-line interface that acts as a
thin adapter over the Shamir core and share encoding layers.

The CLI performs direct data transformations and does not introduce any
operational logic, persistence, or policy enforcement.

---

### Overview

The CLI provides two commands:

- `split` — split a secret into threshold shares
- `combine` — reconstruct a secret from shares

All data is read from standard input and written to standard output.

---

### Split

Split a secret into `n` shares with threshold `k`.

bash
shamir split -k <threshold> -n <shares> < secret.bin

---

## Purpose

The purpose of this project is to:

- implement Shamir Secret Sharing correctly and transparently
- provide a small, auditable cryptographic primitive
- support deterministic testing and reproducibility
- serve as a building block for higher-level systems

This repository is **implementation-focused**, not a complete key
management solution.

---

## Scope

This project includes:

- arithmetic over \(GF(256)\)
- polynomial-based secret splitting
- Lagrange interpolation for reconstruction
- deterministic unit tests

It intentionally avoids all non-essential concerns.

---

## Non-Goals

This project does **not**:

- define operational procedures or lifecycle management
- handle custody, rotation, or revocation
- provide serialization or storage formats
- include CLI tools or services
- manage access control or authorization
- replace KMS, HSM, or secret management platforms

Operational governance is explicitly out of scope.

---

## Design Principles

This implementation prioritizes:

- correctness over convenience
- explicit behavior over implicit assumptions
- deterministic testing
- minimal surface area
- separation of cryptography from operations

---

## Relationship to Operational Layer

This repository is designed to be used alongside, but independent from,
the **Operational Layer for Threshold Secrets** specification:

https://github.com/krunixbase/operational-layer-for-threshold-secrets

That project defines governance, accountability, and lifecycle procedures.
This repository provides only the cryptographic primitive.

---

## Status

This repository implements the **core Shamir algorithm**.

The API and behavior are expected to remain stable, with future changes
being additive and deliberate.

