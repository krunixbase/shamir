
Version numbers communicate compatibility guarantees and MUST be interpreted
strictly.

---

## Patch Releases (x.y.Z)

Patch releases MAY include:
- Bug fixes that do not alter documented behavior
- Internal refactoring with no observable API impact
- Documentation corrections

Patch releases MUST NOT:
- Change public API behavior
- Modify failure semantics
- Introduce new public interfaces

---

## Minor Releases (x.Y.z)

Minor releases MAY include:
- Additive public API extensions
- New functionality that does not break existing contracts

Minor releases MUST:
- Preserve all existing API behavior
- Maintain deterministic and fail-closed semantics

Minor releases MUST NOT:
- Remove or alter existing public interfaces
- Change documented guarantees

---

## Major Releases (X.y.z)

A major version increment is REQUIRED for any change that:
- Breaks the public API contract
- Alters documented behavior or failure semantics
- Changes cryptographic assumptions or arithmetic behavior
- Violates guarantees defined in `API_CONTRACT.md`

Major releases represent a deliberate and explicit evolution of the library.

---

## Contract Authority

The following documents are authoritative for compatibility decisions:

- `API_CONTRACT.md`
- `NON_GOALS.md`
- `DESIGN_DECISIONS.md`

Any change conflicting with these documents mandates a major version increment.

---

## Stability Commitment

The primary objective of the `shamir` library is long-term stability and
predictability.

Version increments are expected to be infrequent and deliberate. Feature growth
is secondary to correctness, determinism, and auditability.

---

## Authority

This document is the authoritative reference for versioning and compatibility
policy in the `shamir` library.

Any assumptions beyond what is stated here are invalid.
