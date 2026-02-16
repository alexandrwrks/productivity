#include <iostream>
#include <cmath>

using namespace std;

int main() {

    int row, col, max_col;
    cout << "Введите значение row: "; cin >> row; 
    cout << "Введите значение col: "; cin >> col;
    /* Матрица -
    9 8 7
    6 5 4 
    3 2 1
    */ 
    double matrix[row][col], max = -100;


    // Ввод матрицы row * col
    for (int i = 0; i < row; i++) {
        cout << "Введите значения " << i+1 << " строки" << endl;
        for (int j = 0; j < col; j++) {
            int num; cout << j+1 << ": "; cin >> num;
            if (num > max) {
                max = num;
                max_col = j;
            }
            matrix[i][j] = num;
        }
    }

    cout << "Максимальный элемент " << max << " находится в столбце " << max_col+1 << "\n" << endl;
    // Вывод матрицы без замены
    for (int i = 0; i < row; i++) {
        for (int j = 0; j < col; j++) {
            cout << matrix[i][j] << " ";
        }
        cout << endl;
    }
    
    // Переставляем столбец с максимальным числом на конец
    for (int i = 0; i < row; i++) {
        int a = matrix[i][col-1];
        matrix[i][col-1] = matrix[i][max_col];
        matrix[i][max_col] = a;
    }
    
    // Вывод матрицы с максимальным числом в конце
    for (int i = 0; i <= row-1; i++) {
        for (int j = 0; j <= col-1; j++) {
            cout << matrix[i][j] << " ";
        }
        cout << endl;
    }

    return 0;
}

int main(){

    const int n = 4;
    double y = 0.0, x[n+1];


    cout << "Введите " << n+1 << " элементов массива x: " << endl;
    for (int i = 0; i <= n; i++) {
        cout << "Введите " << i+1 << " значение: ";
        double a; cin >> a; x[i] = a;
    }

    for (int j = 0; j <= n; j++)
    {
        if (j % 2 == 0) {
            y += x[j] * x[n - j];
        } else {
            y -= x[j] * x[n - j];
        }
    }

    cout << "Сумма: " << y;

    return 0;
}
