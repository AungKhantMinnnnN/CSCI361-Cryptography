#include "RingSignature.h"

RingSignature::RingSignature() : signerPrivateKey(nullptr), signerIndex(-1) {}

RingSignature::~RingSignature()
{
    for (auto key : publicKeys)
    {
        delete key;
    }
    if (signerPrivateKey && signerPrivateKey != publicKeys[signerIndex])
    {
        delete signerPrivateKey;
    }
}

std::string RingSignature::aesEncrypt(const std::string &plaintext, const unsigned char *key)
{
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    unsigned char iv[16];
    RAND_bytes(iv, 16);

    EVP_EncryptInit_ex(ctx, EVP_aes_128_cbc(), nullptr, key, iv);

    unsigned char *ciphertext = new unsigned char[plaintext.length() + 16];
    int len;
    int ciphertext_len;

    EVP_EncryptUpdate(ctx, ciphertext, &len, (unsigned char *)plaintext.c_str(), plaintext.length());
    ciphertext_len = len;

    EVP_EncryptFinal_ex(ctx, ciphertext + len, &len);
    ciphertext_len += len;

    EVP_CIPHER_CTX_free(ctx);

    // Prepend IV to ciphertext
    std::string result((char *)iv, 16);
    result.append((char *)ciphertext, ciphertext_len);

    delete[] ciphertext;
    return result;
}

std::string RingSignature::aesDecrypt(const std::string &ciphertext, const unsigned char *key)
{
    if (ciphertext.length() < 16)
        return "";

    unsigned char iv[16];
    memcpy(iv, ciphertext.c_str(), 16);

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    EVP_DecryptInit_ex(ctx, EVP_aes_128_cbc(), nullptr, key, iv);

    unsigned char *plaintext = new unsigned char[ciphertext.length()];
    int len;
    int plaintext_len;

    EVP_DecryptUpdate(ctx, plaintext, &len,
                      (unsigned char *)ciphertext.c_str() + 16,
                      ciphertext.length() - 16);
    plaintext_len = len;

    EVP_DecryptFinal_ex(ctx, plaintext + len, &len);
    plaintext_len += len;

    EVP_CIPHER_CTX_free(ctx);

    std::string result((char *)plaintext, plaintext_len);
    delete[] plaintext;
    return result;
}

std::string RingSignature::hash(const std::string &input)
{
    unsigned char hash_output[SHA256_DIGEST_LENGTH];
    SHA256((unsigned char *)input.c_str(), input.length(), hash_output);

    std::stringstream ss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++)
    {
        ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash_output[i];
    }
    return ss.str();
}

BIGNUM *RingSignature::rsaOperation(BIGNUM *message, BIGNUM *exponent, BIGNUM *modulus)
{
    BN_CTX *ctx = BN_CTX_new();
    BIGNUM *result = BN_new();
    BN_mod_exp(result, message, exponent, modulus, ctx);
    BN_CTX_free(ctx);
    return result;
}

