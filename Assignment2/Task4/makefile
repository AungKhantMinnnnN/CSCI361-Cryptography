CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra

# Detect operating system
UNAME_S := $(shell uname -s)

# Default OpenSSL paths
OPENSSL_CFLAGS = -I/usr/local/include
OPENSSL_LIBS = -L/usr/local/lib -lssl -lcrypto

# macOS specific OpenSSL paths
ifeq ($(UNAME_S),Darwin)
    HOMEBREW_PREFIX := $(shell brew --prefix 2>/dev/null || echo "/usr/local")
    OPENSSL_PREFIX := $(shell brew --prefix openssl@3 2>/dev/null || brew --prefix openssl 2>/dev/null || echo "$(HOMEBREW_PREFIX)/opt/openssl")
    ifneq (,$(wildcard $(OPENSSL_PREFIX)/include/openssl/ssl.h))
        OPENSSL_CFLAGS = -I$(OPENSSL_PREFIX)/include
        OPENSSL_LIBS = -L$(OPENSSL_PREFIX)/lib -lssl -lcrypto
    else
        OPENSSL_CFLAGS = $(shell pkg-config --cflags openssl 2>/dev/null || echo "-I/opt/homebrew/include -I/usr/local/include")
        OPENSSL_LIBS = $(shell pkg-config --libs openssl 2>/dev/null || echo "-L/opt/homebrew/lib -L/usr/local/lib -lssl -lcrypto")
    endif
endif

# Windows (MSYS2/MinGW) specific OpenSSL paths
ifeq ($(findstring MINGW,$(UNAME_S)),MINGW)
    OPENSSL_CFLAGS = -I/mingw64/include
    OPENSSL_LIBS = -L/mingw64/lib -lssl -lcrypto
endif

CXXFLAGS += $(OPENSSL_CFLAGS)
LIBS = $(OPENSSL_LIBS)

# Object files
COMMON_OBJ = RingSignature.o

# Targets
all: sign verify

sign: $(COMMON_OBJ) sign.o
	$(CXX) $(CXXFLAGS) -o sign $(COMMON_OBJ) sign.o $(LIBS)

verify: $(COMMON_OBJ) verify.o
	$(CXX) $(CXXFLAGS) -o verify $(COMMON_OBJ) verify.o $(LIBS)

# Object file compilation
RingSignature.o: RingSignature.cpp RingSignature.h
	$(CXX) $(CXXFLAGS) -c RingSignature.cpp

sign.o: sign.cpp RingSignature.h
	$(CXX) $(CXXFLAGS) -c sign.cpp

verify.o: verify.cpp RingSignature.h
	$(CXX) $(CXXFLAGS) -c verify.cpp

# Clean target
clean:
	rm -f *.o sign verify

# Install dependencies
install-deps:
ifeq ($(UNAME_S),Darwin)
	@echo "Installing dependencies for macOS..."
	brew install openssl
else ifeq ($(findstring MINGW,$(UNAME_S)),MINGW)
	@echo "Installing dependencies for Windows (MSYS2/MinGW)..."
	pacman -S --noconfirm mingw-w64-x86_64-openssl
else
	@echo "Installing dependencies for Linux..."
	@if [ -f /etc/debian_version ]; then \
		sudo apt-get update && sudo apt-get install -y libssl-dev; \
	elif [ -f /etc/redhat-release ]; then \
		sudo yum install -y openssl-devel; \
	else \
		echo "Unsupported Linux distribution. Please install OpenSSL manually."; \
	fi
endif

.PHONY: all clean install-deps
