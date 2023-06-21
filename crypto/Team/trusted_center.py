# this code is provided to you to familiarize yourself with what works on the server

with open('key.txt', 'r') as file:
    key = [int(i) for i in file.read().split(', ')]

with open('seed.txt', 'r') as file:
    seed = [int(i) for i in file.read().split(', ')]

def rotr(a, n):
    return ((a >> n) | (a << (32 - n))) & 0xffffffff

def sha256(m):
    h0 = 0x6A09E667
    h1 = 0xBB67AE85
    h2 = 0x3C6EF372
    h3 = 0xA54FF53A
    h4 = 0x510E527F
    h5 = 0x9B05688C
    h6 = 0x1F83D9AB
    h7 = 0x5BE0CD19
    k = [0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2]
    m += bytes([0x80] + [0x00]*((55 - len(m)) % 64)) + (len(m)*8).to_bytes(8, byteorder = 'big')
    while m != b'':
        w = [0x10000000] * 64
        for i in range(16):
            w[i], m = int.from_bytes(m[:4], byteorder = 'big'), m[4: ]
        for i in range(16, 64):
            s0 = rotr(w[i-15], 7) ^ rotr(w[i-15], 18) ^ (w[i-15] >> 3)
            s1 = rotr(w[i-2], 17) ^ rotr(w[i-2], 19) ^ (w[i-2] >> 10)
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & 0xffffffff
        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
        for i in range(64):
            sum0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
            Ma = (a & b) ^ (a & c) ^ (b & c)
            t2 = (sum0 + Ma) & 0xffffffff
            sum1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
            Ch = (e & f) ^ ((e ^ 0xffffffff) & g)
            t1 = (h + sum1 + Ch + k[i] + w[i]) & 0xffffffff
            h, g, f, e, d, c, b, a = g, f, e, (d + t1) & 0xffffffff, c, b, a, (t1 + t2) & 0xffffffff
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
        h5 = (h5 + f) & 0xffffffff
        h6 = (h6 + g) & 0xffffffff
        h7 = (h7 + h) & 0xffffffff
    hash256 = hex(h0)[2:] + hex(h1)[2:] + hex(h2)[2:] + hex(h3)[2:] + hex(h4)[2:] + hex(h5)[2:] + hex(h6)[2:] + hex(h7)[2:]
    return hash256

def rand_bit():
    global seed
    new_bit = 0
    for i in range(1, len(key)):
        if key[i] == 1:
            new_bit ^= seed[-i]
    seed = seed[1: ] + [new_bit]
    return new_bit

def rand(L):
    res = 0
    for i in range(L):
        res = (res << 1) ^ rand_bit()
    return res

while True:
    print(rand(512))
    with open('seed.txt', 'w') as file:
        file.write(str(seed)[1:-1])
        break