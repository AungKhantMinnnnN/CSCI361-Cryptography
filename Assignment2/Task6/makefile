# Makefile for Lehman Primality Test

# Compiler
CXX = g++

# Compiler flags
CXXFLAGS = -std=c++11 -Wall

# Target executable
TARGET = LehmanAlgorithm

# Source file
SRC = LehmanAlgorithm.cpp

# Default rule
all: $(TARGET)

# Rule to build the target
$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

# Clean rule
clean:
	rm -f $(TARGET)

.PHONY: all clean
