#!/bin/bash

# This script automates the setup process for the Ring Signature project.

# Detect the operating system
OS="$(uname -s)"

case "$OS" in
    Linux*)
        echo "Detected Linux."
        echo "Installing dependencies..."
        make install-deps
        ;;
    Darwin*)
        echo "Detected macOS."
        echo "Installing dependencies..."
        make install-deps
        ;;
    CYGWIN*|MINGW*|MSYS*)
        echo "Detected Windows."
        echo "Installing dependencies..."
        make install-deps
        ;;
    *)
        echo "Unsupported operating system: $OS"
        exit 1
        ;;
esac

# Build the project
echo "Building the project..."
make

echo "Setup complete."
