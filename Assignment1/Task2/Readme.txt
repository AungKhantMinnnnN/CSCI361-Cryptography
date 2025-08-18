This script, `Task2.py`, is a command-line tool for encrypting and decrypting text files using a keyword-based substitution cipher.

## Description

The script takes a keyword and generates a substitution cipher alphabet. The keyword (after removing duplicate letters) forms the beginning of the cipher alphabet, and the remaining letters of the alphabet are appended in reverse order. This cipher is then used to encrypt or decrypt a specified input file, with the result written to an output file.

## Usage

To use the script, run it from the command line with the following syntax:

```
python Task2.py -k <keyword> (-e <input_file> | -d <input_file>) -o <output_file>
```

### Arguments

- `-k`, `--keyword`: (Required) The keyword to generate the substitution cipher. It must only contain alphabetic characters.
- `-e`, `--encrypt`: (Required for encryption) The path to the input file to be encrypted.
- `-d`, `--decrypt`: (Required for decryption) The path to the input file to be decrypted.
- `-o`, `--output`: (Required) The path to the output file where the result will be saved.

**Note:** You must specify either `-e` for encryption or `-d` for decryption, but not both.

## Examples

### Encryption

To encrypt a file named `input.txt` with the keyword `STRAWBERRY` and save the result to `encrypted.txt`:

```
python Task2.py -k STRAWBERRY -e input.txt -o encrypted.txt
```

### Decryption

To decrypt a file named `encrypted.txt` with the same keyword `STRAWBERRY` and save the result to `decrypted.txt`:

```
python Task2.py -k STRAWBERRY -d encrypted.txt -o decrypted.txt
```
