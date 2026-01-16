# Shamir Share Serialization Format

This document defines the canonical binary format used to serialize
individual Shamir Secret Sharing (SSS) shares.

The format is designed to be:
- self-describing
- versioned
- deterministic
- language-agnostic
- auditable

It intentionally separates mathematical correctness from representation,
storage, and transport concerns.

---

## Design Goals

The share format MUST:
- allow validation before use
- support future extensions without breaking compatibility
- avoid implicit assumptions or hidden state
- not weaken the security properties of Shamir Secret Sharing

The format MUST NOT:
- encrypt share payloads
- hide parameters required for reconstruction
- introduce additional secrecy beyond the SSS algorithm itself

---

## Binary Layout

Each serialized share consists of three parts:

+----------------+----------------+----------------+
| Header         | Payload        | Integrity     |
+----------------+----------------+----------------+

All multi-byte values are encoded in big-endian order.

---

## Header

The header has a fixed size and is encoded as follows:

| Field        | Size | Description                              |
|--------------|------|------------------------------------------|
| magic        | 4    | ASCII string "SHAM"                      |
| version      | 1    | Format version (currently 0x01)          |
| threshold    | 1    | Reconstruction threshold (k)             |
| share_count  | 1    | Total number of shares (n)               |
| share_index  | 1    | Index of this share (1..n)               |
| field_id     | 1    | Finite field identifier                  |

### Field Identifiers

| Value | Meaning   |
|-------|-----------|
| 0x01  | GF(256)   |

---

## Payload

The payload contains the raw share data produced by the Shamir algorithm.

Properties:
- variable length
- no padding
- no compression
- no encryption

The payload is treated as opaque binary data by the format layer.

---

## Integrity

### CRC32 (Mandatory)

A CRC32 checksum (IEEE polynomial) is appended after the payload.

The checksum is computed over:

header || payload


This mechanism detects accidental corruption during storage or transport.

### HMAC-SHA256 (Optional)

An optional HMAC-SHA256 may be appended after the CRC32 value.

Properties:
- computed over `header || payload || crc32`
- requires an external key
- not part of the Shamir secret

This mechanism is intended for environments where active tampering must
be detected.

---

## Validation Rules

A serialized share MUST be rejected if:
- the magic value does not match
- the version is unsupported
- `threshold > share_count`
- `share_index` is outside the range `1..share_count`
- the payload is empty
- the CRC32 checksum does not match
- the HMAC verification fails (if enabled)

---

## Versioning

The `version` field defines the interpretation of the entire format.

Implementations MUST reject unknown versions unless explicitly designed
to support forward compatibility.

---

## Security Considerations

This format does not provide confidentiality.

Security relies entirely on:
- the mathematical properties of Shamir Secret Sharing
- operational separation of shares
- optional external integrity mechanisms

Loss or compromise of individual shares does not reveal the secret
unless the reconstruction threshold is met.

---

## Interoperability

This specification is implemented by:
- the Python reference implementation
- the Go reference implementation

Deterministic test vectors are provided to ensure cross-language
compatibility.
