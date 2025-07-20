import sys
import argparse
import os

# Assignment 1 Task 2

#region Common Functions
def removeDuplicateCharacters(keyword:str) -> str:
    seenChars = set()
    result = []
    for char in keyword.upper():
        if char not in seenChars and char.isalpha():
            seenChars.add(char)
            result.append(char)
    return ''.join(result)

def validateKeyword(keyword:str) -> str:
    if not keyword:
        return False
    return all(char.isalpha() for char in keyword)
#endregion

#region File manipulation functions
def readFile(filename:str) -> str:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f'Error: File: {filename} not found', file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading file '{filename}'.", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file '{filename}'. Please ensure it's a text file.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}", file=sys.stderr)
        sys.exit(1)

def writeFile(filename:str, content:str) -> None:
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Output written to {filename}')
    except PermissionError:
        print(f"Error: Permission denied writing to file '{filename}'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error writing to file '{filename}': {e}", file=sys.stderr)
        sys.exit(1)
#endregion

#region Encryption and Decryption functions
def generateCipherKey(keyword:str) -> dict[str, str]:
    cleanedKeyword = removeDuplicateCharacters(keyword)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    remainingChars = []
    for char in reversed(alphabet):
        if char not in cleanedKeyword:
            remainingChars.append(char)
    
    cipherAlphabet = cleanedKeyword + ''.join(remainingChars)
    cipherKey = {}
    for i, char in enumerate(alphabet):
        cipherKey[char] = cipherAlphabet[i]
    
    return cipherKey

def generateDecipherKey(cipherKey: dict[str, str]) -> dict[str, str]:
    return {v: k for k, v in cipherKey.items()}

def encryptMessage(message: str, cipherKey: dict[str, str]) -> str:
    encrypted = []
    for char in message:
        if char.upper() in cipherKey:
            #Preserve case
            if char.isupper():
                encrypted.append(cipherKey[char.upper()])
            else:
                encrypted.append(cipherKey[char.upper()].lower())
        else:
            #Keep non alphabethic characters
            encrypted.append(char)
    return ''.join(encrypted)

def decryptMessage(cipherText:str, decipherKey: dict[str, str]) -> str:
    decrypted = []
    for char in cipherText:
        if char.upper() in decipherKey:
            if char.isupper():
                decrypted.append(decipherKey[char.upper()])
            else:
                decrypted.append(decipherKey[char.upper()].lower())
        else:
            decrypted.append(char)
    return ''.join(decrypted)
#endregion

def main():

    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt messages using a keyword-based substitution cipher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
        # Encrypt a message
        python cipher.py -k STRAWBERRY -e input.txt -o encrypted.txt
        
        # Decrypt a message
        python cipher.py -k STRAWBERRY -d encrypted.txt -o decrypted.txt
        """
    )

    parser.add_argument('-k', '--keyword', required=True,
                        help='Keyword for the substitution cipher')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--encrypt', metavar='INPUT_FILE', help='Encrypt the specified file.')
    group.add_argument('-d', '--decrypt', metavar='INPUT_FILE', help='Decrypt the specified file')
    parser.add_argument('-o', '--output', required=True, help='Output file for the result.')

    args = parser.parse_args()

    if not validateKeyword(args.keyword):
        print("Error: Keyword must contain only alphabetic characters.", file=sys.stderr)
        sys.exit(1)
    
    cipherKey = generateCipherKey(args.keyword)

    try:
        if args.encrypt:
            print(f"Encrypting '{args.encrypt}' with keyword '{args.keyword}'")
            plainText = readFile(args.encrypt)
            cipherText = encryptMessage(plainText, cipherKey)
            writeFile(args.output, cipherText)
        elif args.decrypt:
            print(f"Decrypting '{args.decrypt} with keyword '{args.keyword}''")
            cipherText = readFile(args.decrypt)
            decipherKey = generateDecipherKey(cipherKey)
            plainText = decryptMessage(cipherText, decipherKey)
            writeFile(args.output, plainText)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()