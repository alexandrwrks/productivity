#include <iostream>

using namespace std;

// int main() {
//     int num, sum, digit;

//     cout << "Enter number: "; cin >> num;
//     num = abs(num); 
//     sum = 0;

//     while (num > 0) {
//         digit = num % 10;
//         sum += digit;
//         num /= 10; 
//     }
//     cout << "The sum of the digits in the number: " << sum;
//     return 0;
// }

int main() {
    // a * (a - n) * (a - 2n) *..* (a - n^2)
    int n, k;
    double a, sum;

    cout << "Enter n: "; cin >> n;
    cout << "Enter a: "; cin >> a; 
    sum = 1.0;
    for (k=0; k<=n; k++) {
        sum *= (a - k * n);
    }

    cout << "The sum: " << sum;
    return 0;
}