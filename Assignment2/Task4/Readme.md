# Ring Signature Implementation

This project provides a C++ implementation of a ring signature scheme using OpenSSL for the underlying cryptographic operations.

## Features

- **Ring Signature Generation:** Create a ring signature for a message using a set of public keys.
- **Ring Signature Verification:** Verify a ring signature using the set of public keys.
- **Cross-Platform:** The code is written in standard C++ and can be compiled on macOS, Linux, and Windows (with MSYS2/MinGW).

## Prerequisites

- **g++:** A C++ compiler that supports C++11.
- **OpenSSL:** The OpenSSL library is required for the cryptographic operations.

Commands to install OpenSSL:

-   **Ubuntu/Debian:** `sudo apt-get install libssl-dev`
-   **macOS (with Homebrew):** `brew install openssl`
-   **Windows (with MSYS2/MinGW):** `pacman -S mingw-w64-x86_64-openssl`

To install dependencies, run the following command:
`./setup.sh`

## Building

To build the project, run the following command:

```bash make```

This will compile the source code and create two executables: `sign` and `verify`.

## Usage

### Signing

To sign a message, run the `sign` executable:

```./sign```

Input the message you want to sign in `message.txt`
This will create a file named `signature.txt` containing the ring signature.

### Verifying

To verify a signature, run the `verify` executable:

```./verify```

This will read the signature from `signature.txt` and the public keys from `publickey.txt` and print whether the signature is valid or not.

