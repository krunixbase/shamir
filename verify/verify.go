func VerifyShares(shares []core.Share, threshold int) VerificationReport {
    report := VerificationReport{}

    if len(shares) == 0 {
        report.Errors = append(report.Errors, VerificationError{
            Code:    ErrInvalidShareFormat,
            Message: "No shares provided",
        })
        return report
    }

    report.Errors = append(report.Errors, checkDuplicateIDs(shares)...)
    report.Errors = append(report.Errors, checkParameterConsistency(shares)...)
    report.Errors = append(report.Errors, checkShareStructure(shares)...)

    report.ThresholdSatisfied = checkThreshold(len(shares), threshold)
    if !report.ThresholdSatisfied {
        report.Errors = append(report.Errors, VerificationError{
            Code:    ErrThresholdNotMet,
            Message: "Reconstruction threshold not satisfied",
        })
    }

    report.Errors = append(report.Errors, checkPolynomialConsistency(shares)...)

    report.ValidSharesCount = len(shares) - len(report.Errors)
    report.InvalidSharesCount = len(report.Errors)

    return report
}

