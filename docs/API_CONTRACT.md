# API Contract — shamir

## Scope

This document defines the normative public API contract for the `shamir`
library.

It specifies which interfaces are considered stable, the guarantees they
provide, and the constraints governing their evolution.

Any behavior not explicitly documented here is considered internal and
subject to change.

---

## Public API Definition

The public API consists exclusively of the following elements:

- Deterministic Shamir Secret Sharing split functionality
- Deterministic Shamir Secret Sharing recovery functionality
- Explicit parameter validation and failure signaling

All public functions MUST:
- Operate deterministically for identical inputs
- Reject invalid parameters explicitly
- Fail closed on any inconsistency or misuse

---

## Determinism Guarantees

For a given set of valid inputs, the library MUST produce identical outputs
across executions and environments.

No hidden randomness, implicit state, or environmental dependency is permitted
within the public API.

---

## Error Handling and Failure Semantics

The public API is explicitly fail-closed.

Failures include, but are not limited to:
- Invalid threshold or share count parameters
- Duplicate or inconsistent share indices
- Insufficient shares for recovery
- Corrupted or malformed share data

Partial recovery, best-effort behavior, or silent error handling is forbidden.

All failures MUST be signaled explicitly via documented exceptions or error
returns.

---

## Cryptographic Guarantees

The library implements Shamir Secret Sharing over GF(256).

The following properties are guaranteed:
- Finite field arithmetic over GF(256)
- Deterministic polynomial construction
- No embedded encryption, storage, or transport mechanisms

Cryptographic parameters and arithmetic behavior are fixed and documented.

---

## Non-Goals

The public API explicitly does NOT provide:
- Encryption or authenticated encryption
- Key derivation or password handling
- Storage, persistence, or serialization formats
- Network, CLI, or user interface components

Such functionality is intentionally out of scope.

---

## Compatibility and Versioning

The public API follows semantic versioning.

- Patch releases MAY fix bugs without altering documented behavior
- Minor releases MAY add new public interfaces without breaking existing ones
- Major releases are REQUIRED for any change that breaks this contract

Any change violating this document mandates a major version increment.

---

## Authority

This document is the authoritative definition of the public API contract for
the `shamir` library.

Any assumptions beyond what is stated here are invalid.
