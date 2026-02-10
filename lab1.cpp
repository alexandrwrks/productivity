#include <iostream>
#include <string>

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
    // нахождение периметра прямоугольника
    double a, b;

    cout << "Введите длину и ширину: " << endl;
    cin >> a >> b;

    cout << "Периметр равен: " << (a+b)*2;
    return 0;
}

