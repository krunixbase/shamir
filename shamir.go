package shamir

import (
    "errors"
    "io"

    "github.com/krunixbase/shamir/gf256"
)

// Share represents a single Shamir share.
type Share struct {
    X byte
    Y []byte
}

// Split splits the secret into n shares with threshold k.
// rng is used to generate random polynomial coefficients.
func Split(secret []byte, k, n int, rng io.Reader) ([]Share, error) {
    if k < 2 {
        return nil, errors.New("threshold k must be >= 2")
    }
    if n < k {
        return nil, errors.New("number of shares n must be >= k")
    }
    if len(secret) == 0 {
        return nil, errors.New("secret must not be empty")
    }

    // Prepare shares
    shares := make([]Share, n)
    for i := 0; i < n; i++ {
        shares[i] = Share{
            X: byte(i + 1),
            Y: make([]byte, len(secret)),
        }
    }

    coeffs := make([]byte, k)

    for idx, s := range secret {
        coeffs[0] = s

        if _, err := io.ReadFull(rng, coeffs[1:]); err != nil {
            return nil, err
        }

        for i := 0; i < n; i++ {
            x := shares[i].X
            y := coeffs[0]
            pow := byte(1)

            for j := 1; j < k; j++ {
                pow = gf256.Mul(pow, x)
                y = gf256.Add(y, gf256.Mul(coeffs[j], pow))
            }

            shares[i].Y[idx] = y
        }
    }

    return shares, nil
}

// Combine reconstructs the secret from at least k shares.
func Combine(shares []Share) ([]byte, error) {
    if len(shares) < 2 {
        return nil, errors.New("at least two shares are required")
    }

    secretLen := len(shares[0].Y)
    for _, s := range shares {
        if len(s.Y) != secretLen {
            return nil, errors.New("inconsistent share lengths")
        }
    }

    secret := make([]byte, secretLen)

    for idx := 0; idx < secretLen; idx++ {
        var acc byte

        for i, si := range shares {
            num := byte(1)
            den := byte(1)

            for j, sj := range shares {
                if i == j {
                    continue
                }
                num = gf256.Mul(num, sj.X)
                den = gf256.Mul(den, gf256.Add(sj.X, si.X))
            }

            invDen, ok := gf256.Inv(den)
            if !ok {
                return nil, errors.New("singular interpolation")
            }

            term := gf256.Mul(si.Y[idx], gf256.Mul(num, invDen))
            acc = gf256.Add(acc, term)
        }

        secret[idx] = acc
    }

    return secret, nil
}
