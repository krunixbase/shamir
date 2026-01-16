"""
Common exception hierarchy for the Shamir package.

This module defines explicit error types used across the codebase
to keep failure modes predictable, auditable, and easy to handle
by higher-level layers.
"""


class ShamirError(Exception):
    """
    Base exception for all Shamir-related errors.
    """


class ShareFormatError(ShamirError):
    """
    Raised when a serialized share is malformed, unsupported,
    or fails structural validation.
    """


class IntegrityError(ShamirError):
    """
    Raised when integrity verification fails (CRC or MAC).
    """


class ReconstructionError(ShamirError):
    """
    Raised when secret reconstruction fails due to insufficient
    or inconsistent shares.
    """
