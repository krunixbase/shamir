from dataclasses import dataclass
from enum import Enum
from typing import Optional


class OperationStage(Enum):
    INITIALIZE = "initialize"
    SPLIT = "split"
    VERIFY = "verify"
    RECONSTRUCT = "reconstruct"


@dataclass(frozen=True)
class OperationContext:
    """
    Immutable operational context for Shamir secret sharing procedures.

    This context defines all parameters required to execute a single,
    auditable operation lifecycle without relying on hidden state.
    """

    session_id: str
    threshold: int
    total_shares: int
    algorithm_version: str
    dry_run: bool = False

    def validate(self) -> Optional[str]:
        """
        Perform basic structural validation of the context.

        Returns:
            None if the context is valid, otherwise a string error code.
        """
        if self.threshold <= 0:
            return "INVALID_THRESHOLD"

        if self.total_shares <= 0:
            return "INVALID_TOTAL_SHARES"

        if self.threshold > self.total_shares:
            return "THRESHOLD_EXCEEDS_TOTAL_SHARES"

        if not self.session_id:
            return "MISSING_SESSION_ID"

        if not self.algorithm_version:
            return "MISSING_ALGORITHM_VERSION"

        return None
