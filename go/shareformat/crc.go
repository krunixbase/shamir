package shareformat

import "hash/crc32"

// CRC32 computes the IEEE CRC32 checksum for given data.
//
// This function is used as a mandatory integrity check
// for serialized Shamir shares to detect accidental corruption.
func CRC32(data []byte) uint32 {
    return crc32.ChecksumIEEE(data)
}
