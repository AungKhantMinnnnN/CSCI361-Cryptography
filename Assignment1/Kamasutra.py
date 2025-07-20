import sys
import os

def generateKeypair(keyfile):
    # Generate a keyfile with the default alphabet
    try:
        with open(keyfile,'w') as f:
            f.write("abcdefghijklmnopqrstuvwxyz\n")
        print(f"Keyfile has been generated. {keyfile}")
    except IOError as e:
        print(f"Error: Cannot create keyfile {keyfile}. {e}")
        sys.exit(1)

def readKeyfile(keyfile):
    # Read the key from the keyfile
    try:
        with open(keyfile, 'r') as f:
            key = f.readline().strip()
        return key
    except IOError as e:
        print(f"Error: Cannot open keyfile {keyfile}. {e}")
        sys.exit(1)

def createCipherMapping(key):
    cipherMap = {}
    keyLength = len(key)
    
    # Initialize identity mapping
    for i in range(26):
        char = chr(ord('a') + i)
        cipherMap[char] = char
    
    # Create pairing based on key
    for i in range(keyLength // 2):
        first = key[i].lower()
        second = key[keyLength - 1 - i].lower()

        if 'a' <= first <= 'z' and 'a' <= second <= 'z':
            cipherMap[first] = second
            cipherMap[second] = first

    return cipherMap

def transformText(inputFile, outputFile, key, encryptMode = True):
    # Encrypt or decrypt text using the flipped kamasutra cipher
    try:
        with open(inputFile, 'r') as in_file:
            text = in_file.read()
    except IOError as e:
        print(f"Error: Cannot open input file {inputFile}. {e}")
        sys.exit(1)

    try:
        with open(outputFile, 'w') as out_file:
            cipherMapping = createCipherMapping(key)

            for char in text:
                if char == 'f' or char == 'F':
                    out_file.write(char)
                elif char.islower():
                    out_file.write(cipherMapping.get(char, char))
                elif char.isupper():
                    lowerChar = char.lower()
                    mappedChar = cipherMapping.get(lowerChar, lowerChar)
                    out_file.write(mappedChar.upper())
                else:
                    out_file.write(char)
        operation = "Encryption" if encryptMode else "Decryption"
        print(f"{operation} complete. {inputFile} -> {outputFile}")
    except IOError as e:
        print(f"Error: An error has occurred while creating output file {outputFile}. {e}")
        sys.exit(1)

def encryptText(keyfile, plainTextFile, cipherTextFile):
    key = readKeyfile(keyfile)
    transformText(plainTextFile, cipherTextFile, key, encryptMode=True)

def decryptText(keyfile, cipherTextFile, plainTextFile):
    key = readKeyfile(keyfile)
    transformText(cipherTextFile, plainTextFile, key, encryptMode=False)

def main():
    if len(sys.argv) < 3:
        print("Please include all the required arguments to run the program.")
        program_name = sys.argv[0]
        print("Usage:")
        print(f"  {program_name} -k <keyfile.txt>")
        print(f"  {program_name} -e <keyfile.txt> <plaintext.txt> <ciphertext.txt>")
        print(f"  {program_name} -d <keyfile.txt> <ciphertext.txt> <plaintext.txt>")
        sys.exit(1)
    
    option = sys.argv[1]

    if option == '-k':
        if len(sys.argv) != 3:
            print(f"Error: -k option requires keyfile name.")
            sys.exit(1)
        generateKeypair(sys.argv[2])

    elif option == '-e':
        if len(sys.argv) != 5:
            print(f"Error: -e option requires keyfile, plaintext file and ciphertext file")
            sys.exit(1)
        encryptText(sys.argv[2], sys.argv[3], sys.argv[4])

    elif option == "-d":
        if len(sys.argv) != 5:
            print("Error: -d option requires keyfile, ciphertext file, and plaintext file", file=sys.stderr)
            sys.exit(1)
        decryptText(sys.argv[2], sys.argv[3], sys.argv[4])
    
    else:
        print(f"Error: Unknown option {option}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()