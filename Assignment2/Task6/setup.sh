#!/bin/bash

# This script compiles the LehmanAlgorithm.cpp file using g++

echo "Compiling LehmanAlgorithm.cpp..."
g++ -std=c++11 -o LehmanAlgorithm LehmanAlgorithm.cpp

if [ $? -eq 0 ]; then
    echo "Compilation successful. Run with ./LehmanAlgorithm"
else
    echo "Compilation failed."
fi
