class ShamirError(Exception):
    """Base exception for Shamir Secret Sharing errors."""
    pass


class InvalidThresholdError(ShamirError):
    """Raised when threshold value is invalid."""
    pass


class InvalidShareCountError(ShamirError):
    """Raised when number of shares is invalid."""
    pass


class InvalidSecretError(ShamirError):
    """Raised when secret is outside the finite field."""
    pass


class ReconstructionError(ShamirError):
    """Raised when secret reconstruction fails."""
    pass


class EncodingError(ShamirError):
    """Raised when share encoding or decoding fails."""
    pass

