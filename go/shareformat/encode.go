package shareformat

import (
    "bytes"
    "encoding/binary"
    "errors"
    "hash/crc32"
)

var (
    ErrEmptyPayload = errors.New("empty payload")
)

func Encode(header ShareHeader, payload []byte) ([]byte, error) {
    if len(payload) == 0 {
        return nil, ErrEmptyPayload
    }

    if err := header.validate(); err != nil {
        return nil, err
    }

    var buf bytes.Buffer

    // Header
    if err := binary.Write(&buf, binary.BigEndian, []byte(magicValue)); err != nil {
        return nil, err
    }
    if err := binary.Write(&buf, binary.BigEndian, uint8(version)); err != nil {
        return nil, err
    }
    if err := binary.Write(&buf, binary.BigEndian, header.Threshold); err != nil {
        return nil, err
    }
    if err := binary.Write(&buf, binary.BigEndian, header.ShareCount); err != nil {
        return nil, err
    }
    if err := binary.Write(&buf, binary.BigEndian, header.ShareIndex); err != nil {
        return nil, err
    }
    if err := binary.Write(&buf, binary.BigEndian, header.FieldID); err != nil {
        return nil, err
    }

    // Payload
    if _, err := buf.Write(payload); err != nil {
        return nil, err
    }

    // CRC32
    crc := crc32.ChecksumIEEE(buf.Bytes())
    if err := binary.Write(&buf, binary.BigEndian, crc); err != nil {
        return nil, err
    }

    return buf.Bytes(), nil
}
