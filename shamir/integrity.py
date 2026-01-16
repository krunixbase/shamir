"""
Integrity primitives for Shamir share serialization.

This module provides lightweight integrity mechanisms used by the
share format layer. It intentionally does not perform encryption
and does not depend on the cryptographic core.
"""

import zlib
import hmac
import hashlib
from typing import Optional


class IntegrityError(Exception):
    """Raised when integrity verification fails."""


def crc32(data: bytes) -> int:
    """
    Compute CRC32 checksum for given data.

    Used as a mandatory integrity check to detect accidental corruption.
    """
    return zlib.crc32(data) & 0xFFFFFFFF


def verify_crc32(data: bytes, expected: int) -> None:
    """
    Verify CRC32 checksum.

    Raises IntegrityError on mismatch.
    """
    actual = crc32(data)
    if actual != expected:
        raise IntegrityError("CRC32 mismatch")


def hmac_sha256(data: bytes, key: bytes) -> bytes:
    """
    Compute HMAC-SHA256 for given data and key.

    This is an optional integrity mechanism intended for environments
    where active tampering must be detected.
    """
    return hmac.new(key, data, hashlib.sha256).digest()


def verify_hmac_sha256(data: bytes, key: bytes, expected: bytes) -> None:
    """
    Verify HMAC-SHA256.

    Raises IntegrityError on mismatch.
    """
    actual = hmac_sha256(data, key)
    if not hmac.compare_digest(actual, expected):
        raise IntegrityError("HMAC verification failed")
