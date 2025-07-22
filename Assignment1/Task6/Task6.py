def characterToNumber(char):
    return ord(char) - ord('A')

def numberToCharacter(number):
    return chr((number % 26) + ord('A'))

def generateKeyStream(k0,  k1, length):
    keys = [k0, k1]
    for i in range(2, length):
        nextKey = (keys[-1] + keys[-2]) % 26
        keys.append(nextKey)
    return keys

def encryption(plainText, k0, k1):
    plainText = plainText.replace(" ", "").upper()
    m = [characterToNumber(char) for char in plainText]
    key = generateKeyStream(k0, k1, len(m))
    cipher = [(m[i] + key[i]) % 26 for i in range(len(m))]
    return ''.join(numberToCharacter(ci) for ci in cipher)

def decryption(cipherText, k0, k1):
    cipherText = cipherText.replace(" ", "").upper()
    cipher = [characterToNumber(char) for char in cipherText]
    key = generateKeyStream(k0, k1, len(cipher))
    m = [(cipher[i] - key[i]) % 26 for i in range(len(cipher))]
    return ''.join(numberToCharacter(mi) for mi in m)

def main():
    # Encryption of "I LOVE WOLLONGONG" with K0 = 7, K1 = 11
    print("Encryption of I LOVE WOLLONGONG with K0 = 7 and K1 = 11")
    print(encryption("I LOVE WOLLONGONG", 7, 11))

    # Decryption of "MQJJ" with K0 = 7 and K1 = 11
    print("Decryption of MQJJ with K0 = 7 and K1 = 11")
    print(decryption("MQJJ", 7, 11))

if __name__ == "__main__":
    main()