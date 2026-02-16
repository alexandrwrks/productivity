// #include <iostream>
// #include <string>
// #include <ctype.h>

// using namespace std;

// // int main() {
// //     cout << "Введите строку: "; 
    
// //     // abc123def45gh
// //     // Hello world 2026!!!
// //     // Привет 2026 год!!!
// //     // Введите строку

// //     string line; // cin >> line;
// //     getline(cin, line); 

// //     int max_len = 0, current_len = 0;

// //     // for (char symbol : line) {
// //     //     cout << symbol;
// //     // }

// //     for (size_t i = 0; i < line.length(); i++) {
// //         if (not isdigit(line[i])) {
// //             current_len += 1;
// //         } else {
// //             if (current_len > max_len) {
// //                 max_len = current_len;
// //                 current_len = 0;
// //             } else {
// //                 current_len = 0;
// //             }
// //         }
// //     }
// //     if (current_len > max_len) {
// //         max_len = current_len;
// //     }

// //     cout << "Максимальная длина = " << max_len;

// //     return 0;
// // }

// int main() {

//     // Hello (world) 2026
//     // Hello ((world)) 2026
//     // (abc)123def45gh

//     bool brackets = false;
//     string start_line, result; 

//     cout << "Введите строку: "; getline(cin, start_line);

//     for (size_t i = 0; i < start_line.length(); i++) {
//         if (start_line[i] == '(') {
//             brackets = true;
//         } 
//         else if (start_line[i] == ')') {
//             brackets = false;
//         } 
//         else {
//             if (!brackets) {
//                 result += start_line[i];
//             }
//         }
//     }

//     cout << "Результат: " << result << endl;

//     return 0;
// }

#include <iostream>
#include <string>
#include <vector>
#include <iomanip>

using namespace std;

// Определяем структуру ORDER
struct ORDER {
    string PLAT;        // расчетный счет плательщика
    string POL;         // расчетный счет получателя
    double SUMMA;       // перечисляемая сумма в рублях
};

int main() {
    const int SIZE = 8;  // размер массива
    vector<ORDER> SPISOK(SIZE);  // массив из 8 элементов типа ORDER
    
    // Ввод данных с клавиатуры
    cout << "Введите информацию о 8 платежах:\n";
    cout << "================================\n";
    
    for (int i = 0; i < SIZE; i++) {
        cout << "\nПлатеж №" << i + 1 << ":\n";
        
        cout << "Расчетный счет плательщика: ";
        getline(cin, SPISOK[i].PLAT);
        
        cout << "Расчетный счет получателя: ";
        getline(cin, SPISOK[i].POL);
        
        cout << "Сумма перевода (руб): ";
        cin >> SPISOK[i].SUMMA;
        cin.ignore();  // очищаем буфер ввода
    }
    
    // Вывод введенной информации для проверки
    cout << "\nВведенная информация:\n";
    cout << "------------------------------------------------\n";
    cout << left << setw(15) << "Плательщик" 
         << setw(15) << "Получатель" 
         << setw(10) << "Сумма" << endl;
    cout << "------------------------------------------------\n";
    
    for (int i = 0; i < SIZE; i++) {
        cout << left << setw(15) << SPISOK[i].PLAT 
             << setw(15) << SPISOK[i].POL 
             << setw(10) << fixed << setprecision(2) << SPISOK[i].SUMMA << endl;
    }
    
    // Поиск суммы по счету плательщика
    string search_plat;
    cout << "\nВведите расчетный счет плательщика для поиска: ";
    getline(cin, search_plat);
    
    double total_sum = 0;
    bool found = false;
    
    // Подсчитываем общую сумму для указанного плательщика
    for (int i = 0; i < SIZE; i++) {
        if (SPISOK[i].PLAT == search_plat) {
            total_sum += SPISOK[i].SUMMA;
            found = true;
        }
    }
    
    // Вывод результата
    cout << "\nРезультат поиска:\n";
    cout << "================\n";
    
    if (found) {
        cout << "Со счета плательщика " << search_plat 
             << " было снято " << fixed << setprecision(2) 
             << total_sum << " руб.\n";
    } else {
        cout << "Расчетный счет плательщика " << search_plat 
             << " не найден в базе данных.\n";
    }
    
    return 0;
}