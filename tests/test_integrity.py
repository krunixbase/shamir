import pytest

from shamir.integrity import (
    crc32,
    verify_crc32,
    hmac_sha256,
    verify_hmac_sha256,
    IntegrityError,
)


def test_crc32_deterministic():
    data = b"test-data"
    assert crc32(data) == crc32(data)


def test_crc32_detects_corruption():
    data = b"test-data"
    checksum = crc32(data)

    corrupted = b"test-Data"
    with pytest.raises(IntegrityError):
        verify_crc32(corrupted, checksum)


def test_crc32_accepts_valid_data():
    data = b"test-data"
    checksum = crc32(data)

    verify_crc32(data, checksum)


def test_hmac_sha256_deterministic():
    data = b"test-data"
    key = b"secret-key"

    mac1 = hmac_sha256(data, key)
    mac2 = hmac_sha256(data, key)

    assert mac1 == mac2


def test_hmac_sha256_detects_wrong_key():
    data = b"test-data"
    mac = hmac_sha256(data, b"key-a")

    with pytest.raises(IntegrityError):
        verify_hmac_sha256(data, b"key-b", mac)


def test_hmac_sha256_detects_corruption():
    data = b"test-data"
    key = b"secret-key"
    mac = hmac_sha256(data, key)

    corrupted = b"test-Data"
    with pytest.raises(IntegrityError):
        verify_hmac_sha256(corrupted, key, mac)


def test_hmac_sha256_accepts_valid_data():
    data = b"test-data"
    key = b"secret-key"
    mac = hmac_sha256(data, key)

    verify_hmac_sha256(data, key, mac)
