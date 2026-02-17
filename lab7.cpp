#include <iostream>
#include <iomanip>
#include <string>
#include <vector>

#include <clocale>
#include <windows.h>

// #include <list> 

using namespace std;

struct LAB7 {
    /* data */
    string NAME; // имя сотрудника
    string COMPANY; // название компании
    double currency; // средняя зарплата
};

int main() {

    SetConsoleCP(CP_UTF8);
    SetConsoleOutputCP(CP_UTF8);
    
    setlocale(LC_ALL, "Russian");  

    const int SIZE = 2;
    vector<LAB7> LIST(SIZE);

    cout << "Введите информацию о работниках: \n";
    cout << "================================\n";

    for (int i = 0; i < SIZE; i++) {

        cout << "\nВведите имя " << i+1 << " работника: "; 
        getline(cin, LIST[i].NAME);
        
        cout << "Введите компанию(где работает "<< i + 1 << " сотрудник): ";
        getline(cin, LIST[i].COMPANY);

        cout << "Введите среднюю зарплатную плату сотрудника(тысяч руб.): ";
        cin >> LIST[i].currency;
        cin.ignore();
    }
    // Вывод введеной информации
    cout << "\nВведёная ифнформация:\n";
    cout << "====================================================\n";
    cout << left << setw(20) << "Имя сотрудника" 
         << setw(20) << "Название компании"
         << setw(20) << "Заработная плата" << endl;
    cout << "====================================================\n";

    for (int i = 0; i < SIZE; i++) {
        cout << left << setw(20) << LIST[i].NAME 
             << setw(20) << LIST[i].COMPANY
             << setw(15) << fixed << setprecision(2) << LIST[i].currency << endl;
    }

    string name_company;
    cout << "\nВведите название компании: "; cin >> name_company;
    bool found = false;

    // string name;

    int sum_company = 0;
    double sum = 0, avg_sum = 0;

    for (int i = 0; i < SIZE; i++) {
        if (LIST[i].COMPANY == name_company) {
            sum += LIST[i].currency;
            sum_company++;
            found = true;
        }
    }

    avg_sum = sum/sum_company;
    cout << "Средняя заработная плата: " << avg_sum << " (тысяч руб.)";

    return 0;
}
