# Threat Model

This document describes the threat model for the Shamir Secret Sharing
implementation and its associated share serialization format.

The goal is to make explicit:
- what is protected
- what is not protected
- which assumptions are required for security

This document is descriptive, not prescriptive.

---

## Scope

This threat model applies to:
- the Shamir Secret Sharing algorithm implementation
- the share serialization format
- integrity mechanisms (CRC32, optional HMAC)

It does not cover:
- key management systems
- secure storage solutions
- transport security
- access control or authentication

---

## Assets

The primary asset is:
- the original secret provided to the Shamir split operation

Secondary assets include:
- individual shares
- metadata describing share parameters

---

## Trust Assumptions

Security relies on the following assumptions:

- fewer than `threshold` shares are compromised
- shares are stored or distributed independently
- the reconstruction threshold is chosen appropriately
- the implementation is used as specified

Violation of these assumptions may result in loss of confidentiality.

---

## Threats Considered

### Accidental Corruption

Examples:
- disk errors
- transmission errors
- partial file writes

Mitigation:
- mandatory CRC32 integrity checks
- strict format validation

---

### Active Tampering

Examples:
- modification of share contents
- substitution of share metadata

Mitigation:
- optional HMAC-SHA256 integrity verification
- explicit validation of all header fields

Note:
- HMAC requires an external key and is not part of the Shamir secret

---

### Share Loss

Examples:
- deletion of share files
- unavailable storage locations

Impact:
- permanent loss of the secret if fewer than `threshold` shares remain

Mitigation:
- operational redundancy
- careful selection of `share_count` and `threshold`

---

### Share Compromise

Examples:
- unauthorized access to individual shares

Impact:
- no information leakage unless `threshold` shares are compromised

Mitigation:
- inherent properties of Shamir Secret Sharing
- operational separation of shares

---

## Threats Explicitly Out of Scope

The following threats are not addressed by this project:

- confidentiality of individual shares at rest
- confidentiality during transport
- side-channel attacks
- malicious runtime environments
- compromised random number generators
- denial-of-service attacks

These concerns must be addressed by the surrounding system.

---

## Non-Goals

This project intentionally does not:
- encrypt share payloads
- hide reconstruction parameters
- attempt to detect all forms of malicious behavior
- replace secure storage or transport mechanisms

---

## Residual Risk

Correct use of this implementation reduces the risk of secret disclosure
under the stated assumptions. Residual risk remains if operational
controls fail or assumptions are violated.

Users are responsible for evaluating whether this threat model is
appropriate for their environment.
