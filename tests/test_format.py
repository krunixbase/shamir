import pytest

from shamir.format import (
    encode_share,
    decode_share,
    ShareHeader,
    ShareFormatError,
)
from shamir.integrity import IntegrityError


def make_header(k=3, n=5, i=1):
    return ShareHeader(
        threshold=k,
        share_count=n,
        share_index=i,
    )


def test_encode_decode_roundtrip():
    header = make_header()
    payload = b"test-payload"

    encoded = encode_share(header, payload)
    decoded_header, decoded_payload = decode_share(encoded)

    assert decoded_header == header
    assert decoded_payload == payload


def test_invalid_magic():
    header = make_header()
    payload = b"payload"
    encoded = encode_share(header, payload)

    corrupted = b"XXXX" + encoded[4:]
    with pytest.raises(ShareFormatError):
        decode_share(corrupted)


def test_invalid_version():
    header = make_header()
    payload = b"payload"
    encoded = encode_share(header, payload)

    corrupted = bytearray(encoded)
    corrupted[4] = 0xFF  # version byte
    with pytest.raises(ShareFormatError):
        decode_share(bytes(corrupted))


def test_invalid_threshold_share_count():
    header = ShareHeader(threshold=5, share_count=3, share_index=1)
    payload = b"payload"

    with pytest.raises(ShareFormatError):
        encode_share(header, payload)


def test_invalid_share_index():
    header = ShareHeader(threshold=2, share_count=3, share_index=0)
    payload = b"payload"

    with pytest.raises(ShareFormatError):
        encode_share(header, payload)


def test_empty_payload_rejected():
    header = make_header()

    with pytest.raises(ShareFormatError):
        encode_share(header, b"")


def test_crc_mismatch_detected():
    header = make_header()
    payload = b"payload"
    encoded = encode_share(header, payload)

    corrupted = bytearray(encoded)
    corrupted[-1] ^= 0xFF  # flip last byte

    with pytest.raises(IntegrityError):
        decode_share(bytes(corrupted))


def test_mac_roundtrip():
    header = make_header()
    payload = b"payload"
    key = b"mac-key"

    encoded = encode_share(header, payload, mac_key=key)
    decoded_header, decoded_payload = decode_share(encoded, mac_key=key)

    assert decoded_header == header
    assert decoded_payload == payload


def test_mac_mismatch_detected():
    header = make_header()
    payload = b"payload"
    encoded = encode_share(header, payload, mac_key=b"key-a")

    with pytest.raises(IntegrityError):
        decode_share(encoded, mac_key=b"key-b")
