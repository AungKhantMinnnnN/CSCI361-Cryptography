#include "RingSignature.h"

int main(){
    cout << "Ring Signature - Sign Program" << endl;
    cout << "Enter person to sign (1 or 2): ";
    int signer;
    cin >> signer;

    if (signer != 1 && signer != 2){
        cerr << "Invalid signer. Must be 1 or 2" << endl;
        return 1;
    }

    string message = readFile("message.txt");
    if(message.empty()){
        cerr << "Failed to read message from message.txt" << endl;
        return 1;
    }

    RingSignature rs;
    if(!rs.loadPublicKeys("publickey.txt")){
        cerr << "Failed to load public keys from publickey.txt" << endl;
        return 1;
    }

    string signature = rs.generateRingSignature(message);
    if (signature.empty()){
        cerr << "Failed to generate signature." << endl;
        return 1;
    }

    if (writeFile("signature.txt", signature)){
        cout << "Signature generated and saved to signature.txt" << endl;
    }
    else{
        cerr << "Failed to write signature to signature.txt" << endl;
        return 1;
    }

    return 0;
}