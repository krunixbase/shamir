from typing import List

from .context import OperationContext
from .errors import OperationError


def verify_shares(shares: List, context: OperationContext):
    """
    Perform procedural verification of Shamir shares.

    This function validates structural and contextual correctness of shares
    without performing cryptographic reconstruction.
    """

    if not shares:
        return OperationError.INSUFFICIENT_SHARES.value

    if len(shares) < context.threshold:
        return OperationError.INSUFFICIENT_SHARES.value

    seen = set()
    for share in shares:
        identifier = getattr(share, "id", None)
        session_id = getattr(share, "session_id", None)

        if identifier is None:
            return OperationError.CORRUPTED_INPUT.value

        if identifier in seen:
            return OperationError.DUPLICATE_SHARE.value

        seen.add(identifier)

        if session_id != context.session_id:
            return OperationError.SHARE_CONTEXT_MISMATCH.value

    return None
