#include <iostream>
#include <vector>
#include <fstream>
#include <string>

using namespace std;

double recurseSumFunc(vector<int>& vec, size_t index = 0) {
    if (index >= vec.size()) {
        return 0;
    }
    return (1.0/vec[index]) + recurseSumFunc(vec, index + 1);
}

int main() {
    
    int lenght; 
    cout << "Enter number of lenght: "; cin >> lenght;
    vector<int> massive(lenght);

    for (int i = 0; i < lenght; i++) {
        cout << "Enter " << i+1 << " number: ";
        cin >> massive[i];
    }

    double result = recurseSumFunc(massive);
    cout << "Sum of numbers: " << result;

    return 0;
}

// ifstream in;
// int sum = 0;

// int recurseSumNumbers() {
//     int number;

//     if (in >> number) {
//         return number + recurseSumNumbers();
//     } else {
//         return 0;
//     }
// }

// int main()
// {
//     string numbers;
//     cout << "Enter numbers separted by spaces: " << endl;
//     getline(cin, numbers);

//     ofstream out("lab-10.txt");
//     if (out.is_open()) {
//         out << numbers;
//         out.close();
//     }

//     in.open("lab-10.txt");

//     if (in.is_open()) {
//         int result = recurseSumNumbers();
//         cout << "Sum = " << result << endl;
//         in.close();
//     }

//     return 0;
// }