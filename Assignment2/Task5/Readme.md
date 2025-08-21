# Fast Exponentiation Calculator

This program calculates modular exponentiation (a^b mod p) using the fast exponentiation algorithm, also known as the square-and-multiply method. It provides a step-by-step breakdown of the calculation.

## How to Compile and Run

### Using Makefile (macOS/Linux)

1.  **Compile the code:**
    ```bash
    make
    ```
2.  **Run the program:**
    ```bash
    ./FastExponent
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
    ./FastExponent
    ```

### For Windows

1.  **Compile the code using g++:**
    ```bash
    g++ -o FastExponent.exe FastExponent.cpp
    ```
2.  **Run the program:**
    ```bash
    ./FastExponent.exe
    ```

## Program Usage

When you run the program, it will prompt you to enter:

-   The base `a`
-   The exponent `b`
-   The modulus `p`

The program will then display the steps to compute `a^b mod p` and print the final result.
