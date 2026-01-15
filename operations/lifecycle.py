from typing import List, Tuple, Optional

from .context import OperationContext, OperationStage
from .errors import OperationError
from .verify import verify_shares


class OperationResult:
    """
    Deterministic result of a single operational stage.
    """

    def __init__(
        self,
        stage: OperationStage,
        success: bool,
        error_code: Optional[str] = None,
        message: Optional[str] = None,
    ):
        self.stage = stage
        self.success = success
        self.error_code = error_code
        self.message = message


def initialize(context: OperationContext) -> OperationResult:
    """
    Initialize and validate an operational context.
    """
    error = context.validate()
    if error:
        return OperationResult(
            stage=OperationStage.INITIALIZE,
            success=False,
            error_code=error,
            message="Context validation failed",
        )

    return OperationResult(
        stage=OperationStage.INITIALIZE,
        success=True,
        message="Context initialized successfully",
    )


def split(
    secret: bytes,
    context: OperationContext,
    splitter,
) -> Tuple[OperationResult, Optional[List]]:
    """
    Split a secret into shares using the provided splitter implementation.
    """
    if context.dry_run:
        return (
            OperationResult(
                stage=OperationStage.SPLIT,
                success=False,
                error_code="DRY_RUN_ACTIVE",
                message="Split skipped due to dry-run mode",
            ),
            None,
        )

    try:
        shares = splitter(
            secret,
            context.threshold,
            context.total_shares,
        )
    except Exception:
        return (
            OperationResult(
                stage=OperationStage.SPLIT,
                success=False,
                error_code="SPLIT_FAILED",
                message="Secret splitting failed",
            ),
            None,
        )

    return (
        OperationResult(
            stage=OperationStage.SPLIT,
            success=True,
            message="Secret split successfully",
        ),
        shares,
    )


def verify(
    shares: List,
    context: OperationContext,
) -> OperationResult:
    """
    Verify structural and procedural correctness of shares.
    """
    error = verify_shares(shares, context)
    if error:
        return OperationResult(
            stage=OperationStage.VERIFY,
            success=False,
            error_code=error,
            message="Share verification failed",
        )

    return OperationResult(
        stage=OperationStage.VERIFY,
        success=True,
        message="Shares verified successfully",
    )


def reconstruct(
    shares: List,
    context: OperationContext,
    reconstructor,
) -> Tuple[OperationResult, Optional[bytes]]:
    """
    Reconstruct a secret from verified shares.
    """
    verification = verify(shares, context)
    if not verification.success:
        return verification, None

    try:
        secret = reconstructor(shares)
    except Exception:
        return (
            OperationResult(
                stage=OperationStage.RECONSTRUCT,
                success=False,
                error_code="RECONSTRUCTION_FAILED",
                message="Secret reconstruction failed",
            ),
            None,
        )

    return (
        OperationResult(
            stage=OperationStage.RECONSTRUCT,
            success=True,
            message="Secret reconstructed successfully",
        ),
        secret,
    )
