#include <iostream>
#include <vector>

using namespace std;

int main() {
//     const int SIZE = 7;

//     vector<int> N(SIZE);
//     vector<double> X(SIZE);

//     cout << "Enter numbers to N:\n";
//     for (int i = 0; i < SIZE; i++) {
//         cout << i+1 << ":";
//         cin >> N[i];
//     }
//     cout << "Enter numbers to X:\n";
//     for (int i = 0; i < SIZE; i++) {
//         cout << i+1 << ":";
//         cin >> X[i];
//     }

//     double numerator = 0.0;
//     for (int i = 0; i < SIZE; i++) {
//         numerator += N[i]*X[i];
//     }
//     int denominator = 0;
//     for (int i = 0; i < SIZE; i++) {
//         denominator += N[i];
//     }

//     if (denominator == 0) {
//         cout << "Error: denominator don't be 0" << endl;
//         return 1;
//     }

//     double result = numerator / denominator;
//     cout << "Result: " << result << endl;

//     return 0;
// }


// int main() {
    int nums;
    double S = 0.0; 

    cout << "Enter amount number: ";
    cin >> nums;

    vector<double> a(nums); 

    for(int i = 0; i < nums; ++i) {
        cout << i+1 << ":";
        cin >> a[i];
    }

    for (int i = 0; i < nums; ++i) {
        if(i == 0 || i == nums - 1) { 
            S += a[i];
        } else {
            S += a[i] * 2;
        }
    }

    cout << "Summa: " << S << endl;

    return 0;
}