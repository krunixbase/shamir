shamir
Reference-grade implementation of Shamir Secret Sharing with modular encoding and audit-ready structure.

## 🧭 Overview
This repository provides clean, dependency-free implementations of Shamir Secret Sharing (SSS) in both Python and Go, designed for correctness, clarity, and long-term maintainability.

The project focuses on:

✅ Explicit mathematical correctness

✅ Clear separation of responsibilities

✅ Deterministic behavior suitable for audits and integrations

## 🚀 Features
## Python
Pure Python implementation of Shamir Secret Sharing

Configurable threshold and share count

URL-safe Base64 encoding for share transport

Explicit exception hierarchy for safe integration

Deterministic and auditable unit tests

## Go
Modular share verification with audit-grade reporting

Deterministic error codes and structured context

CLI integration with human-readable and JSON output

No reconstruction logic — pure defensiveness

Integration-ready for CI and automated pipelines

## 🧠 Design Principles
Separation of concerns  
Cryptographic logic is isolated from encoding, I/O, and validation layers.

Explicit failure semantics  
All error conditions are represented by structured exceptions or error objects.

Audit-first structure  
Code is written to be readable, reviewable, and defensible — suitable for compliance and forensic use.


## Python Usage Example
python
from shamir.core import split_secret, reconstruct_secret
from shamir.encoding import encode_shares, decode_shares

secret = 123456789
shares = split_secret(secret, threshold=3, shares_count=5)

encoded = encode_shares(shares)
decoded = decode_shares(encoded)

recovered = reconstruct_secret(decoded[:3])
assert recovered == secret

## Go Module: Audit-Grade Share Verification (TOR A)
This repository also includes a reference-grade Go module for deterministic share verification, designed to audit Shamir Secret Sharing inputs before reconstruction.

Go API
go
report := verify.VerifyShares(shares, threshold)
Always returns a VerificationReport

Never panics, never reconstructs

Can be serialized to JSON for CI integration

CLI
bash
shamir verify shares.json --threshold 3
shamir verify shares.json --threshold 3 --json
Exit code 0 → valid and threshold satisfied

Exit code 1 → any critical error

## Dual Implementation Philosophy: Python & Go
This repository intentionally contains two parallel implementations of Shamir Secret Sharing, each serving a distinct purpose:

### Python — Protocol Reference
The Python module (shamir/) provides a full implementation of the Shamir Secret Sharing protocol:

- Splitting and reconstructing secrets

- Encoding and decoding shares

- Exception-safe API for integration

- Designed for clarity, correctness, and educational use

Python defines how the protocol works.

### Go — Defensive Verification (TOR A)
The Go modules (core/, math/, verify/, cli/) focus on verifying externally supplied shares:

- Modular validation of share structure and consistency

- Deterministic error reporting with stable codes

- Audit-grade VerificationReport for CI and forensic use

- CLI with human-readable and JSON output modes

Go defines how to defend against invalid or malicious input.

### Why Both?
Python expresses the cryptographic protocol clearly.

Go enforces structural discipline and auditability.

- Both follow the same principles:

- separation of concerns,

- deterministic behavior,

- explicit failure semantics.

Together, they form a system that is:

- understandable,

- verifiable,

- and resistant to misuse.


## Project Structure

```

shamir/
├── cli/            # Command-line interface adapters
│   ├── verify.go   # Verify command entry point
│   
├── core/           # Core Shamir Secret Sharing logic
│   ├── share.go    # Share structure definition
│   ├── polynomial.go # Polynomial operations
│   └── params.go   # Scheme parameters
│
├── docs/
│   └── operational_flow.md
│
├── math/           # Mathematical primitives
│   ├── field.go    # Abstract field interface
│   └── interpolate.go # Polynomial interpolation (Lagrange)
│
├── operations/    
│   ├── context.py
│   ├── lifecycle.py
│   ├── errors.py
│   └── verify.py
│
├── verify/         # Defensive share verification (TOR A)
│   ├── verify.go   # Verification orchestrator
│   ├── checks.go   # Modular validation checks
│   ├── report.go   # VerificationReport definition
│   └── errors.go   # Structured verification errors
│
├── tests/             # Integration tests
│   ├── test_shamir.py
│   ├── verify_test.go # VerifyShares integration tests
│   ├── test_split.py
│   ├── test_combine.py
│   ├── test_encoding.py
│   ├── test_cli.py        # CLI happy-path + error cases
│   └── vectors/
│       ├── README.md
│       ├── split_k2_n3.json
│       ├── split_k3_n5.json
│       └── encoding_v1.json
│
├── shamir/         # Python reference implementation
│   ├── core.py     # Shamir Secret Sharing logic
│   ├── encoding.py # Share serialization utilities
│   └── exceptions.py # Explicit exception hierarchy├─ THREAT_MODEL.md │
│
├── CHANGELOG.md
├── THREAT_MODEL.md
├── PR_JUSTIFICATION.md
├── DESIGN_DECISIONS.md
├── README.md       # Project documentation
├── LICENSE         # MIT license
├── SECURITY.md     # Security policy
└── .gitignore      # Git ignore rules

```
## License
This project is licensed under the MIT License. See LICENSE for details.

## Audit & Security
See SECURITY.md, THREAT_MODEL.md and PR_JUSTIFICATION.md
for design rationale and threat assumptions.

