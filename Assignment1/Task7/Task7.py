import time
import os

class TEA:
    def __init__(self, key):
        if len(key) != 16:
            raise ValueError("Key must be 16 bytes")
        self.key = []
        self.delta = 0x9e3779b9
        for i in range(0, 16, 4):
            self.key.append(int.from_bytes(key[i:i+4], 'big'))

    def encryption(self, plainText):
        if len(plainText) != 8:
            raise ValueError("Block must be 8 bytes")
        
        v0 = int.from_bytes(plainText[:4], 'big')
        v1 = int.from_bytes(plainText[:4], 'big')

        k0, k1, k2, k3 = self.key
        sumValue = 0

        for _ in range(32):
            sumValue = (sumValue + self.delta) & 0xFFFFFFFF
            v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + sumValue) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
            v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + sumValue) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF

        return v0.to_bytes(4, 'big') + v1.to_bytes(4, 'big')

class CFB:
    def __init__(self, cipher, iv):
        self.cipher = cipher
        self.iv = iv
        self.blockSize = 8 

    def encrypt(self, plainText, shiftRegister):
        encryptedString = self.cipher.encryption(shiftRegister)
        keystream = (encryptedString[0] >> 7) & 1
        ciphertext = plainText ^ keystream
        newString = bytearray(shiftRegister)

        carry = 0
        for i in range(len(newString) - 1, -1, -1):
            newCarry = (newString[i] >> 7) & 1
            newString[i] = ((newString[i] << 1 | carry)) & 0xFF
            carry = newCarry

        newString[-1] |= ciphertext
        return ciphertext, bytes(newString)

    def decrypt(self, cipherText, shiftRegister):
        encryptedString = self.cipher.encryption(shiftRegister)
        keystream = (encryptedString[0] >> 7) & 1
        plaintext = cipherText ^ keystream
        newString = bytearray(shiftRegister)

        carry = 0
        for i in range(len(newString) - 1, -1, -1):
            newCarry = (newString[i] >> 7) & 1
            newString[i] = ((newString[i] << 1) | carry) & 0xFF
            carry = newCarry

        newString[-1] |= cipherText
        return plaintext, bytes(newString)

class SynchronousCipher:
    def __init__(self, k0, k1):
        self.k0 = k0
        self.k1 = k1
        self.keystream = [k0, k1]

    def generateKeystream(self, length):
        while len(self.keystream) < length:
            newKey = (self.keystream[-1] * self.keystream[-2]) % 26
            self.keystream.append(newKey)
        return self.keystream[:length]

    def encrypt_char(self, char, key):
        if 'A' <= char <= 'Z':
            return chr(((ord(char) - ord('A') + key) % 26) + ord('A'))
        return char

    def decrypt_char(self, char, key):
        if 'A' <= char <= 'Z':
            return chr(((ord(char) - ord('A') - key) % 26) + ord('A'))
        return char

    def encryption(self, plaintext):
        keystream = self.generateKeystream(len(plaintext))
        result = ""
        for i, char in enumerate(plaintext):
            result += self.encrypt_char(char, keystream[i])
        return result

    def decryption(self, ciphertext):
        keystream = self.generateKeystream(len(ciphertext))
        result = ""
        for i, char in enumerate(ciphertext):
            result += self.decrypt_char(char, keystream[i])
        return result

class CombinationCipher:
    def __init__(self, teaKey, iv, k0, k1):
        self.tea = TEA(teaKey)
        self.cfb = CFB(self.tea, iv)
        self.syncCipher = SynchronousCipher(k0, k1)

    def encryption(self, plaintext):
        result = ""
        shiftRegister = self.cfb.iv

        keystream = self.syncCipher.generateKeystream(len(plaintext))

        for i, char in enumerate(plaintext):
            if i % 2 == 0:
                if 'A' <= char <= 'Z':
                    charValue = ord(char) - ord('A')
                    encryptionBits = []

                    for bitPosition in range(5):
                        bit = (charValue >> (4 - bitPosition)) & 1
                        encryptedBit, shiftRegister = self.cfb.encrypt(bit, shiftRegister)
                        encryptionBits.append(encryptedBit)

                    encryptedValue = 0
                    for bit in encryptionBits:
                        encryptedValue = (encryptedValue << 1) | bit
                    result += chr((encryptedValue % 26) + ord('A'))
                else:
                    result += char
            else:
                result += self.syncCipher.encrypt_char(char, keystream[i])
        return result

    def decryption(self, ciphertext):
        result = ""
        shiftRegister = self.cfb.iv

        keystream = self.syncCipher.generateKeystream(len(ciphertext))

        for i, char in enumerate(ciphertext):
            if i % 2 == 0:
                if 'A' <= char <= 'Z':
                    charValue = ord(char) - ord('A')
                    decryptedBits = []

                    for bitPosition in range(5):
                        bit = (charValue >> (4 - bitPosition)) & 1
                        decryptedBit, shiftRegister = self.cfb.decrypt(bit, shiftRegister)
                        decryptedBits.append(decryptedBit)

                    decryptedValue = 0
                    for bit in decryptedBits:
                        decryptedValue = (decryptedValue << 1) | bit
                    result += chr((decryptedValue % 26) + ord('A')) 
                else:
                    resutl += char
            else:
                result += self.syncCipher.decrypt_char(char, keystream[i])

        return result

