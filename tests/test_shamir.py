import unittest

from shamir.core import split_secret, reconstruct_secret
from shamir.encoding import encode_shares, decode_shares
from shamir.exceptions import (
    InvalidThresholdError,
    InvalidShareCountError,
    InvalidSecretError,
    ReconstructionError,
    EncodingError,
)


class TestShamirSecretSharing(unittest.TestCase):

    def test_split_and_reconstruct(self):
        secret = 123456789
        shares = split_secret(secret, threshold=3, shares_count=5)

        recovered = reconstruct_secret(shares[:3])
        self.assertEqual(recovered, secret)

    def test_encoding_and_decoding(self):
        secret = 987654321
        shares = split_secret(secret, threshold=3, shares_count=5)

        encoded = encode_shares(shares)
        decoded = decode_shares(encoded)

        recovered = reconstruct_secret(decoded[:3])
        self.assertEqual(recovered, secret)

    def test_invalid_threshold(self):
        with self.assertRaises(InvalidThresholdError):
            split_secret(42, threshold=1, shares_count=5)

    def test_threshold_exceeds_share_count(self):
        with self.assertRaises(InvalidShareCountError):
            split_secret(42, threshold=6, shares_count=5)

    def test_invalid_secret_range(self):
        with self.assertRaises(InvalidSecretError):
            split_secret(-1, threshold=2, shares_count=3)

    def test_insufficient_shares_for_reconstruction(self):
        secret = 111
        shares = split_secret(secret, threshold=3, shares_count=5)

        with self.assertRaises(ReconstructionError):
            reconstruct_secret(shares[:1])

    def test_invalid_encoded_share(self):
        with self.assertRaises(EncodingError):
            decode_shares(["not-a-valid-share"])


if __name__ == "__main__":
    unittest.main()

