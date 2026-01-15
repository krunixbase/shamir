# Reference Test Vectors

This directory contains static, versioned reference vectors
for the Shamir Secret Sharing implementation.

The files in this directory are treated as immutable artifacts.
They define expected behavior and data formats independently
of any specific implementation or runtime environment.

## Purpose

Reference vectors serve as:
- audit artifacts,
- regression anchors,
- cross-implementation validation data.

They are intended to be consumed by tests, reviewers,
and external implementations without modification.

## Design Principles

- No randomness.
- No runtime generation.
- No helper code.
- No implicit assumptions.

All values are explicitly encoded and documented.

## Contents

- `split_k2_n3.json` — reference split with threshold=2 and shares=3.
- `split_k3_n5.json` — reference split with threshold=3 and shares=5.
- `encoding_v1.json` — canonical share encoding specification.

## Stability Guarantees

Once published, reference vectors MUST NOT be changed.
Any incompatible change requires a new versioned file.

This directory is part of the project’s public contract.
