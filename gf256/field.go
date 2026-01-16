package gf256

// GF(256) arithmetic with the irreducible polynomial x^8 + x^4 + x^3 + x + 1 (0x11B),
// as commonly used (e.g., AES). All operations are deterministic and allocation-free.

// expTable is duplicated to avoid a modulus operation on indices in multiplication.
var expTable [512]byte

// logTable maps a non-zero field element to its discrete log.
// logTable[0] is unused.
var logTable [256]byte

func init() {
    // Build log/exp tables using generator 0x03 (common choice for AES field).
    //
    // expTable[i] = g^i for i in [0..254]
    // logTable[g^i] = i for i in [0..254]
    //
    // Then expTable is duplicated so expTable[i+255] == expTable[i].
    var x byte = 1
    for i := 0; i < 255; i++ {
        expTable[i] = x
        logTable[x] = byte(i)
        x = mulNoTable(x, 0x03)
    }
    for i := 255; i < 512; i++ {
        expTable[i] = expTable[i-255]
    }
}

// Add returns a + b in GF(256). (Same as subtraction.)
func Add(a, b byte) byte { return a ^ b }

// Sub returns a - b in GF(256). (Same as addition.)
func Sub(a, b byte) byte { return a ^ b }

// Mul returns a * b in GF(256).
func Mul(a, b byte) byte {
    if a == 0 || b == 0 {
        return 0
    }
    return expTable[int(logTable[a])+int(logTable[b])]
}

// Inv returns the multiplicative inverse of a in GF(256).
// If a == 0, ok is false and inv is 0.
func Inv(a byte) (inv byte, ok bool) {
    if a == 0 {
        return 0, false
    }
    // a^{-1} = g^(255 - log_g(a))
    return expTable[255-int(logTable[a])], true
}

// Div returns a / b in GF(256).
// If b == 0, ok is false and q is 0.
func Div(a, b byte) (q byte, ok bool) {
    if b == 0 {
        return 0, false
    }
    if a == 0 {
        return 0, true
    }
    la := int(logTable[a])
    lb := int(logTable[b])
    d := la - lb
    if d < 0 {
        d += 255
    }
    return expTable[d], true
}

// mulNoTable multiplies a * b in GF(256) using the "Russian peasant" method.
// Deterministic and table-free; used only to build the exp/log tables.
func mulNoTable(a, b byte) byte {
    var p byte
    for i := 0; i < 8; i++ {
        if (b & 1) != 0 {
            p ^= a
        }
        hi := a & 0x80
        a <<= 1
        // Reduce by 0x11B (drop the x^8 term -> XOR 0x1B).
        if hi != 0 {
            a ^= 0x1B
        }
        b >>= 1
    }
    return p
}
