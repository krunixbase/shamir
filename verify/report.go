type VerificationReport struct {
    ValidSharesCount   int
    InvalidSharesCount int
    ThresholdSatisfied bool
    Errors             []VerificationError
    Warnings           []VerificationWarning
}
