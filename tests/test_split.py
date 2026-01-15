import pytest

from shamir.core import split
from shamir.errors import ShamirError


def test_split_produces_expected_number_of_shares():
    secret = b"super-secret"
    threshold = 3
    shares = 5

    result = split(secret=secret, threshold=threshold, shares=shares)

    assert len(result) == shares


def test_split_requires_threshold_less_or_equal_shares():
    secret = b"super-secret"

    with pytest.raises(ShamirError):
        split(secret=secret, threshold=5, shares=3)


def test_split_rejects_empty_secret():
    with pytest.raises(ShamirError):
        split(secret=b"", threshold=2, shares=3)


def test_split_is_deterministic_for_same_input_and_rng():
    secret = b"deterministic-secret"
    threshold = 2
    shares = 3

    result_a = split(secret=secret, threshold=threshold, shares=shares, seed=42)
    result_b = split(secret=secret, threshold=threshold, shares=shares, seed=42)

    assert result_a == result_b


def test_split_produces_distinct_shares():
    secret = b"unique-secret"
    threshold = 2
    shares = 4

    result = split(secret=secret, threshold=threshold, shares=shares)

    assert len(set(result)) == shares
