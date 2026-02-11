#include <iostream>
#include <string>
#include <cmath>

using namespace std;

// int main() {
//     Сумма цифр в числе
//     int num, sum, digit;

//     cout << "Введите целое число: "; cin >> num;
//     abs(num); sum = 0;

//     while (num > 0) {
//         digit = num % 10;
//         sum += digit;
//         num /=10; 
//     }
//     cout << "Сумма цифр равна: " << sum;

//     return 0;
// }
int main() {
    // натуральное и действительное a
    // a * (a - n) * (a - 2n) *..* (a - n^2)
    int n, k, a, sum;

    cout << "Введите значение n: "; cin >> n;
    cout << "Введите значение a: "; cin >> a; 
    sum = 1;
    for (k=0; k<=n; k++) {
        sum *= (a - k * n);
    }
    
    // k = n;
    // while (k>=1, k--) {
    //     sum *= a - (k * n);
    // }

    cout << "Сумма равна: " << sum;
    return 0;
}