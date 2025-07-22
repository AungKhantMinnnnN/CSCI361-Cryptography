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
    print("=" * 60)
    print("1-bit CFB TEA File Encryption and Decryption")
    print("=" * 60)

    key = b"CRYPTOGRAPHY_KEY" # 16 byte cryptography key
    iv = b"INITIAL_" # 8 byte IV
    input_file = "plaintext.txt"
    encrypted_file = "encrypted.txt"
    decrypted_file = "decrypted.txt"

    # Read plaintext from file
    with open(input_file, 'rb') as f:
        plaintext = f.read()

    cipher = TEA_CFB_1bit(key)

    # Encrypt the file
    print(f"Encrypting {input_file}...")
    startTime_encrypt = time.time()
    cipherText = cipher.encryption(plaintext, iv)
    endTime_encrypt = time.time()
    encryption_time = endTime_encrypt - startTime_encrypt

    with open(encrypted_file, 'wb') as f:
        f.write(cipherText)

    print(f"Encryption complete. Encrypted data saved to {encrypted_file}")
    print(f"Encryption time: {encryption_time:.6f} seconds")
    print()

    # Decrypt the file
    print(f"Decrypting {encrypted_file}...")
    startTime_decrypt = time.time()
    decryptedText = cipher.decryption(cipherText, iv)
    endTime_decrypt = time.time()
    decryption_time = endTime_decrypt - startTime_decrypt

    with open(decrypted_file, 'wb') as f:
        f.write(decryptedText)

    print(f"Decryption complete. Decrypted data saved to {decrypted_file}")
    print(f"Decryption time: {decryption_time:.6f} seconds")
    print()

    # Verification
    print("Verification:")
    with open(input_file, 'rb') as f1, open(decrypted_file, 'rb') as f2:
        original_content = f1.read()
        decrypted_content = f2.read()
        if original_content == decrypted_content:
            print("File content verification: PASS")
        else:
            print("File content verification: FAIL")

if __name__ == "__main__":
    main()
