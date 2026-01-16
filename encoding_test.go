package shamir

import (
    "bytes"
    "testing"
)

func TestBinaryEncodingRoundTrip(t *testing.T) {
    share := Share{
        X: 3,
        Y: []byte{0x10, 0x20, 0x30, 0x40},
    }

    enc, err := EncodeShare(share)
    if err != nil {
        t.Fatalf("EncodeShare failed: %v", err)
    }

    dec, err := DecodeShare(enc)
    if err != nil {
        t.Fatalf("DecodeShare failed: %v", err)
    }

    if dec.X != share.X {
        t.Fatalf("X mismatch: got %d, want %d", dec.X, share.X)
    }
    if !bytes.Equal(dec.Y, share.Y) {
        t.Fatalf("Y mismatch")
    }
}

func TestTextEncodingRoundTrip(t *testing.T) {
    share := Share{
        X: 7,
        Y: []byte("encoded payload"),
    }

    text, err := MarshalText(share)
    if err != nil {
        t.Fatalf("MarshalText failed: %v", err)
    }

    dec, err := UnmarshalText(text)
    if err != nil {
        t.Fatalf("UnmarshalText failed: %v", err)
    }

    if dec.X != share.X {
        t.Fatalf("X mismatch after text round-trip")
    }
    if !bytes.Equal(dec.Y, share.Y) {
        t.Fatalf("Y mismatch after text round-trip")
    }
}

func TestInvalidPrefix(t *testing.T) {
    _, err := UnmarshalText("invalidprefix:abcd")
    if err == nil {
        t.Fatalf("expected error for invalid prefix")
    }
}

func TestMalformedBinaryEncoding(t *testing.T) {
    // Missing payload length
    data := []byte{0x01, 0x02, 0x03}
    _, err := DecodeShare(data)
    if err == nil {
        t.Fatalf("expected error for malformed binary encoding")
    }
}

func TestEmptyShareEncoding(t *testing.T) {
    _, err := EncodeShare(Share{X: 1, Y: nil})
    if err == nil {
        t.Fatalf("expected error for empty share payload")
    }
}
