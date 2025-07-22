import struct
import time

class TEA_CFB_1bit:
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

    def encryption(self, plainText, iv):

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

    def decryption(self, cipherText, iv):
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
    print("1-bit CFB TEA ALGORITHM")
    print("=" * 60)
    print(f"Student Number: {studentNumber}")

    key = b"CRYPTOGRAPHY_KEY" # 16 byte cryptography key
    iv = b"INITIAL_" # 8 byte IV
    plaintext = studentNumber.encode('utf-8')

    print(f"Plaintext (student number): {studentNumber}")
    print(f"Key: {key.decode('utf-8')}")
    print(f"IV: {iv.decode('utf-8')}")
    print()

    cipher = TEA_CFB_1bit(key)

    print("1-bit CFB TEA Encryption")
    print("-" * 40)

    startTime = time.time()
    cipherText_1bit = cipher.encryption(plaintext, iv)
    time_1bit = time.time() - startTime

    print(f"1-bit CFB TEA Ciphertext (hex): {cipherText_1bit.hex()}")
    print(f"1-bit CFB TEA Encryption time: {time_1bit:.6f} seconds")

    decryptedText_1bit = cipher.decryption(cipherText_1bit, iv)
    decrypted_1bit_trimmed = decryptedText_1bit[:len(plaintext)]
    print(f"1-bit CFB TEA Decrypted: {decrypted_1bit_trimmed.decode('utf-8')}")
    print(f"1-bit CFB TEA Verification: {'PASS' if plaintext == decrypted_1bit_trimmed else 'FAIL'}")
    print()

if __name__ == "__main__":
    main()
