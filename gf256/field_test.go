package gf256

import "testing"

func TestAddSubIdentity(t *testing.T) {
    for a := 0; a < 256; a++ {
        for b := 0; b < 256; b++ {
            aa := byte(a)
            bb := byte(b)

            if Add(aa, bb) != Sub(aa, bb) {
                t.Fatalf("add/sub mismatch for %02x, %02x", aa, bb)
            }
            if Add(aa, bb)^bb != aa {
                t.Fatalf("add inverse failed for %02x, %02x", aa, bb)
            }
        }
    }
}

func TestMulZeroAndOne(t *testing.T) {
    for a := 0; a < 256; a++ {
        aa := byte(a)

        if Mul(aa, 0) != 0 {
            t.Fatalf("a*0 != 0 for %02x", aa)
        }
        if Mul(0, aa) != 0 {
            t.Fatalf("0*a != 0 for %02x", aa)
        }
        if Mul(aa, 1) != aa {
            t.Fatalf("a*1 != a for %02x", aa)
        }
        if Mul(1, aa) != aa {
            t.Fatalf("1*a != a for %02x", aa)
        }
    }
}

func TestMulInverse(t *testing.T) {
    for a := 1; a < 256; a++ {
        aa := byte(a)

        inv, ok := Inv(aa)
        if !ok {
            t.Fatalf("inverse missing for %02x", aa)
        }
        if Mul(aa, inv) != 1 {
            t.Fatalf("a*inv(a) != 1 for %02x", aa)
        }
    }
}

func TestDivConsistency(t *testing.T) {
    for a := 0; a < 256; a++ {
        for b := 1; b < 256; b++ {
            aa := byte(a)
            bb := byte(b)

            q, ok := Div(aa, bb)
            if !ok {
                t.Fatalf("division failed for %02x / %02x", aa, bb)
            }
            if Mul(q, bb) != aa {
                t.Fatalf("division inconsistency for %02x / %02x", aa, bb)
            }
        }
    }
}

func TestInverseOfZero(t *testing.T) {
    if _, ok := Inv(0); ok {
        t.Fatal("inverse of zero should fail")
    }
}

func TestDivisionByZero(t *testing.T) {
    if _, ok := Div(1, 0); ok {
        t.Fatal("division by zero should fail")
    }
}
