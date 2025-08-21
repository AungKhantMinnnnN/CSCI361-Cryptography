# Knapsack Cryptosystem

This program implements the knapsack cryptosystem for educational purposes. It allows users to define a private key (a super-increasing knapsack), generate a corresponding public key, and then perform encryption and decryption of messages.

## How to Compile and Run

### Using Makefile (macOS/Linux)

1.  **Compile the code:**
    ```bash
    make
    ```
2.  **Run the program:**
    ```bash
    ./knapsack
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
    ./knapsack
    ```

### For Windows

1.  **Compile the code using g++:**
    ```bash
    g++ -o knapsack.exe knapsack.cpp
    ```
2.  **Run the program:**
    ```bash
    ./knapsack.exe
    ```

## Program Flow

1.  **Setup Phase:**
    *   The user is prompted to enter the size of the super-increasing knapsack.
    *   The user enters the elements of the private key, which must form a super-increasing sequence.
    *   The user provides a modulus and a multiplier, which are used to transform the private key into a public key. The program validates these inputs.
    *   The public key is generated and displayed.

2.  **Encryption:**
    *   The user enters a message to be encrypted.
    *   The message is converted into a sequence of ciphertext blocks using the public key.

3.  **Decryption:**
    *   The user enters the ciphertext blocks.
    *   The program uses the private key and the original modulus and multiplier to decrypt the ciphertext and recover the original message.
