# Changelog

All notable changes to this project are documented in this file.

The format follows a structured, factual approach intended
to support audit, review, and long-term maintenance.
No marketing language or forward-looking guarantees are used.

## [Unreleased]

### Added
- Explicit threat model documenting security assumptions and non-goals.
- SECURITY.md describing operational security boundaries.
- PR_JUSTIFICATION.md capturing design intent and scope.
- DESIGN_DECISIONS.md documenting architectural choices.
- README references to audit and security documentation.

### Changed
- Project documentation structure elevated to first-class artifacts
  located in the repository root.

### Security
- No functional security changes; documentation clarifies existing
  assumptions and operational boundaries.

## [0.1.0] – Initial reference implementation

### Added
- Core Shamir Secret Sharing implementation.
- Deterministic split and combine logic.
- Minimal, versioned share encoding.
- Test suite covering split, combine, and encoding behavior.

## v1.0.0-reference
- Initial operational lifecycle release
- Deterministic error handling
- Procedural control layer
- Audit-grade documentation
