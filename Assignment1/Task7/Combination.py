import random

def TEA_encrypt(plaintext, key):
    v0 = plaintext & 0x1F # Lower 5 bits
    v1 = (plaintext >> 5) & 0x1F # Upper 5 bits

    k0, k1, k2, k3 = key

    deltaValue = 0x9E3779B9
    sumValue = 0

    # 32 rounds encryption
    for _ in range(32):
        sumValue = (sumValue + deltaValue) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + sumValue) ^ ((v1 >> 5) + k1))) & 0x1F
        v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + sumValue) ^ ((v0 >> 5) + k3))) & 0x1F

    return (v1 << 5) | v0

def CFB1BitEncryption(message, key, iv):
    result = []
    shiftRegister = iv & 0x3FF

    for char in message:
        encryptedChar = 0
        charValue = ord(char)

        # Process each bit
        for bitPosition in range(8):
            # Extract the bit
            messageBit = (charValue >> bitPosition) & 1

            # Encrypt shift register
            encryptedShiftRegister = TEA_encrypt(shiftRegister, key)

            # Get the leftmost bit of encrypted shift register
            keyBit = (encryptedShiftRegister >> 9) & 1 # Assuming 10 bit output

            # XOR with message bit
            cipherBit = messageBit ^ keyBit
            encryptedChar |= (cipherBit << bitPosition)

            # Update shift register : Shift left and add new cipher bit
            shiftRegister = ((shiftRegister << 1) | cipherBit) & 0x3FF

        result.append(chr(encryptedChar))
    
    return ''.join(result)

def CFB1BitDecryption(ciphertext, key, iv):
    result = []
    shiftRegister = iv & 0x3FF

    for char in ciphertext:
        decryptedChar = 0
        charValue = ord(char)

        # Process each bit
        for bitPosition in range(8):
            # Encrypt shift register
            encryptedShiftRegister = TEA_encrypt(shiftRegister, key)

            # Get the leftmost bit of encrypted shift register
            keyBit = (encryptedShiftRegister >> 9) & 1 # Assuming 10 bit output

            # Extract the ciphertext bit
            cipherBit = (charValue >> bitPosition) & 1

            # XOR with key bit to get the plaintext bit
            messageBit = cipherBit ^ keyBit
            decryptedChar |= (messageBit << bitPosition)

            # Update shift register : Shift left and add the ciphertext bit
            shiftRegister = ((shiftRegister << 1) | cipherBit) & 0x3FF

        result.append(chr(decryptedChar))

    return ''.join(result)

def generateKeyStream(k0, k1, length):
    keystream = [k0 % 26, k1 % 26]
    for i in range(2, length):
        key = (keystream[i-1] * keystream[i-2]) % 26
        keystream.append(key)
    return keystream

def syncCipherEncrypt(message, key):
    k0, k1 = key[0], key[1]
    result = []

    keystream = generateKeyStream(k0, k1, len(message))
    
    # Encryption
    for i, char in enumerate(message):
        if char.isalpha():
            # Convert to 0-25
            charValue = ord(char.upper()) - ord('A')
            encryptedValue = (charValue + keystream[i]) % 26 # Encryption: c_i = m_i + k_i mod 26
            if char.islower():
                result.append(chr(encryptedValue + ord('a')))
            else:
                result.append(chr(encryptedValue + ord('A')))
        else:
            result.append(char) # non alphabetic char remains unchanged

    return ''.join(result)

def syncCipherDecrypt(ciphertext, key):
    k0, k1 = key[0], key[1]
    result = []

    keystream = generateKeyStream(k0, k1, len(ciphertext))

    # Decryption
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            # Convert to 0-25
            charValue = ord(char.upper()) - ord('A')
            decryptedValue = (charValue - keystream[i]) % 26 # Encryption: c_i = m_i - k_i mod 26
            if char.islower():
                result.append(chr(decryptedValue + ord('a')))
            else:
                result.append(chr(decryptedValue + ord('A')))
        else:
            result.append(char)
    
    return ''.join(result)

