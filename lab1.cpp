#include <iostream>
#include <string>
#include <math.h>

using namespace std;

// int main() {

//     int a;
//     string number = "515-1";
//     // string name = "Alexeyev Alexandr";
//     string name = "Алексеев Александр";
    
//     // cout << "Enter your age: ";
//     cout << "Введите ваш возраст: ";
//     cin >> a;

//     cout << name << ' ' << "\nГрупа - " << number << endl;
//     // cout << "Your age: " << a << endl;
//     cout << "Ваш возраст: " << a << endl; 
    
//     return 0;
// }

int main(){
    // нахождение площади круга
    // S = pi * r**2
    double rad, pi; // радиус круга
    pi = 3.14;
    cout << "Введите радиус круга: "; cin >> rad;
    cout << "Площадь круга равна - " << pi*(pow(rad, 2));
    return 0;
}