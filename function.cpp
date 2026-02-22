#include <iostream>

using namespace std;

int fun(int i, int j) {
    if (i/2 == 0) return 0;
    else if (i % 2 == 0) return fun(i/2, 3*j) + i+j;
    else return fun(i/2, 2*j) + i + j;
    
}

int main() {
    cout << fun(20, 1) << endl;
    return 0;
}