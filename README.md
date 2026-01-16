# Shamir

Reference implementation of Shamir Secret Sharing with a
versioned, auditable share serialization format.

This project focuses on correctness, explicitness, and long-term
maintainability rather than feature completeness.

---

## Overview

The repository provides:

- a clean implementation of Shamir Secret Sharing
- a self-describing binary format for serialized shares
- deterministic integrity mechanisms
- cross-language interoperability (Python and Go)
- formal documentation of assumptions and non-goals

The cryptographic core is intentionally separated from
representation, storage, and transport concerns.

---

## Design Principles

- explicit over implicit
- validation before use
- minimal surface area
- no hidden state
- no security theater

Every component has a single, well-defined responsibility.

---

## Components

### Cryptographic Core

Pure implementation of the Shamir Secret Sharing algorithm.

- no I/O
- no serialization
- no integrity logic
- deterministic behavior

### Share Format

A versioned binary format for individual shares.

- self-describing header
- explicit reconstruction parameters
- mandatory CRC32 integrity check
- optional HMAC-SHA256 for tamper detection

See: `docs/share-format.md`

### Integrity Primitives

Lightweight helpers for detecting corruption and manipulation.

- CRC32 (mandatory)
- HMAC-SHA256 (optional)

### CLI

Minimal command-line interface for splitting and reconstructing secrets.

- explicit inputs and outputs
- no interactive prompts
- no implicit defaults

---

## Interoperability

The share format is implemented in:

- Python (reference implementation)
- Go (independent parser and encoder)

Deterministic test vectors ensure compatibility across languages.

---

## Security Model

This project does not provide confidentiality for individual shares.

Security relies on:

- the mathematical properties of Shamir Secret Sharing
- operational separation of shares
- correct selection of threshold parameters

See: `docs/threat-model.md`

---

## Non-Goals

This project intentionally does not:

- encrypt share payloads
- manage keys or secrets
- provide secure storage or transport
- implement access control
- hide reconstruction parameters

These concerns must be handled by the surrounding system.

---

## Status

The implementation is complete and stable.

The format, tests, and documentation are intended to remain
backward-compatible and auditable over time.
