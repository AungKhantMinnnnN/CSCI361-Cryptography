#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

// Function to convert decimal to binary string
string toBinary(long long n)
{
    if (n == 0)
        return "0";
    string binary = "";
    while (n > 0)
    {
        binary = (n % 2 == 0 ? "0" : "1") + binary;
        n /= 2;
    }
    return binary;
}

// Function to perform modular exponentiation using square and multiply
long long fastExponentiation(long long a, long long b, long long p)
{
    cout << "Computing " << a << "^" << b << " (mod " << p << ")" << endl;

    // Step 1: Convert b to binary
    string binary = toBinary(b);
    cout << "Step 1 - Convert " << b << " to binary: " << binary << endl;

    // Step 2: Convert to S and X notation
    cout << "Step 2 - Convert to S and X notation:" << endl;
    vector<char> operations;
    for (int i = 0; i < binary.length(); i++)
    {
        if (i > 0)
            operations.push_back('S'); // Square for each bit position after first
        if (binary[i] == '1')
            operations.push_back('X'); // Multiply for each 1 bit
    }

    cout << "Sequence: ";
    for (char op : operations)
    {
        cout << op << " ";
    }
    cout << endl;

    // Step 3: Remove first SX (if present)
    cout << "Step 3 - Remove first SX:" << endl;
    if (operations.size() >= 2 && operations[0] == 'S' && operations[1] == 'X')
    {
        operations.erase(operations.begin());
        operations.erase(operations.begin());
        cout << "Removed first SX. ";
    }
    cout << "New sequence: ";
    for (char op : operations)
    {
        cout << op << " ";
    }
    cout << endl;

    // Step 4: Compute according to sequence
    cout << "Step 4 - Compute according to sequence:" << endl;
    long long result = a % p;
    cout << "Initial value: " << result << endl;

    int step = 1;
    for (char op : operations)
    {
        if (op == 'S')
        {
            long long oldResult = result;
            result = (result * result) % p;
            cout << "Step " << step << " (S): " << oldResult << "^2 mod " << p << " = " << result << endl;
        }
        else if (op == 'X')
        {
            long long oldResult = result;
            result = (result * a) % p;
            cout << "Step " << step << " (X): " << oldResult << " * " << a << " mod " << p << " = " << result << endl;
        }
        step++;
    }

    return result;
}

int main()
{
    long long a, b, p;

    cout << "Fast Exponentiation Calculator" << endl;
    cout << "==============================" << endl;
    cout << "Enter base (a): ";
    cin >> a;
    cout << "Enter exponent (b): ";
    cin >> b;
    cout << "Enter modulus (p): ";
    cin >> p;
    cout << endl;

    long long result = fastExponentiation(a, b, p);

    cout << endl;
    cout << "Final Result: " << a << "^" << b << " (mod " << p << ") = " << result << endl;

    return 0;
}