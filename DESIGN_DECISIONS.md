# Design Decisions

## Encoding
- Versioned share format
- Minimal metadata
- Forward-compatible parsing

## Errors
- Deterministic, typed errors
- No panic paths during normal operation

## CLI
- Explicit flags
- No interactive prompts
- STDIN/STDOUT friendly

## Cryptography
- Standard Shamir over finite fields
- No custom primitives
