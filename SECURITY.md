## Security Policy

This project provides a reference implementation of Shamir Secret Sharing.

It does not store, transmit, or manage secrets beyond in-memory operations.
Security considerations are limited to correctness of the algorithm and
explicit failure semantics.

No vulnerability reporting process is defined at this stage.

## Security Notes

- No telemetry, no logging of secrets or shares
- Designed for offline use
- Deterministic error handling (no secret-dependent branches)
- Explicit memory zeroization where applicable
- No persistence beyond explicit user action

## Reporting
Security issues should be reported privately.
