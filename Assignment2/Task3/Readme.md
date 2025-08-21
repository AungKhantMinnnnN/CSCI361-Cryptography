# SHA-1 Collision Finder

This program demonstrates a birthday attack to find a collision for a simplified SHA-1 hash function (SSHA-1). The SSHA-1 hash is the first 34 bits of the standard SHA-1 hash.

## Prerequisites

This program requires the OpenSSL library to be installed.

-   **Ubuntu/Debian:** `sudo apt-get install libssl-dev`
-   **macOS (with Homebrew):** `brew install openssl`
-   **Windows (with MSYS2/MinGW):** `pacman -S mingw-w64-x86_64-openssl`

## How to Compile and Run

### Using Makefile (macOS/Linux)

The provided makefile will automatically detect the operating system and use the correct flags.

1.  **Compile the code:**
    ```bash
    make
    ```
2.  **Run the program:**
    ```bash
    ./sha1_collision
    ```
3.  **Clean up generated files:**
    ```bash
    make clean
    ```

### Using setup.sh (macOS/Linux)

1.  **Give execute permission to the script:**
    ```bash
    chmod +x setup.sh
    ```
2.  **Run the script to compile:**
    ```bash
    ./setup.sh
    ```
3.  **Run the program:**
    ```bash
    ./sha1_collision
    ```

### For Windows

1.  **Compile the code using g++:**
    ```bash
    g++ -o sha1_collision.exe ssha1.cpp -lssl -lcrypto
    ```
2.  **Run the program:**
    ```bash
    ./sha1_collision.exe
    ```

## Program Logic

The program searches for a collision by hashing two similar message templates:

-   `Donald Trump owes Aung Khant Min x dollars`
-   `Donald Trump owes Aung Khant Min x' dollars`

It iteratively replaces `x` and `x'` with integer values, calculates the SSHA-1 hash for each message, and stores them in a hash table. A collision is found when two different messages produce the same 34-bit hash value.