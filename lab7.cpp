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
//              << BOOK[i].BDAY[0] << ".0" << BOOK[i].BDAY[1] << "." << BOOK[i].BDAY[2] << endl;
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

struct KINO
{
    string NAME; // name of the films
    double COST; // cost of the films
    string DIRECTOR; // name of the director
};    


int main() {

    int SIZE;
    cout << "Enter the number of movies: "; 
    cin >> SIZE; // amount of films
    cin.ignore(); 
    vector<KINO> LIST(SIZE);

    cout << "\nEnter information about the films: \n";
    cout << "================================\n";
    for (int i = 0; i < SIZE; i++) {
        cout << "\nEnter the name of " << i + 1 << " film: "; 
        getline(cin, LIST[i].NAME);
        
        cout << "Enter the cost of " << i + 1 << " film: ";
        cin >> LIST[i].COST;

        cout << "Enter the name of the director of " << i + 1 << " film: ";
        cin.ignore();
        getline(cin, LIST[i].DIRECTOR);
    }

    cout << "\nInformation provided:\n";
    cout << "====================================================\n";
    cout << left << setw(20) << "Name of the film" 
         << setw(20) << "Cost of the film"
         << setw(20) << "Director" << endl;

    for (int i = 0; i < SIZE; i++) {
        cout << left << setw(20) << LIST[i].NAME 
             << setw(20) << LIST[i].COST
             << setw(20) << LIST[i].DIRECTOR << endl;
    }

    for (int i = 0; i < SIZE-1; i++) {
        for (int j = 0; j < SIZE-i-1; j++) {
            if (LIST[j].COST > LIST[j+1].COST) {
                KINO kino = LIST[j];
                LIST[j] = LIST[j+1];
                LIST[j+1] = kino;
            }
        }
    }

    cout << "\nChanged information:\n";
    cout << "====================================================\n";
    cout << left << setw(20) << "Name of the film" 
         << setw(20) << "Cost of the film"
         << setw(20) << "Director" << endl;
    for (int i = 0; i < SIZE; i++) {
        cout << left << setw(20) << LIST[i].NAME 
             << setw(20) << LIST[i].COST
             << LIST[i].DIRECTOR << endl;
    }
    return 0;
} 