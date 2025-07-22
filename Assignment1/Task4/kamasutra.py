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
    
    for i in range(keyLength // 2):
        first = key[i].lower()
        second = key[keyLength - 1 - i].lower()
        
        if 'a' <= first <= 'z' and 'a' <= second <= 'z':
            cipherMap[first] = second
            cipherMap[second] = first
    
    # Handle middle character for odd-length keys (maps to itself)
    if keyLength % 2 == 1:
        middle_char = key[keyLength // 2].lower()
        if 'a' <= middle_char <= 'z':
            cipherMap[middle_char] = middle_char

    return cipherMap

def encryption(inputFile, outputFile, key):
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
                if char == 'f' or char == 'F' or char == 'u' or char == 'U':
                    out_file.write(char)
                elif char.islower():
                    out_file.write(cipherMapping.get(char, char))
                elif char.isupper():
                    lowerChar = char.lower()
                    mappedChar = cipherMapping.get(lowerChar, lowerChar)
                    out_file.write(mappedChar.upper())
                else:
                    out_file.write(char)
            print(f"Encryption complete: {inputFile} -> {outputFile}")
    except IOError as e:
        print(f"Error: Cannot create output file {outputFile} - {e}", file=sys.stderr)
        sys.exit(1)

def decryption(inputFile, outputFile, key):
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
                if char == 'f' or char == 'F' or char == 'u' or char == 'U':
                    out_file.write(char)
                elif char.islower():
                    out_file.write(cipherMapping.get(char, char))
                elif char.isupper():
                    lowerChar = char.lower()
                    mappedChar = cipherMapping.get(lowerChar, lowerChar)
                    out_file.write(mappedChar.upper())
                else:
                    out_file.write(char)
            print(f"Decryption complete: {inputFile} -> {outputFile}")
    except IOError as e:
        print(f"Error: Cannot create output file {outputFile} - {e}", file=sys.stderr)
        sys.exit(1)

def encryptText(keyfile, plainTextFile, cipherTextFile):
    key = readKeyfile(keyfile)
    encryption(plainTextFile, cipherTextFile, key)
def decryptText(keyfile, cipherTextFile, plainTextFile):
    key = readKeyfile(keyfile)
    decryption(cipherTextFile, plainTextFile, key)

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