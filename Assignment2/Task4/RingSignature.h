#ifndef RING_SIGNATURE_H
#define RING_SIGNATURE_H

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <random>
#include <iomanip>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <openssl/sha.h>
#include <openssl/aes.h>
#include <openssl/rand.h>
#include <openssl/evp.h>
#include <openssl/bn.h>

using namespace std;

class RingSignature{
    private:
        struct RSAKeyPair{
            BIGNUM *e; // public exponent
            BIGNUM *n; // modulus
            BIGNUM *d; // private exponent ( only to be used by sender )

            RSAKeyPair() : e(nullptr), n(nullptr), d(nullptr) {}
            ~RSAKeyPair(){
                if (e) BN_free(e);
                if (n) BN_free(n);
                if (d) BN_free(d);
            }
        };

        vector<RSAKeyPair*> publicKeys;
        RSAKeyPair* signerPrivateKey;
        int signerIndex;

        // AES encryption and decryption functions
        string aesEncrypt(const string& plaintext, const unsigned char* key);
        string aesDecrypt(const string& ciphertext, const unsigned char* key);

        // Hash function using SHA-256
        string hash(const string& input);

        // RSA operation functions using BIGNUM
        BIGNUM* rsaOperation(BIGNUM* message, BIGNUM* exponent, BIGNUM* modulus);
    
    public:
        RingSignature();
        ~RingSignature();

        // Function: load public keys from file
        bool loadPublicKeys(const string& filename);

        // Function: generate ring signature for message
        string generateRingSignature(const string& message);

        // Function: verify ring signature
        bool verifyRingSignature(const string& signature, const string& publicKeyFile);

        // Function: set signer index
        void setSignerIndex(int index);
};

// utils
string readFile(const string& filename);
bool writeFile(const string& filename, const string& message);

#endif