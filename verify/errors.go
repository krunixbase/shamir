type ErrorCode string

type VerificationError struct {
    Code    ErrorCode
    Message string
    Context map[string]interface{}
}

const (
    ErrDuplicateShareID      ErrorCode = "ERR_DUPLICATE_SHARE_ID"
    ErrInconsistentField     ErrorCode = "ERR_INCONSISTENT_FIELD"
    ErrInvalidShareFormat    ErrorCode = "ERR_INVALID_SHARE_FORMAT"
    ErrThresholdNotMet       ErrorCode = "ERR_THRESHOLD_NOT_MET"
    ErrMathInconsistency     ErrorCode = "ERR_MATH_INCONSISTENCY"
)
