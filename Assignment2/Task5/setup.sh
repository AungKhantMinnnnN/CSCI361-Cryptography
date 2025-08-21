#!/bin/bash

# This script compiles the FastExponent.cpp file using g++

echo "Compiling FastExponent.cpp..."
g++ -std=c++11 -o FastExponent FastExponent.cpp

if [ $? -eq 0 ]; then
    echo "Compilation successful. Run with ./FastExponent"
else
    echo "Compilation failed."
fi
