#include "RingSignature.h"

int main(){
    

    string signature = readFile("signature.txt");
    if (signature.empty()){
        cerr << "Failed to read signature from signature.txt" << endl;
        return 1;
    }

    RingSignature rs;

    bool is_valid = rs.verifyRingSignature(signature, "publickey.txt");

    cout << "The generated ring signature is " << (is_valid ? "Valid." : "Not Valid.") << endl;
}