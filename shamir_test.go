package shamir

import (
    "bytes"
    "testing"
)

// fixedRNG returns a deterministic byte stream for tests.
type fixedRNG struct {
    data []byte
    pos  int
}

func (r *fixedRNG) Read(p []byte) (int, error) {
    for i := range p {
        p[i] = r.data[r.pos%len(r.data)]
        r.pos++
    }
    return len(p), nil
}

func TestSplitAndCombine(t *testing.T) {
    secret := []byte("correct horse battery staple")
    rng := &fixedRNG{data: []byte{0x42, 0x99, 0x17}}

    shares, err := Split(secret, 3, 5, rng)
    if err != nil {
        t.Fatalf("split failed: %v", err)
    }

    recovered, err := Combine(shares[:3])
    if err != nil {
        t.Fatalf("combine failed: %v", err)
    }

    if !bytes.Equal(secret, recovered) {
        t.Fatalf("recovered secret mismatch")
    }
}

func TestOrderIndependence(t *testing.T) {
    secret := []byte("order does not matter")
    rng := &fixedRNG{data: []byte{0x01, 0x02, 0x03}}

    shares, err := Split(secret, 3, 5, rng)
    if err != nil {
        t.Fatalf("split failed: %v", err)
    }

    // Reverse order
    recovered, err := Combine([]Share{shares[4], shares[2], shares[0]})
    if err != nil {
        t.Fatalf("combine failed: %v", err)
    }

    if !bytes.Equal(secret, recovered) {
        t.Fatalf("recovered secret mismatch with reordered shares")
    }
}

func TestInsufficientShares(t *testing.T) {
    secret := []byte("too few shares")
    rng := &fixedRNG{data: []byte{0xAA}}

    shares, err := Split(secret, 3, 5, rng)
    if err != nil {
        t.Fatalf("split failed: %v", err)
    }

    recovered, err := Combine(shares[:2])
    if err == nil && bytes.Equal(secret, recovered) {
        t.Fatalf("secret should not reconstruct with insufficient shares")
    }
}

func TestDifferentSecretLengths(t *testing.T) {
    secrets := [][]byte{
        {0x00},
        {0x01, 0x02},
        []byte("variable length secret"),
    }

    for _, secret := range secrets {
        rng := &fixedRNG{data: []byte{0x55}}

        shares, err := Split(secret, 2, 3, rng)
        if err != nil {
            t.Fatalf("split failed: %v", err)
        }

        recovered, err := Combine(shares[:2])
        if err != nil {
            t.Fatalf("combine failed: %v", err)
        }

        if !bytes.Equal(secret, recovered) {
            t.Fatalf("recovered secret mismatch for length %d", len(secret))
        }
    }
}

