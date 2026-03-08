#include <iostream>
#include <vector>
#include <iomanip>
#include <string>
#include <fstream>

using namespace std;

ofstream file_out;
ifstream file_in;

/*
Laboratory work 7.1
*/ 

// struct FACTORY {
//     string surname;
//     double age;
//     string prof;
//     double salary;
// };

// void output(vector<FACTORY>& factory) {
//     cout << "Output information: " << endl;
//     cout << left << setw(20) << "Surname" 
//          << setw(10) << "Age"
//          << setw(20) << "Specialization"
//          << "Salary" << endl;

//     for (int i = 0; i < factory.size(); i++) {
//         cout << left << setw(20) << factory[i].surname
//              << setw(10) << factory[i].age 
//              << setw(20) << factory[i].prof 
//              << factory[i].salary << endl;
//     }
// }

// void fileOutput(vector<FACTORY>& factory) {
    
//     file_in.open("do_tasks.txt");
//     if (file_in.is_open()) {
//         string line;
//         getline(file_in, line);

//         FACTORY S;
//         cout << left << setw(20) << "\nSurname" 
//              << setw(10) << "Age"
//              << setw(20) << "Specialization"
//              << "Salary" << endl;

//         int T = 0, L = 0;
//         string turner = "turner";
//         string locksmith = "locksmith";
//         while (file_in >> ws && getline(file_in, S.surname, ' ') &&
//                file_in >> S.age >> S.prof >> S.salary) {
//                 cout << left << setw(20) << S.surname 
//                      << setw(10) << S.age
//                      << setw(20) << S.prof
//                      << S.salary << endl;
//                 if (S.prof == turner) {
//                     T++;
//                 } else if (S.prof == locksmith) {
//                     L++;
//                 }
//         }  
        
//         cout << "\nAmount of " << turner << ":" << T << endl;
//         cout << "Amount of " << locksmith << ":" << L << endl;
//     }
//     file_in.close();
// }

// int main() {

//     cout << "Enter amount of workers: ";
//     int N; cin >> N;
//     cin.ignore();

//     vector<FACTORY> factory(N);
//     file_out.open("do_tasks.txt");

//     if (file_out.is_open()) {
//         file_out << left << setw(20) << "Surname" 
//              << setw(10) << "Age"
//              << setw(20) << "Specialization"
//              << "Salary" << endl;
//         cout << "Enter information for " << N << " workers: " << endl;
//         for (int i = 0; i < N; i++) {
//             cout << "Enter surname for " << i + 1 << " worker: ";
//             getline(cin, factory[i].surname);

//             cout << "Enter age: ";
//             cin >> factory[i].age;
//             cin.ignore();
//             cout << "Enter specialization: ";
//             getline(cin, factory[i].prof);

//             cout << "Enter salary: ";
//             cin >> factory[i].salary;
//             cin.ignore();

//             file_out << left << setw(20) << factory[i].surname
//                      << setw(10) << factory[i].age 
//                      << setw(20) << factory[i].prof
//                      << factory[i].salary << endl;
//         }
//         file_out.close();
//     } else {
//         cout << "Couldn't open file" << endl;
//     }    
    
//     fileOutput(factory);
    
// }   

/*
Laboratory work 8.1
*/

// Функция для нахождения наименьшего делителя числа n, большего 1
// int f(int n) {
//     for (int i = 2; i <= n; i++) {
//         if (n % i == 0) {
//             return i;  // возвращаем первый (наименьший) найденный делитель
//         }
//     }
//     return n;  // для простых чисел вернется само число
// }

// int main() {
//     vector<int> a {4, 7, 9, 8, 10};
    
//     // Алгоритм простого выбора (selection sort)
//     for (int i = 0; i < a.size() - 1; i++) {
//         int min_index = i;  // индекс элемента с минимальным f(n)
        
//         // Ищем элемент с наименьшим f(n) в оставшейся части массива
//         for (int j = i + 1; j < a.size(); j++) {
//             // Сравниваем не сами числа, а их f-значения
//             if (f(a[j]) < f(a[min_index])) {
//                 min_index = j;
//             }
//         }
        
//         // Меняем местами текущий элемент с найденным минимальным
//         if (min_index != i) {
//             swap(a[i], a[min_index]);
//         }
//     }
    
//     // Вывод отсортированного массива
//     for (int i = 0; i < a.size(); i++) {
//         cout << a[i] << ' ';
//     }
    
//     return 0;
// }   

/*
Laboratory work 10.1
*/

// int sign(string s, int index = 0) {

//     static vector<char> z {'.', ',', ';', ':'};
    
//     if (index >= s.length()) {
//         return 0;
//     }

//     char currentChar = s[index];

//     for (char punctuation : z) {
//         if (currentChar == punctuation) {
//             return 1 + sign(s, index + 1) ;
//         }
//     }

//     return 0 + sign(s, index + 1);
// }

// int main() {

//     cout << "Enter line:";
//     string line;
//     getline(cin, line);

//     int result = sign(line);
//     cout << "Number of punctuation marks: " << result << endl;

//     return 0;
// }


class Person {
protected:
    string name;
    int age;

public:

    Person() : name(), age() {}

    void print() {
        cout << name << " - " << age << " age" << endl;
    }

    void input() {
        cout << "Enter name: ";
        getline(cin, name);
        cout << "Enter age:";
        cin >> age;
        cin.ignore();
        print();
    }
};

class Child : public Person {
private:
    string school;
    string hobby;

public:

    Child() : Person(), school(), hobby() {}

    void print() {
        Person::print();
        cout << "School: " << school << "\nHobby: " << hobby << endl;
    }

    void input() {
        Person::input();
        cout << "Enter school: ";
        getline(cin, school);
        cout << "Enter hobby: ";
        cin >> hobby;
        cin.ignore();
        print();
        play();
    }

    void play() {
        cout << name << " is playing " << hobby << endl;
    }

};

int main() {

    cout << "===PERSON===" << endl;
    Person p1;
    p1.input();


    cout << "===CHILD===" << endl;
    Child p2;
    p2.input();
    
    return 0;
}