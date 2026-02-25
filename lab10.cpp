#include <iostream>
#include <vector>

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