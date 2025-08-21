# Makefile for SHA-1 Collision Finder

# Target executable
TARGET = sha1_collision

# Source file
SRC = ssha1.cpp

# Default compiler
CXX = g++

# Default flags
CXXFLAGS = -std=c++11 -Wall
LIBS = -lssl -lcrypto

# OS-specific settings
UNAME_S := $(shell uname -s)

ifeq ($(UNAME_S),Darwin)
    # macOS
    BREW_PREFIX := $(shell brew --prefix openssl)
    CXX = clang++
    CXXFLAGS += -O2 -I$(BREW_PREFIX)/include
    LDFLAGS = -L$(BREW_PREFIX)/lib
else ifeq ($(UNAME_S),Linux)
    # Linux
    # No special flags needed if libssl-dev is installed
else
    # Assume Windows/other
    TARGET := $(TARGET).exe
endif

# Default rule
all: $(TARGET)

# Rule to build the target
$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $@ $(SRC) $(LDFLAGS) $(LIBS)

# Clean rule
clean:
	rm -f $(TARGET) sha1_collision.exe

.PHONY: all clean