bool RingSignature::loadPublicKeys(const std::string &filename)
{
    std::ifstream file(filename);
    if (!file.is_open())
    {
        std::cerr << "Cannot open public key file: " << filename << std::endl;
        return false;
    }

    // Clear existing keys
    for (auto key : publicKeys)
    {
        delete key;
    }
    publicKeys.clear();
    signerPrivateKey = nullptr;
    signerIndex = -1;

    std::string line;
    int keyIndex = 0;
    while (std::getline(file, line) && keyIndex < 4)
    {
        // Skip empty lines and comments
        if (line.empty() || line[0] == '#')
        {
            continue;
        }

        // Parse e, n, d (d will be 0 for public keys)
        std::istringstream iss(line);
        std::string e_str, n_str, d_str;

        if (std::getline(iss, e_str, ',') &&
            std::getline(iss, n_str, ',') &&
            std::getline(iss, d_str))
        {

            // Remove any trailing comma from d_str
            if (!d_str.empty() && d_str.back() == ',')
            {
                d_str.pop_back();
            }

            // Trim whitespace
            e_str.erase(0, e_str.find_first_not_of(" \t\r\n"));
            e_str.erase(e_str.find_last_not_of(" \t\r\n") + 1);
            n_str.erase(0, n_str.find_first_not_of(" \t\r\n"));
            n_str.erase(n_str.find_last_not_of(" \t\r\n") + 1);
            d_str.erase(0, d_str.find_first_not_of(" \t\r\n"));
            d_str.erase(d_str.find_last_not_of(" \t\r\n") + 1);

            

            RSAKeyPair *key = new RSAKeyPair();

            // Convert hex strings to BIGNUM with error checking
            if (BN_hex2bn(&key->e, e_str.c_str()) == 0)
            {
                std::cerr << "Error: Invalid hex format for e in key " << keyIndex << std::endl;
                delete key;
                continue;
            }

            if (BN_hex2bn(&key->n, n_str.c_str()) == 0)
            {
                std::cerr << "Error: Invalid hex format for n in key " << keyIndex << std::endl;
                delete key;
                continue;
            }

            // For signing, we need the private key
            if (d_str != "0" && !d_str.empty())
            {
                if (BN_hex2bn(&key->d, d_str.c_str()) == 0)
                {
                    std::cerr << "Error: Invalid hex format for d in key " << keyIndex << std::endl;
                    delete key;
                    continue;
                }
                signerPrivateKey = key;
                signerIndex = keyIndex;
                
            }

            publicKeys.push_back(key);
            keyIndex++;
        }
        else
        {
            std::cerr << "Error: Invalid line format: " << line << std::endl;
        }
    }
    file.close();

    
    return keyIndex == 4;
}

void RingSignature::setSignerIndex(int index)
{
    if (index >= 0 && index < (int16_t)publicKeys.size() && publicKeys[index]->d != nullptr)
    {
        signerIndex = index;
        signerPrivateKey = publicKeys[index];
    }
}

