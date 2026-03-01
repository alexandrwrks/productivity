#include <iostream>
#include <cmath>

using namespace std;

// int main() {

//     int row, col, max_col;
//     cout << "Enter row: "; cin >> row; 
//     cout << "Enter col: "; cin >> col;
//     double matrix[row][col], max = -100;

//     for (int i = 0; i < row; i++) {
//         cout << "Enter " << i+1 << " row" << endl;
//         for (int j = 0; j < col; j++) {
//             cout << j+1 << ": ";
//             double num;  
//             cin >> num;
//             if (num > max) {
//                 max = num;
//                 max_col = j;
//             }
//             matrix[i][j] = num;
//         }
//     }

//     cout << "Max number: " << max << "\nTo be in col: " << max_col+1 << endl;
//     cout << "Matrix" << endl;
//     for (int i = 0; i < row; i++) {
//         for (int j = 0; j < col; j++) {
//             cout << matrix[i][j] << " ";
//         }
//         cout << endl;
//     }

//     cout << "\nSorted matrix:\n";
//     for (int i = 0; i < row; i++) {
//         int a = matrix[i][col-1];
//         matrix[i][col-1] = matrix[i][max_col];
//         matrix[i][max_col] = a;
//     }

//     for (int i = 0; i <= row-1; i++) {
//         for (int j = 0; j <= col-1; j++) {
//             cout << matrix[i][j] << " ";
//         }
//         cout << endl;
//     }
//     return 0;
// }

int main(){

    const int n = 4;
    double y = 0.0, x[n+1];

    cout << "Enter " << n+1 << " elements to massive x: " << endl;
    for (int i = 0; i <= n; i++) {
        cout << "Enter " << i+1 << " element: ";
        cin >> x[i];
    }

    for (int j = 0; j <= n; j++)
    {
        if (j % 2 == 0) {
            y += x[j] * x[n - j];
        } else {
            y -= x[j] * x[n - j];
        }
    }
    cout << "The sum: " << y;
    return 0;
}