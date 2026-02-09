#include <iostream>
#include <string>

using namespace std;

int main() {

    int a;
    string number = "515-1";
    string name = "Alexeyev Alexandr";
    
    cout << "Enter your age: ";
    cin >> a;

    cout << name << ' ' << number << endl;
    cout << "Your age: " << a << endl;
    
    return 0;
}
