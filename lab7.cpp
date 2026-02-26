#include <iostream>
#include <iomanip>
#include <string>
#include <vector>

using namespace std;

// struct ZNAK {
//     /* data */
//     string NAME; // people's name and surname
//     string ZODIAC; // title of the zodiac sign
//     double BDAY[3]; // day, month, year of birth
// };

// int main() {

//     const int SIZE = 8;
//     vector<ZNAK> BOOK(SIZE);

//     cout << "Enter information about the employees: \n";
//     cout << "================================\n";
//     // Input information about the employees
//     for (int i = 0; i < SIZE; i++) {

//         cout << "\nEnter the name and surname of " << i+1 << " employee: "; 
//         getline(cin, BOOK[i].NAME);
        
//         cout << "Enter the zodiac sign of " << i + 1 << " employee: ";
//         cin >> BOOK[i].ZODIAC;

//         cout << "Enter the birth date: \n";
//         cout << "Day: "; cin >> BOOK[i].BDAY[0];
//         cout << "Month(without 0): "; cin >> BOOK[i].BDAY[1];
//         cout << "Year: "; cin >> BOOK[i].BDAY[2];
//         cin.ignore();
//     }
//     // Output the information about the employees
//     cout << "\nInformation provided:\n";
//     cout << "====================================================\n";
//     cout << left << setw(20) << "Name and Surname" 
//          << setw(20) << "Company Name"
//          << setw(20) << "Date of Birth" << endl;
//     cout << "====================================================\n";
//     for (int i = 0; i < SIZE; i++) {
//         cout << left << setw(20) << BOOK[i].NAME 
//              << setw(20) << BOOK[i].ZODIAC
//              << BOOK[i].BDAY[0] << "." << BOOK[i].BDAY[1] << "." << BOOK[i].BDAY[2] << endl;
//     }

//     // Input the number of month
//     int number_month, sum_people = 0;
//     cout << "\nEnter the month number: "; cin >> number_month;
//     bool found = false;
//     double sum = 0;

//     for (int i = 0; i < SIZE; i++) {
//         if (BOOK[i].BDAY[1] == number_month) {
//             sum += BOOK[i].BDAY[1];
//             sum_people++;
//             found = true;
//         }
//     }

//     if (found) {
//         cout << "Was found " << sum_people << " people born in " 
//              << number_month << " month." << endl;
//         for (int i = 0; i < SIZE; i++) {
//             if (BOOK[i].BDAY[1] == number_month) {
//                 cout << left << setw(20) << "Name: " 
//                      << setw(20) << "Zodiac: " 
//                      << setw(15) << "Date of Birth: " << endl;
//                 cout << left << setw(20) << BOOK[i].NAME 
//                      << setw(20) << BOOK[i].ZODIAC
//                      << BOOK[i].BDAY[0] << ".0" << BOOK[i].BDAY[1] << "." << BOOK[i].BDAY[2] << endl;
//             }
//         }
//     } else {
//         cout << "No people were found born in " 
//              << number_month << " month." << endl;
//     }
    
//     return 0;
// }

// Сделать вторую задачу 7 лабы
struct STUDY{
    string NAME;
    int AGE;
    int GROUP;
};

int main() {

    cout << "Enter amount of students: ";
    int amount; cin >> amount;

    vector<STUDY> BOOK(amount);
    cin.ignore();
    // Enter information
    cout << "Enter information about " << amount << " students" << endl;
    cout << "=================================";
    for (int i = 0; i < amount; i++) {
        
        cout << "\nStudent " << i + 1 << endl;
        cout << "Name: ";
        getline(cin, BOOK[i].NAME);

        cout << "Age: ";
        cin >> BOOK[i].AGE;

        cout << "Group: ";
        cin >> BOOK[i].GROUP;
        cin.ignore();
    }   

    // Print information
    cout << "\nInformation about a students" << endl;
    cout << "====================================================" << endl;
    cout << left << setw(20) << "Name" 
         << setw(20) << "Age" 
         << "Group" << endl;
    cout << "====================================================" << endl;

    
    for (int i = 0; i < amount; i++) {
        cout << left << setw(20) << BOOK[i].NAME
             << setw(20) << BOOK[i].AGE
             << BOOK[i].GROUP << endl;
    }

    cout << "\nEnter a number of group: ";
    int number_of_group; 
    cin >> number_of_group;
    bool found = true;

    if (found) {
        cout << "Information found for the group " << number_of_group << endl; 
        cout << "====================================================" << endl;
        for (int i = 0; i < amount; i++) {
            if (BOOK[i].GROUP == number_of_group) {
                cout << left << setw(20) << BOOK[i].NAME
                     << setw(20) << BOOK[i].AGE
                     << BOOK[i].GROUP;
            }
        }
    } else {
        cout << "Students of the entered group were not found" << endl;
    }

    return 0;
}