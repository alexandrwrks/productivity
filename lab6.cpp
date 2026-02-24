#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

int main() {

    const int SIZE = 4;
    vector<double> X(SIZE), Y(SIZE), Z(SIZE);
    double num = 1.0, W = 1;

    for (int i = 0; i < SIZE; i++) {
        cout << "Enter the " << i+1 << " number: ";
        cin >> Y[i];
    }

    for (int i = 0; i < SIZE; i++) {
        num *= (1 - pow(Y[i], 2));
    }

    cout << "The product of the array Y is " << num << endl;
    if (num > 0.5) {
        cout << "\nEnter the numbers for branch X:\n";
        for (int i = 0; i < SIZE; i++) {
            cout << "X[" << i+1 << "] = ";
            cin >> X[i];
        }
        for (int i = 0; i < SIZE; i++) {
            W *= sin(X[i]) + 2;
        }
    } else {
        cout << "\nEnter the numbers for branch Z:\n";
        for (int i = 0; i < SIZE; i++) {
            cout << "Z[" << i+1 << "] = ";
            cin >> Z[i];
        }
        for (int i = 0; i < SIZE; i++) {
            W *= (1 - pow(Z[i], 2));
        }
    }
    cout << "Product of W: " << W;
    return 0;
}   

const int SIZE = 4;

void createMatrix(vector<vector<int>>& matrix) {
    cout << "Enter " << SIZE << "x" << SIZE << "matrix elements:" << endl;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            cout << "Element [" << i << "][" << j << "]";
            cin >> matrix[i][j];
        }
    }
        

}

void printMatrix(const vector<vector<int>>& matrix) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            cout << matrix[i][j] << " ";
        }
        cout << endl;
    }
}

vector<vector<int>> productMatrix(const vector<vector<int>>& A,
                                  const vector<vector<int>>& B) {
    vector<vector<int>> result(SIZE, vector<int>(SIZE, 0));

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            for (int k = 0; k < SIZE; k++) {
                result[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    return result;
}

int main() {
    // Create 3 matrix 4 row

    const int SIZE = 4;
    vector<vector<int>> A(SIZE, vector<int>(SIZE));
    vector<vector<int>> B(SIZE, vector<int>(SIZE));
    vector<vector<int>> C(SIZE, vector<int>(SIZE));

    cout << "Create A matrix" << endl;
    createMatrix(A);

    cout << "Create B matrix" << endl;
    createMatrix(B);

    cout << "Create C matrix" << endl;
    createMatrix(C);

    cout << "\n\nCreated matrixes\n";
    cout << "Matrix A\n";
    printMatrix(A);

    cout << "Matrix B\n";
    printMatrix(B);

    cout << "Matrix C\n";
    printMatrix(C);


    vector<vector<int>> AB = productMatrix(A, B);
    vector<vector<int>> BC = productMatrix(B, C);
    vector<vector<int>> AC = productMatrix(A, C);

    cout << "\nA * B: " << endl;
    printMatrix(AB);

    cout << "\nB * C: " << endl;
    printMatrix(BC);

    cout << "\nA * C: " << endl;
    printMatrix(AC);

    return 0;
}

