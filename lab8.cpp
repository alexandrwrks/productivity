#include <iostream> 
#include <iomanip>
#include <vector>

using namespace std;

void sortBySum(vector<int>& numbers, vector<int>& sum_numbers) {

    for (int i = 0; i < sum_numbers.size()-1; i++) {
        int min_index = i;
        for (int j = i + 1; j < sum_numbers.size(); j++) {
            if (sum_numbers[min_index] > sum_numbers[j]) {
                min_index = j;
            }
        }   
        int num = numbers[i], sum = sum_numbers[i];
        numbers[i] = numbers[min_index];
        numbers[min_index] = num;

        sum_numbers[i] = sum_numbers[min_index];
        sum_numbers[min_index] = sum;
    } 
}

int main() {
    vector<int> numbers {29, 22, 8, 5, 12, 17, 3, 9, 15, 11};
    vector<int> sum_numbers(numbers.size());

    for (int i = 0; i < numbers.size(); i++) {
        int sum = 0, num = numbers[i], digit;
        while (num > 0) {
            digit = num % 10;
            sum += digit;
            num /= 10;
        }
        sum_numbers[i] = sum;
    }
    cout << "\nStarting values:\n"; 
    for (int i = 0; i < numbers.size(); i++) {
        cout << numbers[i] << " ";
    }

    cout << "\nThe sum of the digits of the value:\n"; 
    for (int i = 0; i < sum_numbers.size(); i++) {
        cout << sum_numbers[i] << " ";
    }
    sortBySum(numbers, sum_numbers);
    cout << "\nModified array\n";
    for (int i = 0; i < numbers.size(); i++) {
        cout << numbers[i] << " ";
    }

    cout << "\nThe sum of the values in ascending order\n";
    for (int i = 0; i < sum_numbers.size(); i++) {
        cout << sum_numbers[i] << " ";
    }
    return 0;
}


