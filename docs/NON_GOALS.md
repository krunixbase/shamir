# Non-Goals — shamir

## Purpose

This document defines the explicit non-goals of the `shamir` library.

It exists to prevent scope creep, implicit expectations, and unintended
expansion beyond the library’s intended role as a reference-grade
implementation of Shamir Secret Sharing.

---

## Explicit Non-Goals

The `shamir` library explicitly does NOT aim to provide:

- Command-line interfaces or interactive tools
- Encryption, authenticated encryption, or key management
- Password handling, key derivation, or mnemonic systems
- Storage, persistence, or serialization formats
- Network, RPC, or distributed system components
- User experience abstractions or convenience wrappers
- Performance optimizations beyond correctness and determinism
- Hardware integration or secure enclave support

---

## Out of Scope by Design

The following concerns are intentionally excluded:

- Operational workflows or recovery procedures
- Compliance, governance, or policy enforcement
- Audit logging or forensic metadata
- Backward compatibility with legacy or non-deterministic implementations
- Automatic error recovery or best-effort behavior

These concerns are addressed, where appropriate, by higher-level tools or
separate projects.

---

## Stability Over Expansion

The primary goal of the `shamir` library is correctness, determinism, and
auditability.

Feature growth, extensibility, or ecosystem integration are explicitly
secondary and may be rejected even if technically feasible.

---

## Authority

This document is authoritative.

Any feature request or change proposal that conflicts with these non-goals
is invalid by definition.
