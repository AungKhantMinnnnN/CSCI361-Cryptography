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

if __name__ == "__main__":
    main()