std::string RingSignature::generateRingSignature(const std::string &message)
{
    

    if (signerIndex == -1 || signerPrivateKey == nullptr)
    {
        std::cerr << "No private key found for signing!" << std::endl;
        return "";
    }

    if (publicKeys.size() != 4)
    {
        std::cerr << "Need exactly 4 public keys, got " << publicKeys.size() << std::endl;
        return "";
    }

    

    // Generate AES key for symmetric encryption (10 rounds = AES-128)
    unsigned char aes_key[16];
    if (RAND_bytes(aes_key, 16) != 1)
    {
        std::cerr << "Failed to generate random AES key" << std::endl;
        return "";
    }

    

    // Encrypt the message
    std::string encrypted_message;
    try
    {
        encrypted_message = aesEncrypt(message, aes_key);
        
    }
    catch (...)
    {
        std::cerr << "AES encryption failed" << std::endl;
        return "";
    }

    // Convert AES key to BIGNUM for RSA operations
    BIGNUM *key_bn = BN_new();
    if (!key_bn || BN_bin2bn(aes_key, 16, key_bn) == nullptr)
    {
        std::cerr << "Failed to convert AES key to BIGNUM" << std::endl;
        if (key_bn)
            BN_free(key_bn);
        return "";
    }

    // Check key_bn is smaller than modulus
    if (BN_cmp(key_bn, signerPrivateKey->n) >= 0)
    {
        std::cout << "Warning: AES key larger than modulus, taking modulo" << std::endl;
        BN_CTX *ctx = BN_CTX_new();
        BN_mod(key_bn, key_bn, signerPrivateKey->n, ctx);
        BN_CTX_free(ctx);
    }

    

    // Generate random values for other ring members
    std::vector<BIGNUM *> r_values(4);
    std::vector<BIGNUM *> s_values(4);

    for (int i = 0; i < 4; i++)
    {
        r_values[i] = BN_new();
        s_values[i] = BN_new();

        if (!r_values[i] || !s_values[i])
        {
            std::cerr << "Failed to allocate BIGNUM for index " << i << std::endl;
            // Cleanup
            for (int j = 0; j <= i; j++)
            {
                if (r_values[j])
                    BN_free(r_values[j]);
                if (s_values[j])
                    BN_free(s_values[j]);
            }
            BN_free(key_bn);
            return "";
        }

        if (i != signerIndex)
        {
            // Generate random r and s for non-signers (smaller than modulus)
            if (BN_rand_range(r_values[i], publicKeys[i]->n) != 1 ||
                BN_rand_range(s_values[i], publicKeys[i]->n) != 1)
            {
                std::cerr << "Failed to generate random values for index " << i << std::endl;
                // Cleanup and return
                for (int j = 0; j < 4; j++)
                {
                    if (r_values[j])
                        BN_free(r_values[j]);
                    if (s_values[j])
                        BN_free(s_values[j]);
                }
                BN_free(key_bn);
                return "";
            }
        }
    }

    

    // Create simplified ring signature (for demonstration)
    // This is a simplified version - a real implementation would be more complex

    // For the signer, we'll use a simple approach:
    // r_signer = key_encrypted mod n
    // s_signer = hash(message + r_values) mod n

    BIGNUM *key_encrypted = rsaOperation(key_bn, signerPrivateKey->d, signerPrivateKey->n);
    if (!key_encrypted)
    {
        std::cerr << "RSA operation failed" << std::endl;
        // Cleanup
        for (int i = 0; i < 4; i++)
        {
            BN_free(r_values[i]);
            BN_free(s_values[i]);
        }
        BN_free(key_bn);
        return "";
    }

    // Set signer's r value
    BN_copy(r_values[signerIndex], key_encrypted);

    // Create hash input from message and r values
    std::string hash_input = encrypted_message;
    for (int i = 0; i < 4; i++)
    {
        char *r_hex = BN_bn2hex(r_values[i]);
        if (r_hex)
        {
            hash_input += r_hex;
            OPENSSL_free(r_hex);
        }
    }

    // Hash and set signer's s value
    std::string challenge_hash = hash(hash_input);
    BIGNUM *challenge = BN_new();
    if (BN_hex2bn(&challenge, challenge_hash.substr(0, 32).c_str()) == 0)
    {
        std::cerr << "Failed to create challenge BIGNUM" << std::endl;
        // Cleanup
        for (int i = 0; i < 4; i++)
        {
            BN_free(r_values[i]);
            BN_free(s_values[i]);
        }
        BN_free(key_bn);
        BN_free(key_encrypted);
        BN_free(challenge);
        return "";
    }

    BN_CTX *ctx = BN_CTX_new();
    BN_mod(s_values[signerIndex], challenge, publicKeys[signerIndex]->n, ctx);
    BN_CTX_free(ctx);

    

    // Format signature
    std::stringstream signature;
    signature << "RING_SIG:";

    // Add encrypted message (hex encoded)
    for (unsigned char c : encrypted_message)
    {
        signature << std::hex << std::setw(2) << std::setfill('0') << (unsigned char)c;
    }
    signature << ":";

    // Add ring signature values
    for (int i = 0; i < 4; i++)
    {
        char *r_hex = BN_bn2hex(r_values[i]);
        char *s_hex = BN_bn2hex(s_values[i]);
        if (r_hex && s_hex)
        {
            signature << r_hex << "," << s_hex;
            if (i < 3)
                signature << ":";
        }

        if (r_hex)
            OPENSSL_free(r_hex);
        if (s_hex)
            OPENSSL_free(s_hex);
    }

    // Cleanup
    for (int i = 0; i < 4; i++)
    {
        BN_free(r_values[i]);
        BN_free(s_values[i]);
    }
    BN_free(key_bn);
    BN_free(key_encrypted);
    BN_free(challenge);

    
    return signature.str();
}

