#!/bin/bash

# This script compiles the knapsack.cpp file using g++

echo "Compiling knapsack.cpp..."
g++ -std=c++11 -o knapsack knapsack.cpp

if [ $? -eq 0 ]; then
    echo "Compilation successful. Run with ./knapsack"
else
    echo "Compilation failed."
fi
