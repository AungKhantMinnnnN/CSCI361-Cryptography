# Lehman Primality Test

This program implements the Lehman primality test, a probabilistic algorithm to determine if a number is prime.

## How to Compile and Run

### Using Makefile (macOS/Linux)

1.  **Compile the code:**
    ```bash
    make
    ```
2.  **Run the program:**
    ```bash
    ./LehmanAlgorithm
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
    ./LehmanAlgorithm
    ```

### For Windows

1.  **Compile the code using g++:**
    ```bash
    g++ -o LehmanAlgorithm.exe LehmanAlgorithm.cpp
    ```
2.  **Run the program:**
    ```bash
    ./LehmanAlgorithm.exe
    ```

## Program Usage

When you run the program, it will prompt you to enter a number to test for primality. The program will then run the Lehman test and print whether the number is likely prime or composite. It also runs a set of predefined test cases for demonstration.
