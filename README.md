# shamir

Reference-grade implementation of Shamir Secret Sharing with modular encoding
and audit-ready structure.

## Overview

This repository provides a clean, dependency-free implementation of
Shamir Secret Sharing (SSS), designed for correctness, clarity, and
long-term maintainability.

The project focuses on:
- explicit mathematical correctness,
- clear separation of responsibilities,
- deterministic behavior suitable for audits and integrations.

## Features

- Pure Python implementation of Shamir Secret Sharing
- Configurable threshold and share count
- URL-safe Base64 encoding for share transport
- Explicit exception hierarchy for safe integration
- Deterministic and auditable unit tests

## Design Principles

- **Separation of concerns**  
  Core cryptographic logic is isolated from encoding and I/O layers.

- **Explicit failure semantics**  
  All error conditions are represented by dedicated exception classes.

- **Audit-first structure**  
  Code is written to be readable, reviewable, and defensible.

## Project Structure

```
shamir/
├── shamir/
│   ├── core.py         # Shamir Secret Sharing logic
│   ├── encoding.py     # Share serialization utilities
│   └── exceptions.py   # Explicit error definitions
├── tests/
│   └── test_shamir.py
└── README.md
```

## Usage Example

```python
from shamir.core import split_secret, reconstruct_secret
from shamir.encoding import encode_shares, decode_shares

secret = 123456789
shares = split_secret(secret, threshold=3, shares_count=5)

encoded = encode_shares(shares)
decoded = decode_shares(encoded)

recovered = reconstruct_secret(decoded[:3])
assert recovered == secret
