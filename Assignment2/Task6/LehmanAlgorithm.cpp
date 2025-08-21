#include <iostream>
#include <cmath>
#include <vector>
#include <random>
#include <algorithm>

using namespace std;

class LehmanPrimalityTest
{
private:
    mt19937 rng;
    int test_count;
    vector<long long> random_numbers_used;

    // Greatest Common Divisor using Euclidean algorithm
    long long gcd(long long a, long long b)
    {
        while (b != 0)
        {
            long long temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    // Modular exponentiation: (base^exp) % mod
    long long modPow(long long base, long long exp, long long mod)
    {
        long long result = 1;
        base %= mod;
        while (exp > 0)
        {
            if (exp & 1)
            {
                result = (__int128)result * base % mod;
            }
            base = (__int128)base * base % mod;
            exp >>= 1;
        }
        return result;
    }

    // Jacobi symbol calculation
    int jacobi(long long a, long long n)
    {
        if (n <= 0 || n % 2 == 0)
            return 0;

        int result = 1;
        a %= n;

        while (a != 0)
        {
            while (a % 2 == 0)
            {
                a /= 2;
                if (n % 8 == 3 || n % 8 == 5)
                {
                    result = -result;
                }
            }
            std::swap(a, n);
            if (a % 4 == 3 && n % 4 == 3)
            {
                result = -result;
            }
            a %= n;
        }

        return (n == 1) ? result : 0;
    }

    // Single Lehman test iteration
    bool lehmanTest(long long n, long long a)
    {
        // Check if gcd(a, n) > 1
        long long g = gcd(a, n);
        if (g > 1)
        {
            return false; // Composite
        }

        // Calculate Jacobi symbol (a/n)
        int jacobi_symbol = jacobi(a, n);

        // Calculate a^((n-1)/2) mod n
        long long exp = (n - 1) / 2;
        long long result = modPow(a, exp, n);

        // Convert result to {-1, 0, 1} form
        if (result == n - 1)
            result = -1;
        else if (result != 1)
            result = 0;

        // Test passes if a^((n-1)/2) ≡ (a/n) (mod n)
        return result == jacobi_symbol;
    }

public:
    LehmanPrimalityTest() : rng(random_device{}()), test_count(0) {}

    bool isPrime(long long n, int iterations = 20)
    {
        test_count = 0;
        random_numbers_used.clear();

        // Handle small cases
        if (n < 2)
            return false;
        if (n == 2)
            return true;
        if (n % 2 == 0)
            return false;
        if (n == 3)
            return true;

        // Check for small prime factors up to sqrt(n) or reasonable limit
        int limit = min(1000LL, (long long)sqrt(n) + 1);
        for (int i = 3; i <= limit; i += 2)
        {
            if (n % i == 0)
                return false;
        }

        // Perform Lehman tests
        uniform_int_distribution<long long> dist(2, n - 2);

        for (int i = 0; i < iterations; i++)
        {
            long long a = dist(rng);
            random_numbers_used.push_back(a);
            test_count++;

            if (!lehmanTest(n, a))
            {
                return false; // Definitely composite
            }
        }

        return true; // Probably prime
    }

    void printTestResults(long long n, bool result)
    {
        cout << "Testing number: " << n << endl;
        cout << "Number of tests conducted: " << test_count << endl;
        cout << "Random numbers used for testing: ";

        for (size_t i = 0; i < random_numbers_used.size(); i++)
        {
            cout << random_numbers_used[i];
            if (i < random_numbers_used.size() - 1)
                cout << ", ";
        }
        cout << endl;

        cout << "Result: " << n << " is "
            << (result ? "probably PRIME" : "COMPOSITE") << endl;
        cout << "----------------------------------------" << endl;
    }
};

int main()
{
    LehmanPrimalityTest lehman;
    long long number;

    cout << "=== Lehman's Primality Test ===" << endl;
    cout << "Enter a number to test for primality: ";
    cin >> number;

    // Test the number
    bool is_prime = lehman.isPrime(number, 20);
    lehman.printTestResults(number, is_prime);

    // Additional test cases for demonstration
    cout << "\n=== Additional Test Cases ===" << endl;
    vector<long long> test_cases = {17, 25, 97, 100, 1009, 1013, 9973, 10007};

    for (long long test_num : test_cases)
    {
        bool result = lehman.isPrime(test_num, 10);
        lehman.printTestResults(test_num, result);
    }

    return 0;
}