def combinedEncryption(message, cfbKey, syncKey, iv):
    oddChars = ""
    evenChars = ""
    positions = {}

    # Separate odd and even position characters
    for i, char in enumerate(message):
        if (i + 1) % 2 == 1:
            oddChars += char
            positions[len(oddChars) - 1] = i
        else:
            evenChars += char
            positions[len(evenChars) - 1 + len(message)//2] = i
    
    # Encrypt odd chars with CFB
    oddEncryption = CFB1BitEncryption(oddChars, cfbKey, iv) if oddChars else ""

    # Encrypt even chars with synchronous cipher
    evenEncryption = syncCipherEncrypt(evenChars, syncKey) if evenChars else ""

    # Message reconstruction
    result = [''] * len(message)
    oddId = 0
    evenId = 0

    for i in range(len(message)):
        if (i + 1) % 2 == 1:
            result[i] = oddEncryption[oddId]
            oddId += 1
        else:
            result[i] = evenEncryption[evenId]
            evenId += 1
    
    return ''.join(result)

def combinedDecryption(cipherText, cfbKey, syncKey, iv):
    oddChars = ""
    evenChars = ""

    # Seperate odd and even position characters
    for i, char in enumerate(cipherText):
        if (i + 1) % 2 == 1:
            oddChars += char
        else:
            evenChars += char

    # Decrypt odd chars with CFB
    oddDecryption = CFB1BitDecryption(oddChars, cfbKey, iv) if oddChars else ""

    # Decrypt even chars with synchronous cipher
    evenDecryption = syncCipherDecrypt(evenChars, syncKey) if evenChars else ""

    # Message reconstruction
    result = [''] * len(cipherText)
    oddId = 0
    evenId = 0
    for i in range(len(cipherText)):
        if (i + 1) % 2 == 1:
            result[i] = oddDecryption[oddId]
            oddId += 1
        else:
            result[i] = evenDecryption[evenId]
            evenId += 1

    return ''.join(result)

def main():
    message = "TESTING ENCRYPTION AND DECRYPTION SAMPLE MESSAGE"

    # Keys 
    cfbKeys = [0x12, 0x34, 0x56, 0x78] # for TEA encryption/decryption
    syncKeys = [7, 11, 13, 17] # k0 = 7, k1 = 11
    iv = 0x1A3 # initial vector for CFB

    print(f"Original Message: [{message}]")
    print(f"Original Mesasge Length: [{len(message)}]")
    print()

    print(f"Original Character Positions: ")
    for i, char in enumerate(message):
        positionType = "odd" if (i + 1) % 2 == 1 else "even"
        print(f"Position [{i + 1}] : {char} , {positionType}")
    print()

    # Encryption
    encrypted = combinedEncryption(message, cfbKeys, syncKeys, iv)
    print(f"Encrypted Message: {encrypted}")
    print()

    # Decryption
    decryption = combinedDecryption(encrypted, cfbKeys, syncKeys, iv)
    print(f"Decrypted Message: {decryption}")

    print("Encryption/Decryption successful:", message == decryption)

def testing():

    print("=== Testing Individual Components ===")
    
    # Test 1: Synchronous cipher with the example from Task 6
    print("\n1. Testing Synchronous Cipher:")
    test_msg = "ILOVEWOLLONGONG"
    sync_test_key = [7, 11]
    
    print(f"Message: {test_msg}")
    print(f"Key: k0={sync_test_key[0]}, k1={sync_test_key[1]}")
    
    # Show keystream generation
    keystream = generateKeyStream(7, 11, len(test_msg))
    print(f"Keystream: {keystream}")
    
    encrypted_sync = syncCipherEncrypt(test_msg, sync_test_key)
    decrypted_sync = syncCipherDecrypt(encrypted_sync, sync_test_key)
    
    print(f"Encrypted: {encrypted_sync}")
    print(f"Decrypted: {decrypted_sync}")
    print(f"Success: {test_msg == decrypted_sync}")
    
    # Test 2: 1-bit CFB
    print("\n2. Testing 1-bit CFB:")
    cfb_test_msg = "ABC"
    cfb_test_key = [0x12, 0x34, 0x56, 0x78]
    cfb_test_iv = 0x1A3
    
    print(f"Message: {cfb_test_msg}")
    print(f"Key: {[hex(k) for k in cfb_test_key]}")
    print(f"IV: {hex(cfb_test_iv)}")
    
    encrypted_cfb = CFB1BitEncryption(cfb_test_msg, cfb_test_key, cfb_test_iv)
    decrypted_cfb = CFB1BitDecryption(encrypted_cfb, cfb_test_key, cfb_test_iv)
    
    print(f"Encrypted: {[hex(ord(c)) for c in encrypted_cfb]}")
    print(f"Decrypted: {decrypted_cfb}")
    print(f"Success: {cfb_test_msg == decrypted_cfb}")
    
    # Debug CFB step by step for first character
    print(f"\nDetailed CFB debug for first character '{cfb_test_msg[0]}':")
    debug_char = cfb_test_msg[0]
    debug_char_val = ord(debug_char)
    debug_shift_reg = cfb_test_iv & 0x3FF
    print(f"Character: '{debug_char}' = {debug_char_val} = {bin(debug_char_val)}")
    print(f"Initial shift register: {hex(debug_shift_reg)} = {bin(debug_shift_reg)}")
    
    for bit_pos in range(8):
        message_bit = (debug_char_val >> bit_pos) & 1
        encrypted_sr = TEA_encrypt(debug_shift_reg, cfb_test_key)
        key_bit = (encrypted_sr >> 9) & 1
        cipher_bit = message_bit ^ key_bit
        
        print(f"Bit {bit_pos}: msg_bit={message_bit}, TEA({hex(debug_shift_reg)})={hex(encrypted_sr)}, key_bit={key_bit}, cipher_bit={cipher_bit}")
        
        debug_shift_reg = ((debug_shift_reg << 1) | cipher_bit) & 0x3FF
    
    # Test 3: Combined system
    print("\n=== Testing Combined System ===")
    
    message = "HELLO WORLD"
    cfb_key = [0x12, 0x34, 0x56, 0x78]
    sync_key = [7, 11, 13, 17]
    iv = 0x1A3
    
    print(f"\nOriginal message: '{message}'")
    print(f"Message length: {len(message)}")
    
    # Show character positions
    print("\nCharacter positions:")
    for i, char in enumerate(message):
        pos_type = "odd (CFB)" if (i + 1) % 2 == 1 else "even (Sync)"
        print(f"Position {i+1}: '{char}' - {pos_type}")
    
    # Show what will be processed by each cipher
    odd_chars = "".join([message[i] for i in range(len(message)) if (i + 1) % 2 == 1])
    even_chars = "".join([message[i] for i in range(len(message)) if (i + 1) % 2 == 0])
    
    print(f"\nOdd positioned chars (1-bit CFB): '{odd_chars}'")
    print(f"Even positioned chars (Sync cipher): '{even_chars}'")
    
    # Encrypt
    encrypted = combinedEncryption(message, cfb_key, sync_key, iv)
    print(f"\nEncrypted message: '{encrypted}'")
    
    # Decrypt
    decrypted = combinedDecryption(encrypted, cfb_key, sync_key, iv)
    print(f"Decrypted message: '{decrypted}'")
    
    # Verify
    success = message == decrypted
    print(f"\nCombined system success: {success}")
    
    if not success:
        print("\nDebugging info:")
        print(f"Original:  {[ord(c) for c in message]}")
        print(f"Decrypted: {[ord(c) for c in decrypted]}")
        
        # Check individual components
        odd_encrypted = CFB1BitEncryption(odd_chars, cfb_key, iv)
        odd_decrypted = CFB1BitDecryption(odd_encrypted, cfb_key, iv)
        print(f"CFB test: '{odd_chars}' -> '{odd_decrypted}' (Success: {odd_chars == odd_decrypted})")
        
        even_encrypted = syncCipherEncrypt(even_chars, sync_key)
        even_decrypted = syncCipherDecrypt(even_encrypted, sync_key)
        print(f"Sync test: '{even_chars}' -> '{even_decrypted}' (Success: {even_chars == even_decrypted})")

if __name__ == "__main__":
    testing()