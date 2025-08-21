#include <iostream>
#include <string>
#include <unordered_map>
#include <iomanip>
#include <sstream>
#include <openssl/sha.h>

// SHA-1 function from https://github.com/openssl/openssl/blob/master/include/openssl/sha.h

using namespace std;

class sha1_collisionFinder{
    private:
        string firstname;
        unordered_map<uint64_t, pair<int, string>> hashtable;
    
    public:
        // constructor
        sha1_collisionFinder(const string& name) : firstname(name) {}

        // simplified SHA-1 function that returns only the first 34-bits
        uint64_t ssha1Hash(const string& message){
            unsigned char hash[SHA_DIGEST_LENGTH];

            SHA1(reinterpret_cast<const unsigned char*>(message.c_str()), message.length(), hash);

            // extract the first 34 bits
            // first 4 bytes = 32 bits + 2 more bits from the 5th byte
            uint32_t first4bytes = (static_cast<uint32_t>(hash[0]) << 24) |
                                    (static_cast<uint32_t>(hash[1]) << 16) |
                                    (static_cast<uint32_t>(hash[2]) << 8) |
                                    (static_cast<uint32_t>(hash[3]));

            // get the top 2 bits from the 5th byte
            uint8_t top2bits = (hash[4] >> 6) & 0x3;

            // combine: 32 bits from the first 4 bytes + 2 bits from 5th byte
            uint64_t hash34bits = (static_cast<uint64_t> (first4bytes) << 2) | top2bits;

            return hash34bits;
        }

        // function to find two different messages that produce the same ssha-1 hash
        void findCollision(){
            string temp1 = "Donald Trump owes " + firstname + " x dollars";
            string temp2 = "Donald Trump owes " + firstname + " x' dollars";

            int numOfTrails = 0;
            int x = 0;

            cout << "Searching for SSHA-1 hash collision....." << endl;
            cout << "Template 1: " + temp1 << endl;
            cout << "Template 2: " + temp2 << endl;
            cout << endl;

            while(true){
                numOfTrails++;

                // Create two messages 
                string m1 = temp1;
                string m2 = temp2;

                // replace placeholders with current x value
                size_t pos1 = m1.find("x");
                if (pos1 != string::npos){
                    m1.replace(pos1, 1, to_string(x));
                }

                size_t pos2 = m2.find("x' ");
                if (pos2 != string::npos){
                    m2.replace(pos2, 2, to_string(x));
                }

                // calc SSHA-1 hash
                uint64_t hash1 = ssha1Hash(m1);
                uint64_t hash2 = ssha1Hash(m2);

                // check collision with m1
                auto it1 = hashtable.find(hash1);
                if(it1 != hashtable.end()){
                    if (it1 ->second.second != m1){
                        printCollision(it1->second.second, m1, hash1, numOfTrails);
                        return;
                    }
                }

                // check collision with m2
                auto it2 = hashtable.find(hash2);
                if (it2 != hashtable.end())
                {
                    if (it2->second.second != m2)
                    {
                        printCollision(it2->second.second, m2, hash2, numOfTrails);
                        return;
                    }
                }

                // if no collision is found for both m1 and m2 continue.
                // store the hash values
                hashtable[hash1] = make_pair(x, m1);
                hashtable[hash2] = make_pair(x, m2);

                // Progress indicator
                if (numOfTrails % 10000 == 0)
                {
                    cout << "Tried " << numOfTrails << " combinations..." << endl;
                }

                x++;

                // safetly limit
                if (numOfTrails > 1000000)
                {
                    cout << "Reached maximum trials without finding collision" << endl;
                    break;
                }
            }
        }

    private:
        void printCollision(const string& msg1, const string& msg2, uint64_t hashVal, int numOfTrails){
            cout << "Collision found." << endl;
            cout << "Message 1: " << msg1 << endl;
            cout << "Message 2: " << msg2 << endl;
            cout << "Hash value: " << hashVal << " (0x"
                << hex << setfill('0') << setw(9)
                << hashVal << dec << ")" << endl;
            cout << "Number of trails ran: " << numOfTrails << endl;

            cout << "Verification: " << endl;
            uint64_t v1 = ssha1Hash(msg1);
            uint64_t v2 = ssha1Hash(msg2);

            cout << "Hash of '" << msg1 << "': " << v1
                    << " (0x" << hex << setfill('0') << setw(9)
                    << v1 << dec << ")" << endl;
            cout << "Hash of '" << msg2 << "': " << v2
                    << " (0x" << hex << setfill('0') << setw(9)
                    << v2 << dec << ")" << endl;
            cout << "Hashes match: " << (v1 == v2 ? "true" : "false") << endl;
        }
};

int main(){
    string name = "Aung Khant Min";
    
    sha1_collisionFinder finder(name);
    finder.findCollision();

    return 0;
}