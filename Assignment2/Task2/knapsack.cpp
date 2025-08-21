#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>

using namespace std;

class knapsackCrypto {
    private:
        vector<int> privateKey; // super-increasing sequence
        vector<int> publicKey; // transformed sequence
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

        bool isSuperIncreasing(const vector<int>& sequence){
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
            cout << "Enter the size of the super-increasing knapsack: ";
            cin >> n;

            privateKey.resize(n);
            cout << "Enter the values of the private key (super-increasing sequence):\n";
            for (int i = 0; i < n; i++){
                cout << "a[" << i << "]: ";
                cin >> privateKey[i];
            }

            //valid super-increasing property
            if(!isSuperIncreasing(privateKey)){
                cout << "Error: The sequence is not super-increasing.\n";
                return;
            }

            //get modulus
            int sum = accumulate(privateKey.begin(), privateKey.end(), 0);
            cout << "Enter modulus: (must be > " << sum << "): ";
            cin >> modulus;

            if (modulus <= sum){
                cout << "Error: Modulus must be greater than " << sum << ".";
                return;
            }

            //get multiplier
            cout << "Enter multiplier: ";
            cin >> multiplier;

            if(!isValidMultiplier(multiplier, modulus)){
                cout << "Error: Multiplier and modulus are not coprime.\n";
                return;
            }

            cout << "Conditions satisfied: GCD(" << multiplier << ", " << modulus << ") = 1/n";

            //calculate multiplicative inverse
            multiplicativeInverse = modInverse(multiplier, modulus);
            if (multiplicativeInverse == -1){
                cout << "Error: Cannot find multiplicative inverse.\n";
                return;
            }

            publicKey.resize(n);
            for (int i = 0; i < n; i++){
                publicKey[i] = (privateKey[i] * multiplier) % modulus;
            }

            //print public key
            for (int i = 0; i < publicKey.size(); i++){
                cout << publicKey[i];
                if (i < publicKey.size() - 1) cout << ", ";
            }
            cout << endl;
        }
        
        vector<int> encryption(const string& plaintext){
            vector<int> ciphertext;
            for (char c : plaintext){
                //convert character to binary
                vector<int> binary(8);
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
            return ciphertext;
        }

        string decryption(const vector<int>& ciphertext){
            string plaintext;
            for (int cipher : ciphertext){
                // transform cipher using multiplicative inverse
                int transformedCipher = (cipher * multiplicativeInverse) % modulus;

                // solve knapsack
                vector<int> binary(8,0);
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
                cout << "Setup failed. Exiting program.\n";
                return;
            }

            //encryption
            string message;
            cout << "\nEnter message for encryption: ";
            cin.ignore(); // clear input buffer
            getline(cin, message);

            vector<int> ciphertext = encryption(message);

            cout << "\nEncrypted ciphertext: ";
            for (int i = 0; i < ciphertext.size(); i++){
                cout << ciphertext[i];
                if (i < ciphertext.size() - 1) cout << ", ";
            }
            cout << endl;

            //decryption
            cout << "\nEnter ciphertext to decrypt (space-separated): ";
            string input;
            getline(cin, input);

            vector<int> inputCiphertext;
            size_t position = 0;
            while (position < input.length()){
                size_t nextPosition = input.find(' ', position);
                if (nextPosition == string::npos) nextPosition = input.length();

                string numberString = input.substr(position, nextPosition - position);
                if(!numberString.empty()){
                    inputCiphertext.push_back(stoi(numberString));
                }
                position = nextPosition + 1;
            }

            string decryptedPlaintext = decryption(inputCiphertext);
            cout << "\nDecrypted message: " << decryptedPlaintext << endl;
        }
};

int main(){
    knapsackCrypto crypto;
    crypto.run();
    return 0;
}