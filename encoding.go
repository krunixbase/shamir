package shamir

import (
    "bytes"
    "encoding/base64"
    "encoding/binary"
    "errors"
    "strings"
)

const (
    tlvX byte = 0x01
    tlvL byte = 0x02
    tlvY byte = 0x03

    textPrefix = "shamir1:"
)

// EncodeShare encodes a Share into a binary TLV format.
func EncodeShare(s Share) ([]byte, error) {
    if s.X == 0 {
        return nil, errors.New("invalid share X value")
    }
    if len(s.Y) == 0 {
        return nil, errors.New("empty share payload")
    }

    var buf bytes.Buffer

    // X
    buf.WriteByte(tlvX)
    buf.WriteByte(s.X)

    // Length
    buf.WriteByte(tlvL)
    if err := binary.Write(&buf, binary.BigEndian, uint16(len(s.Y))); err != nil {
        return nil, err
    }

    // Y
    buf.WriteByte(tlvY)
    buf.Write(s.Y)

    return buf.Bytes(), nil
}

// DecodeShare decodes a Share from a binary TLV format.
func DecodeShare(data []byte) (Share, error) {
    var s Share
    r := bytes.NewReader(data)

    for r.Len() > 0 {
        tag, err := r.ReadByte()
        if err != nil {
            return s, err
        }

        switch tag {
        case tlvX:
            x, err := r.ReadByte()
            if err != nil {
                return s, err
            }
            s.X = x

        case tlvL:
            var l uint16
            if err := binary.Read(r, binary.BigEndian, &l); err != nil {
                return s, err
            }
            s.Y = make([]byte, l)

        case tlvY:
            if len(s.Y) == 0 {
                return s, errors.New("missing length before payload")
            }
            if _, err := r.Read(s.Y); err != nil {
                return s, err
            }

        default:
            return s, errors.New("unknown TLV tag")
        }
    }

    if s.X == 0 || len(s.Y) == 0 {
        return s, errors.New("incomplete share encoding")
    }

    return s, nil
}

// MarshalText encodes a Share into a versioned Base64URL string.
func MarshalText(s Share) (string, error) {
    bin, err := EncodeShare(s)
    if err != nil {
        return "", err
    }

    enc := base64.RawURLEncoding.EncodeToString(bin)
    return textPrefix + enc, nil
}

// UnmarshalText decodes a Share from a versioned Base64URL string.
func UnmarshalText(text string) (Share, error) {
    if !strings.HasPrefix(text, textPrefix) {
        return Share{}, errors.New("invalid share prefix")
    }

    raw := strings.TrimPrefix(text, textPrefix)
    bin, err := base64.RawURLEncoding.DecodeString(raw)
    if err != nil {
        return Share{}, err
    }

    return DecodeShare(bin)
}
