#include <iostream>
#include <string>
#include <cmath>

using namespace std;

int main() {
    // Нахождение плотности жлементов
    // p = m/V
    float m1, m2, v1, v2;
    cout << "Введите массу первого элемента: "; cin >> m1;
    cout << "Введите объём первого элемента: "; cin >> v1;
    cout << "Введите массу второго элемента: "; cin >> m2;
    cout << "Введите объём второго элемента: "; cin >> v2;

    float p1 = m1/v1;
    float p2 = m2/v2;

    if (p1 > p2) {
        cout << "Плотность первого элемента больше:  " << p1;
    } else {
        cout << "Плотность второго элемента больше: " << p2;
    }

    
    return 0;
}

int main() {
    double a,b,c;
    cout << "Введите значения для a, b, c: " << endl;
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