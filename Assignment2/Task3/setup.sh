#!/bin/bash

# This script compiles the ssha1.cpp file

# Detect OS
if [[ "$(uname)" == "Darwin" ]]; then
    # macOS
    echo "Compiling for macOS..."
    clang++ -std=c++11 -O2 -o sha1_collision ssha1.cpp \
    -I$(brew --prefix openssl)/include \
    -L$(brew --prefix openssl)/lib \
    -lssl -lcrypto
else
    # Linux
    echo "Compiling for Linux..."
    g++ -o sha1_collision ssha1.cpp -lssl -lcrypto
fi

if [ $? -eq 0 ]; then
    echo "Compilation successful. Run with ./sha1_collision"
else
    echo "Compilation failed. Make sure OpenSSL is installed."
fi

