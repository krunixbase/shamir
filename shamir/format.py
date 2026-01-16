"""
Share serialization format for Shamir Secret Sharing.

This module defines a versioned, self-describing binary format
for individual shares. It is intentionally separated from the
cryptographic core to keep mathematical operations independent
from representation, storage, and transport concerns.
"""

import struct
import zlib
import hmac
import hashlib
from dataclasses import dataclass
from typing import Optional


MAGIC = b"SHAM"
VERSION = 0x01

FIELD_GF256 = 0x01


class ShareFormatError(Exception):
    """Raised when a serialized share is invalid or malformed."""


@dataclass(frozen=True)
class ShareHeader:
    threshold: int
    share_count: int
    share_index: int
    field_id: int = FIELD_GF256

    def validate(self) -> None:
        if not (1 <= self.threshold <= self.share_count):
            raise ShareFormatError("Invalid threshold/share_count combination")
        if not (1 <= self.share_index <= self.share_count):
            raise ShareFormatError("Invalid share index")
        if self.field_id != FIELD_GF256:
            raise ShareFormatError("Unsupported field identifier")


_HEADER_STRUCT = struct.Struct(">4sBBBBB")
# magic, version, k, n, i, field_id


def encode_share(
    header: ShareHeader,
    payload: bytes,
    mac_key: Optional[bytes] = None,
) -> bytes:
    """
    Encode a single share into a binary representation.

    Integrity is always protected by CRC32.
    If mac_key is provided, an HMAC-SHA256 is appended.
    """
    header.validate()

    if not payload:
        raise ShareFormatError("Empty payload")

    header_bytes = _HEADER_STRUCT.pack(
        MAGIC,
        VERSION,
        header.threshold,
        header.share_count,
        header.share_index,
        header.field_id,
    )

    body = header_bytes + payload
    crc = zlib.crc32(body) & 0xFFFFFFFF
    encoded = body + struct.pack(">I", crc)

    if mac_key is not None:
        mac = hmac.new(mac_key, encoded, hashlib.sha256).digest()
        encoded += mac

    return encoded


def decode_share(
    data: bytes,
    mac_key: Optional[bytes] = None,
) -> tuple[ShareHeader, bytes]:
    """
    Decode and validate a serialized share.

    Verifies magic, version, structural constraints,
    CRC32 integrity, and optional HMAC.
    """
    if len(data) < _HEADER_STRUCT.size + 4:
        raise ShareFormatError("Data too short")

    header_part = data[: _HEADER_STRUCT.size]
    magic, version, k, n, i, field_id = _HEADER_STRUCT.unpack(header_part)

    if magic != MAGIC:
        raise ShareFormatError("Invalid magic value")
    if version != VERSION:
        raise ShareFormatError("Unsupported format version")

    header = ShareHeader(
        threshold=k,
        share_count=n,
        share_index=i,
        field_id=field_id,
    )
    header.validate()

    mac_len = hashlib.sha256().digest_size if mac_key else 0
    payload_end = len(data) - 4 - mac_len

    payload = data[_HEADER_STRUCT.size : payload_end]
    if not payload:
        raise ShareFormatError("Empty payload")

    expected_crc = struct.unpack(">I", data[payload_end : payload_end + 4])[0]
    actual_crc = zlib.crc32(data[:payload_end]) & 0xFFFFFFFF
    if actual_crc != expected_crc:
        raise ShareFormatError("CRC mismatch")

    if mac_key is not None:
        expected_mac = data[-mac_len:]
        actual_mac = hmac.new(
            mac_key,
            data[:-mac_len],
            hashlib.sha256,
        ).digest()
        if not hmac.compare_digest(actual_mac, expected_mac):
            raise ShareFormatError("MAC verification failed")

    return header, payload
