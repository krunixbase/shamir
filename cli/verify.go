package cli

import (
    "fmt"
    "os"

    "github.com/krunixbase/shamir/verify"
)

func RunVerify(shares []core.Share, threshold int) int {
    report := verify.VerifyShares(shares, threshold)

    if report.ThresholdSatisfied && len(report.Errors) == 0 {
        fmt.Println("Verification successful")
        return 0
    }

    fmt.Println("Verification failed")
    for _, err := range report.Errors {
        fmt.Printf("- %s: %s %v\n", err.Code, err.Message, err.Context)
    }

    return 1
}

