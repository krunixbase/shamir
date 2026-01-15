import pytest

from shamir.encoding import encode_share, decode_share
from shamir.errors import ShamirError


def test_encode_and_decode_roundtrip():
    share = (1, b"share-bytes")

    encoded = encode_share(share)
    decoded = decode_share(encoded)

    assert decoded == share


def test_encoded_share_is_bytes():
    share = (2, b"another-share")

    encoded = encode_share(share)

    assert isinstance(encoded, bytes)


def test_decode_rejects_invalid_input_type():
    with pytest.raises(ShamirError):
        decode_share("not-bytes")


def test_decode_rejects_corrupted_data():
    corrupted = b"invalid-encoded-share"

    with pytest.raises(ShamirError):
        decode_share(corrupted)


def test_encoding_is_deterministic():
    share = (3, b"deterministic-share")

    encoded_a = encode_share(share)
    encoded_b = encode_share(share)

    assert encoded_a == encoded_b
