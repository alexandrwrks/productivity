#include <iostream>
#include <vector>
#include <string>
#include <cctype>

using namespace std;

void process_matrix(vector<vector<int>>& matrix, vector<int>& s);

int main() {

    int M, N;
    cout << "Enter the number of rows (M):"; cin >> M;
    cout << "Enter the number of columns (N):"; cin >> N;
    vector<vector<int>> matrix(M, vector<int>(N));
    vector<int> s(M);

    for (int i = 0; i < M; i++) {
        int min, max;
        for (int j = 0; j < N; j++) {
            cout << "Enter elements [" << i << "][" << j << "]: ";
            cin >> matrix[i][j];
            if (j == 0) {
                min = matrix[i][j];
                max = matrix[i][j];
            }

            if (matrix[i][j] < min) min = matrix[i][j];
            if (matrix[i][j] > max) max = matrix[i][j];
            
        }
        s[i] = min + max;
        cout << "Row " << i << " min: " << min << ", max: " << max << endl;
    }
    cout << endl;

    process_matrix(matrix, s);
    return 0;
}

void process_matrix(vector<vector<int>>& matrix, vector<int>& s) { 
    int M = matrix.size();
    int N = matrix[0].size();
    
    cout << "Original matrix:" << endl;
    for (int i = 0; i < M; i++) {
        cout << "[ ";
        for (int j = 0; j < N; j++) {
            cout << matrix[i][j] << " ";
        }
        cout << "]";
        cout << "| s = " << s[i] << endl;
    }

    // Sorted original matrix 
    for (int i = 1; i < M; i++) {
        vector<int> ROW = matrix[i];
        int sum = s[i];
        int j = i - 1;

        while (j >= 0 && s[j] > sum) {
            matrix[j + 1] = matrix[j];
            s[j + 1] = s[j];
            j--;
        }

        matrix[j + 1] = ROW;
        s[j+1] = sum;
    }

    cout << "\nSorted matrix:" << endl;
    for (int i = 0; i < M; i++) {
        cout << "[ ";
        for (int j = 0; j < N; j++) {
            cout << matrix[i][j] << " ";
        }
        cout << "]";
        cout << "| s = " << s[i] << endl;
    }
}

// void sortedMassive(vector<string>& massive) {

//     for (size_t i = 0; i < massive.size()-1; i++) {
//         for (size_t j = 0; j < massive.size()-i-1; j++) {
//             if (massive[j] > massive[j+1]) {
//                 swap(massive[j], massive[j+1]);
//             }
//         }
//     }

//     cout << "\nSorted massive:\n";
//     for (int i = 0; i < massive.size(); i++) {
//         cout << massive[i] << " ";
//     }
// }

// int main() {

//     string name = "banana apple strawberry blueberry blackberry cherry";
//     vector<string> massive;
//     string word;

//     for (size_t i = 0; i < name.length(); i++) {
//         if (name[i] != ' ') {
//             word += name[i];
//         } 
//         else {
//             if (!word.empty()) {
//                 massive.push_back(word);
//                 word.clear();
//             }
//         }
//     }

//     if (!word.empty()) {
//         massive.push_back(word);
//     }

//     cout << "Source massive:\n";
//     for (size_t i = 0; i < massive.size(); i++) {
//         cout << massive[i] << " ";
//     }

//     sortedMassive(massive);
    
//     return 0;
// }