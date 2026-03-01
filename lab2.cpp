#include <iostream>
#include <string>
#include <cmath>

using namespace std;

// int main() {
//     // p = m/V
//     float m1, m2, v1, v2;
//     cout << "Enter weight 1: "; cin >> m1;
//     cout << "Enter volume 1: "; cin >> v1;
//     cout << "Enter weight 1: "; cin >> m2;
//     cout << "Enter volume 1: "; cin >> v2;

//     float p1 = m1/v1;
//     float p2 = m2/v2;

//     if (p1 > p2) {
//         cout << "Density 1 is greater:  " << p1;
//     } else {
//         cout << "Density 2 is greater: " << p2;
//     }
//     return 0;
// }

int main() {
    double a,b,c;
    cout << "Enter number a, b, c: " << endl;
    cin >> a >> b >> c;
    if (a>=b & b >=c) {
        cout << "a: " << 2*a << endl;
        cout << "b: " << 2*b << endl;
        cout << "c: " << 2*c << endl;
    } else {
        cout << "a: " << abs(a) << endl;
        cout << "b: " << abs(b) << endl;
        cout << "c: " << abs(c) << endl;
    }
}