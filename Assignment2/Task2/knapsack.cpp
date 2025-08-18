#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>

class knapsackCrypto {
    private:
        std::vector<int> privateKey; // super-increasing sequence
        std::vector<int> publicKey; // transformed sequence
        int modulus;
        int multiplier;
        int multiplicativeInverse;

        int extendedGCD(int a, int b, int &x, int &y){
            if (a == 0){
                x = 0;
                y = 1;
                return b;
            }
            int x1, y1;
            int gcd = extendedGCD(b % a, a, x1, y1);
            x = y1 - (b / a) * x1;
            y = x1;
            return gcd;
        }

        int modInverse(int a, int m){
            int x, y;
            int gcd = extendedGCD(a, m, x, y);
            if (gcd != 1) return -1; // no inverse exists
            return (x % m + m) % m;
        }

        bool isSuperIncreasing(const std::vector<int>& sequence){
            int sum = 0;
            for (int value : sequence){
                if (value <= sum) return false;
                sum += value;
            }
            return true;
        }

        // Function to check if multiplier and modulus are coprime for each other
        bool isValidMultiplier(int multiplier, int modulus){
            int a = multiplier, b = modulus;
            while (b != 0){
                int temp = b;
                b = a % b;
                a = temp;
            }
            return a == 1; // GCD should be 1
        }

    public:
        void setup(){
            int n;
            std::cout << "Enter the size of the super-increasing knapsack: ";
            std::cin >> n;

            privateKey.resize(n);
            std::cout << "Enter the values of the private key (super-increasing sequence):\n";
            for (int i = 0; i < n; i++){
                std::cout << "a[" << i << "]: ";
                std::cin >> privateKey[i];
            }

            //valid super-increasing property
            if(!isSuperIncreasing(privateKey)){
                std::cout << "Error: The sequence is not super-increasing.\n";
                return;
            }

            //get modulus
            int sum = std::accumulate(privateKey.begin(), privateKey.end(), 0);
            std::cout << "Enter modulus: (must be > " << sum << "): ";
            std::cin >> modulus;

            if (modulus <= sum){
                std::cout << "Error: Modulus must be greater than " << sum << ".";
                return;
            }

            //get multiplier
            std::cout << "Enter multiplier: ";
            std::cin >> multiplier;

            if(!isValidMultiplier(multiplier, modulus)){
                std::cout << "Error: Multiplier and modulus are not coprime.\n";
                return;
            }

            std::cout << "Conditions satisfied: GCD(" << multiplier << ", " << modulus << ") = 1/n";

            //calculate multiplicative inverse
            multiplicativeInverse = modInverse(multiplier, modulus);
            if (multiplicativeInverse == -1){
                std::cout << "Error: Cannot find multiplicative inverse.\n";
                return;
            }

            publicKey.resize(n);
            for (int i = 0; i < n; i++){
                publicKey[i] = (privateKey[i] * multiplier) % modulus;
            }

            //print public key
            for (int i = 0; i < publicKey.size(); i++){
                std::cout << publicKey[i];
                if (i < publicKey.size() - 1) std::cout << ", ";
            }
            std::cout << std::endl;
        }
        
        std::vector<int> encryption(const std::string& plaintext){
            std::vector<int> ciphertext;
            for (char c : plaintext){
                //convert character to binary
                std::vector<int> binary(8);
                for (int i = 7; i >= 0; i--){
                    binary[7-i] = (c >> i) & 1;
                }

                //encryption using public key
                int sum = 0;
                for (int i = 0; i < 8 && i < publicKey.size(); i++){
                    sum += binary[i] * publicKey[i];
                }
                ciphertext.push_back(sum);
            }
        }

        std::string decryption(const std::vector<int>& ciphertext){
            std::string plaintext;
            for (int cipher : ciphertext){
                // transform cipher using multiplicative inverse
                int transformedCipher = (cipher * multiplicativeInverse) % modulus;

                // solve knapsack
                std::vector<int> binary(8,0);
                for (int i = privateKey.size() - 1; i >= 0 && i >= privateKey.size() - 8; i--){
                    int idx = 7 - (privateKey.size() - 1 - i);
                    if (idx >= 0 && transformedCipher >= privateKey[i]){
                        binary[idx] = 1;
                        transformedCipher -= privateKey[i];
                    }
                }

                // convert binary to char
                char c = 0;
                for (int i = 0; i < 8; i++){
                    c |= (binary[i] << (7 - i));
                }
                plaintext += c;
            }
            return plaintext;
        }

        void run(){
            setup();

            if(publicKey.empty()){
                std::cout << "Setup failed. Exiting program.\n";
                return;
            }

            //encryption
            std::string message;
            std::cout << "\nEnter message for encryption: ";
            std::cin.ignore(); // clear input buffer
            std::getline(std::cin, message);

            std::vector<int> ciphertext = encryption(message);

            std::cout << "\nEncrypted ciphertext: ";
            for (int i = 0; i < ciphertext.size(); i++){
                std::cout << ciphertext[i];
                if (i < ciphertext.size() - 1) std::cout << ", ";
            }
            std::cout << std::endl;

            //decryption
            std::cout << "\nEnter ciphertext to decrypt (space-separated): ";
            std::string input;
            std::getline(std::cin, input);

            std::vector<int> inputCiphertext;
            size_t position = 0;
            while (position < input.length()){
                size_t nextPosition = input.find(' ', position);
                if (nextPosition == std::string::npos) nextPosition = input.length();

                std::string numberString = input.substr(position, nextPosition - position);
                if(!numberString.empty()){
                    inputCiphertext.push_back(std::stoi(numberString));
                }
                position = nextPosition + 1;
            }

            std::string decryptedPlaintext = decryption(inputCiphertext);
            std::cout << "\nDecrypted message: " << decryption << std::endl;
        }
};

int main(){
    knapsackCrypto crypto;
    crypto.run();
    return 0;
}