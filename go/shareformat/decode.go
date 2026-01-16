package shareformat

import (
    "bytes"
    "encoding/binary"
    "errors"
    "hash/crc32"
)

var (
    ErrInvalidMagic   = errors.New("invalid magic value")
    ErrInvalidVersion = errors.New("unsupported format version")
    ErrInvalidHeader  = errors.New("invalid share header")
    ErrCRCMismatch    = errors.New("crc32 mismatch")
    ErrEmptyPayload   = errors.New("empty payload")
)

const (
    magicValue = "SHAM"
    version    = 0x01

    fieldGF256 = 0x01
)

type ShareHeader struct {
    Threshold  uint8
    ShareCount uint8
    ShareIndex uint8
    FieldID    uint8
}

func (h ShareHeader) validate() error {
    if h.Threshold == 0 || h.Threshold > h.ShareCount {
        return ErrInvalidHeader
    }
    if h.ShareIndex == 0 || h.ShareIndex > h.ShareCount {
        return ErrInvalidHeader
    }
    if h.FieldID != fieldGF256 {
        return ErrInvalidHeader
    }
    return nil
}

func Decode(data []byte) (ShareHeader, []byte, error) {
    var header ShareHeader

    if len(data) < 10 {
        return header, nil, ErrInvalidHeader
    }

    reader := bytes.NewReader(data)

    var magic [4]byte
    if err := binary.Read(reader, binary.BigEndian, &magic); err != nil {
        return header, nil, err
    }
    if string(magic[:]) != magicValue {
        return header, nil, ErrInvalidMagic
    }

    var ver uint8
    if err := binary.Read(reader, binary.BigEndian, &ver); err != nil {
        return header, nil, err
    }
    if ver != version {
        return header, nil, ErrInvalidVersion
    }

    if err := binary.Read(reader, binary.BigEndian, &header.Threshold); err != nil {
        return header, nil, err
    }
    if err := binary.Read(reader, binary.BigEndian, &header.ShareCount); err != nil {
        return header, nil, err
    }
    if err := binary.Read(reader, binary.BigEndian, &header.ShareIndex); err != nil {
        return header, nil, err
    }
    if err := binary.Read(reader, binary.BigEndian, &header.FieldID); err != nil {
        return header, nil, err
    }

    if err := header.validate(); err != nil {
        return header, nil, err
    }

    payloadLen := len(data) - reader.Len() - 4
    if payloadLen <= 0 {
        return header, nil, ErrEmptyPayload
    }

    payload := make([]byte, payloadLen)
    if _, err := reader.Read(payload); err != nil {
        return header, nil, err
    }

    var expectedCRC uint32
    if err := binary.Read(reader, binary.BigEndian, &expectedCRC); err != nil {
        return header, nil, err
    }

    actualCRC := crc32.ChecksumIEEE(data[:len(data)-4])
    if actualCRC != expectedCRC {
        return header, nil, ErrCRCMismatch
    }

    return header, payload, nil
}
