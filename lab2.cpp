#include <iostream>
#include <string>
#include <cmath>

using namespace std;

// int main() {
//     // Зависимость плотности от объёма и массы
//     // p = m/V
//     float m1, m2, v1, v2;
//     cout << "Введите массу первого тела: "; cin >> m1;
//     cout << "Введите объём первого тела: "; cin >> v1;
//     cout << "Введите массу второго тела: "; cin >> m2;
//     cout << "Введите объём второго тела: "; cin >> v2;

//     float p1 = m1/v1;
//     float p2 = m2/v2;

//     if (p1 > p2) {
//         cout << "Плоность больше у первого материала " << p1;
//     } else {
//         cout << "Плотность больше у второго материала " << p2;
//     }

//     // cout << "Потность первого тела - " << m1/v1 << endl;
//     // cout << "Потность второго тела - " << m2/v2 << endl;
    
//     return 0;
// }
int main() {
    int a,b,c;
    cout << "Введите значения a, b и c: " << endl;
    cin >> a >> b >> c;
    if (a>=b and b >=c) {
        cout << "a: " << 2*a << endl;
        cout << "b: " << 2*b << endl;
        cout << "c: " << 2*c << endl;
    } else {
        cout << "a: " << abs(a) << endl;
        cout << "b: " << abs(b) << endl;
        cout << "c: " << abs(c) << endl;
    }
}