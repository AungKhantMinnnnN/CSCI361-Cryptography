import struct
import time

class TEA_CFB:
    def __init__(self, key):
        if len(key) != 16:
            raise ValueError("Key must be 16 bytes (128 bits)")
        
        self.key = struct.unpack('>4I', key)
        self.delta = 0x9e3779b9

    def TEA_encrypt(self, v0, v1):
        sumValue = 0

        for i in range(32):
            sumValue = (sumValue + self.delta) & 0xffffffff
            v0 = (v0 + (((v1 << 4) + self.key[0]) ^ (v1 + sumValue) ^ ((v1 >> 5) + self.key[1]))) & 0xffffffff
            v1 = (v1 + (((v0 << 4) + self.key[2]) ^ (v0 + sumValue) ^ ((v0 >> 5) + self.key[3]))) & 0xffffffff

        return v0, v1

    def bytesToBits(self, data):
        bits = []
        for byte in data:
            for i in range(8):
                bits.append((byte >> (7-i)) & i)
        return bits

    def bitsToBytes(self, bits):
        while len(bits) % 8 != 0:
            bits.append(0)

        result = bytearray()
        for i in range(0, len(bits), 8):
            byteValue = 0
            for j in range(8):
                if i + j < len(bits):
                    byteValue = (bits[i + j] << ( 7 - j))
            result.append(byteValue)

        return bytes(result)
    
    def shiftRegisterLeft(self, register, newBits, feedbackSize):
        register = register[feedbackSize:] + newBits
        return register 

    def encryption(self, plainText, iv, feedbackBits):

        if len(iv) != 8:
            raise ValueError("IV must be exactly 8 bytes (64 bits)")
        
        shiftRegister = int.from_bytes(iv, 'big')

        if isinstance(plainText, str):
            plainText = plainText.encode('utf-8')

        result = bytearray()

        for byte in plainText:
            encryptedByte = 0

            for position in range(8):
                plaintextBit = (byte >> (7 - position)) & 1

                v0 = (shiftRegister >> 32) & 0xffffffff
                v1 = shiftRegister & 0xffffffff
                encryptedV0, encryptedV1 = self.TEA_encrypt(v0, v1)

                encryptedRegister = ((encryptedV0 << 32) | encryptedV1) & 0xffffffffffffffff

                keystreamBit = (encryptedRegister >> 63) & 1

                cipherBit = plaintextBit ^ keystreamBit

                encryptedByte |= (cipherBit << (7 - position))

                shiftRegister = ((shiftRegister << 1) | cipherBit) &  0xffffffffffffffff
            
            result.append(encryptedByte)

        return bytes(result)

    def decryption(self, cipherText, iv, feedbackBits):
        if len(iv) != 8:
            raise ValueError("IV must be exactly 8 bytes (64 bits)")
        
        shiftRegister = int.from_bytes(iv, 'big')

        result = bytearray()

        for byte in cipherText:
            decryptedByte = 0
            
            for position in range(8):
                cipherBit = (byte >> (7 - position)) & 1

                v0 = (shiftRegister >> 32) & 0xffffffff
                v1 = shiftRegister & 0xffffffff
                encryptedV0, encryptedV1 = self.TEA_encrypt(v0, v1)

                encryptedRegister = ((encryptedV0 << 32) | encryptedV1) & 0xffffffffffffffff

                keystreamBit = (encryptedRegister >> 63) & 1

                plaintextBit = cipherBit ^ keystreamBit

                decryptedByte |= (plaintextBit << (7 - position))

                shiftRegister = ((shiftRegister << 1) | cipherBit) & 0xffffffffffffffff

            result.append(decryptedByte)
        return bytes(result)

def main():
    studentNumber = "670182"
    print("=" * 60)
    print("CFB TEA ALGORITHM COMPARISON")
    print("=" * 60)
    print(f"Student Number: {studentNumber}")

    studentNumberSum = sum(int(digit) for digit in studentNumber)
    c = studentNumberSum % 7
    print(f"Sum of digits: {studentNumberSum}")
    print(f"c = {studentNumberSum} mod 7 = {c}")
    print()

    key = b"CRYPTOGRAPHY_KEY" # 16 byte cryptography key
    iv = b"INITIAL_" # 8 byte IV
    plaintext = studentNumber.encode('utf-8')

    print(f"Plaintext (student number): {studentNumber}")
    print(f"Key: {key.decode('utf-8')}")
    print(f"IV: {iv.decode('utf-8')}")
    print()

    cipher = TEA_CFB(key)

    # Part 2: 5-bit CFB TEA encryption
    print("PART 2: 5-bit CFB TEA Encryption")
    print("-" * 40)

    startTime = time.time()
    cipherText_5bit = cipher.encryption(plaintext, iv, 5)
    time_5bit = time.time() - startTime

    print(f"5-bit CFB TEA Ciphertext (hex): {cipherText_5bit.hex()}")
    print(f"5-bit CFB TEA Encryption time: {time_5bit:.6f} seconds")

    decryptedText_5bit = cipher.decryption(cipherText_5bit, iv, 5)
    decrypted_5bit_trimmed = decryptedText_5bit[:len(plaintext)]
    print(f"5-bit CFB TEA Decrypted: {decrypted_5bit_trimmed.decode('utf-8')}")
    print(f"5-bit CFB TEA Verification: {'PASS' if plaintext == decrypted_5bit_trimmed else 'FAIL'}")
    print()

    # Part 3: c-bit CFB TEA encryption 
    print(f"PART 3: {c}-it CFB TEA encryption")
    print('-' * 40)

    startTime = time.time()
    cipherText_cBit = cipher.encryption(plaintext, iv, c)
    time_cBit = time.time() - startTime

    print(f"{c}-bit CFB TEA Ciphertext (hex): {cipherText_cBit.hex()}")
    print(f"{c}-bit CFB TEA Encryption time: {time_cBit:.6f} seconds")

    decrypted_cBit = cipher.decryption(cipherText_cBit, iv, c)
    decrypted_cBit_trimmed = decrypted_cBit[:len(plaintext)]
    print(f"{c}-bit CFB TEA Decrypted: {decrypted_cBit_trimmed.decode('utf-8')}")
    print(f"{c}-bit CFB TEA Verification: {'PASS' if plaintext == decrypted_cBit_trimmed else 'FAIL'}")
    print()

    # Performance comparison
    print("PERFORMANCE COMPARISON")
    print("-" * 40)
    print(f"5-bit CFB TEA time: {time_5bit:.6f} seconds")
    print(f"{c}-bit CFB TEA time: {time_cBit:.6f} seconds")

    if time_5bit > time_cBit:
        ratio = time_5bit / time_cBit
        print(f"3-bit CFB TEA is {ratio:.2f}x faster than 5-bit CFB TEA")
    else:
        ratio = time_cBit / time_5bit
        print(f"5-bit CFB TEA is {ratio:.2f}x faster than 3-bit CFB TEA")

if __name__ == "__main__":
    main()