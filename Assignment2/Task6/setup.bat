@echo off
REM This script compiles the LehmanAlgorithm.cpp file using g++

echo "Compiling LehmanAlgorithm.cpp..."
g++ -std=c++11 -o LehmanAlgorithm.exe LehmanAlgorithm.cpp

if %errorlevel% equ 0 (
    echo "Compilation successful. Run with LehmanAlgorithm.exe"
) else (
    echo "Compilation failed."
)