def createTestDocument(size=200):
    content = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG. " * 1000
    # Repeat to reach approximately the desired size
    target_size = int(size * 1024 * 1024)
    content_size = len(content.encode())
    multiplier = max(1, target_size // content_size)
    
    # Create the document and ensure it's the right size
    document = (content * multiplier)
    if len(document.encode()) > target_size:
        document = document[:target_size]
    
    return document.replace(" ", "").upper()

def benchmarkEncryption(cipher, document, cipherName):
    print(f"\n=== {cipherName} Benchmark ===")
    print(f"Document size: {len(document)} characters ({len(document.encode())/1024/1024:.2f} MB)")
    
    # Encryption timing
    start_time = time.time()
    encrypted = cipher.encryption(document)
    encrypt_time = time.time() - start_time
    
    # Decryption timing
    start_time = time.time()
    decrypted = cipher.decryption(encrypted)
    decrypt_time = time.time() - start_time
    
    print(f"Encryption time: {encrypt_time:.4f} seconds")
    print(f"Decryption time: {decrypt_time:.4f} seconds")
    print(f"Total time: {encrypt_time + decrypt_time:.4f} seconds")
    
    return encrypt_time, decrypt_time

def main():
    print("=== Task 7: Combined CFB and Synchronous Cipher ===\n")
    
    # Step 1: Create test document (200MB equivalent in characters)
    print("Step 1: Creating test document...")
    test_document = createTestDocument(1)  # Using 1MB for demo (200MB would be very slow)
    print(f"Created document with {len(test_document)} characters")
    
    # Initialize cipher parameters
    tea_key = b"YELLOW SUBMARINE"  # 16-byte key for TEA
    iv = b"INITVECT"  # 8-byte IV for CFB
    k0, k1 = 7, 11  # Keys for synchronous cipher
    
    # Step 2: Test individual ciphers
    print("\n=== Testing Individual Ciphers ===")
    
    # Test 1-bit CFB with TEA
    tea = TEA(tea_key)
    cfb = CFB(tea, iv)
    
    # Test synchronous cipher
    sync_cipher = SynchronousCipher(k0, k1)
    
    # Test with "I LOVE WOLLONGONG"
    test_msg = "ILOVEWOLLONGONG"
    print(f"\nTesting with message: {test_msg}")
    
    # Synchronous cipher test
    sync_encrypted = sync_cipher.encryption(test_msg)
    sync_decrypted = sync_cipher.decryption(sync_encrypted)
    print(f"Synchronous - Encrypted: {sync_encrypted}")
    print(f"Synchronous - Decrypted: {sync_decrypted}")
    print(f"Synchronous - Success: {sync_decrypted == test_msg}")
    
    # Step 3: Test hybrid cipher
    print(f"\n=== Testing Combination Cipher ===")
    hybrid = CombinationCipher(tea_key, iv, k0, k1)
    
    # Test with short message first
    hybrid_encrypted = hybrid.encryption(test_msg)
    hybrid_decrypted = hybrid.decryption(hybrid_encrypted)
    print(f"Combination - Original: {test_msg}")
    print(f"Combination - Encrypted: {hybrid_encrypted}")
    print(f"Combination - Decrypted: {hybrid_decrypted}")
    print(f"Combination - Success: {hybrid_decrypted == test_msg}")
    
    # Step 4: Benchmark with larger document
    print(f"\n=== Performance Comparison ===")
    
    # Use smaller document for demonstration
    benchmark_doc = createTestDocument(0.1)  # 0.1 MB for faster demo
    
    # Benchmark synchronous cipher only
    sync_encrypt_time, sync_decrypt_time = benchmarkEncryption(
        sync_cipher, benchmark_doc, "Synchronous Cipher"
    )
    
    # Benchmark hybrid cipher
    hybrid_encrypt_time, hybrid_decrypt_time = benchmarkEncryption(
        hybrid, benchmark_doc, "Combination Cipher (CFB + Synchronous)"
    )
    
    # Step 5: Analysis
    print(f"\n=== Performance Analysis ===")
    print(f"Synchronous cipher total time: {sync_encrypt_time + sync_decrypt_time:.4f} seconds")
    print(f"Combination cipher total time: {hybrid_encrypt_time + hybrid_decrypt_time:.4f} seconds")
    
    if hybrid_encrypt_time + hybrid_decrypt_time > sync_encrypt_time + sync_decrypt_time:
        ratio = (hybrid_encrypt_time + hybrid_decrypt_time) / (sync_encrypt_time + sync_decrypt_time)
        print(f"Combination cipher is {ratio:.2f}x slower than synchronous cipher")
    else:
        ratio = (sync_encrypt_time + sync_decrypt_time) / (hybrid_encrypt_time + hybrid_decrypt_time)
        print(f"Combination cipher is {ratio:.2f}x faster than synchronous cipher")

if __name__ == "__main__":
    main()
