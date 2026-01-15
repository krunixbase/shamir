# Threat Model — Shamir Secret Sharing

## Assets
- Secret material prior to splitting
- Individual shares
- Reconstruction threshold parameters

## Adversaries
- Passive observer with partial shares
- Insider with access to storage/logs
- Operator error during split/combine

## Assumptions
- Cryptographically secure RNG
- Offline execution environment
- No side-channel hardened hardware assumed

## Threats & Mitigations
- Share leakage → threshold security
- Metadata correlation → minimal, versioned encoding
- Operator error → deterministic validation & errors
- Memory residue → explicit zeroization

## Non-goals
- Active network adversaries
- Hardware fault injection