bool RingSignature::verifyRingSignature(const std::string &signature, const std::string &publicKeyFile)
{
    // Load public keys for verification
    if (!loadPublicKeys(publicKeyFile))
    {
        return false;
    }

    // Parse signature
    if (signature.substr(0, 9) != "RING_SIG:")
    {
        std::cerr << "Invalid signature format" << std::endl;
        return false;
    }

    std::string sig_data = signature.substr(9);
    std::vector<std::string> parts;
    std::stringstream ss(sig_data);
    std::string item;

    while (std::getline(ss, item, ':'))
    {
        parts.push_back(item);
    }

    if (parts.size() != 5)
    { // encrypted_message + 4 ring members
        std::cerr << "Invalid signature structure" << std::endl;
        return false;
    }

    // Decode encrypted message
    std::string encrypted_message;
    for (size_t i = 0; i < parts[0].length(); i += 2)
    {
        std::string hex_byte = parts[0].substr(i, 2);
        encrypted_message += (char)std::stoi(hex_byte, nullptr, 16);
    }

    // Parse ring signature values
    std::vector<BIGNUM *> r_values(4);
    std::vector<BIGNUM *> s_values(4);

    for (int i = 0; i < 4; i++)
    {
        std::istringstream rs_stream(parts[i + 1]);
        std::string r_str, s_str;

        if (std::getline(rs_stream, r_str, ',') && std::getline(rs_stream, s_str))
        {
            r_values[i] = BN_new();
            s_values[i] = BN_new();
            BN_hex2bn(&r_values[i], r_str.c_str());
            BN_hex2bn(&s_values[i], s_str.c_str());
        }
        else
        {
            // Cleanup and return false
            for (int j = 0; j <= i; j++)
            {
                if (r_values[j])
                    BN_free(r_values[j]);
                if (s_values[j])
                    BN_free(s_values[j]);
            }
            return false;
        }
    }

    BN_CTX *ctx = BN_CTX_new();
    if (!ctx) {
        std::cerr << "Failed to create BN_CTX" << std::endl;
        // Cleanup allocated BIGNUMs
        for (int i = 0; i < 4; i++) {
            if (r_values[i]) BN_free(r_values[i]);
            if (s_values[i]) BN_free(s_values[i]);
        }
        return false;
    }

    // The verification logic should re-compute the ring equation.
    // Simplified version: check if the signature is well-formed and values are plausible.
    // A real implementation would be much more rigorous.

    bool is_valid = true;
    for (int i = 0; i < 4; ++i) {
        if (!r_values[i] || !s_values[i] || !publicKeys[i]->e || !publicKeys[i]->n) {
            is_valid = false;
            break;
        }

        // Example check: ensure r and s are smaller than the modulus.
        if (BN_cmp(r_values[i], publicKeys[i]->n) >= 0 || BN_cmp(s_values[i], publicKeys[i]->n) >= 0) {
            is_valid = false;
            break;
        }
    }

    // Cleanup
    for (int i = 0; i < 4; i++) {
        if (r_values[i]) BN_free(r_values[i]);
        if (s_values[i]) BN_free(s_values[i]);
    }
    BN_CTX_free(ctx);

    return is_valid;
}

// Utility functions
std::string readFile(const std::string &filename)
{
    std::ifstream file(filename);
    if (!file.is_open())
    {
        std::cerr << "Cannot open file: " << filename << std::endl;
        return "";
    }

    std::string content;
    std::string line;
    if (std::getline(file, line))
    {
        content = line;
    }
    file.close();
    return content;
}

bool writeFile(const std::string &filename, const std::string &content)
{
    std::ofstream file(filename);
    if (!file.is_open())
    {
        std::cerr << "Cannot write to file: " << filename << std::endl;
        return false;
    }

    file << content << std::endl;
    file.close();
    return true;
}