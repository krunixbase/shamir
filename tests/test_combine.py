import pytest

from shamir.core import split, combine
from shamir.errors import ShamirError


def test_combine_reconstructs_original_secret():
    secret = b"super-secret"
    threshold = 3
    shares = 5

    all_shares = split(secret=secret, threshold=threshold, shares=shares)
    recovered = combine(shares=all_shares[:threshold], threshold=threshold)

    assert recovered == secret


def test_combine_requires_at_least_threshold_shares():
    secret = b"super-secret"
    threshold = 3
    shares = 5

    all_shares = split(secret=secret, threshold=threshold, shares=shares)

    with pytest.raises(ShamirError):
        combine(shares=all_shares[: threshold - 1], threshold=threshold)


def test_combine_rejects_empty_share_list():
    with pytest.raises(ShamirError):
        combine(shares=[], threshold=2)


def test_combine_is_deterministic_for_same_input():
    secret = b"deterministic-secret"
    threshold = 2
    shares = 3

    all_shares = split(secret=secret, threshold=threshold, shares=shares, seed=123)

    result_a = combine(shares=all_shares[:threshold], threshold=threshold)
    result_b = combine(shares=all_shares[:threshold], threshold=threshold)

    assert result_a == result_b


def test_combine_rejects_mismatched_threshold():
    secret = b"super-secret"
    threshold = 3
    shares = 5

    all_shares = split(secret=secret, threshold=threshold, shares=shares)

    with pytest.raises(ShamirError):
        combine(shares=all_shares[:threshold], threshold=threshold + 1)
