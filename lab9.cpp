#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>

using namespace std;

struct STUDY{
    string name;
    string gender;
    int age;
    int course;
};

// int main() {

//     cout << "Enter amount about students: " << endl;
//     int n;
//     cin >> n;
//     cin.ignore();

//     vector<STUDY> study(n);
//     cout << "Enter information about " << n << " students" << endl;
//     ofstream out("lab-9.txt");

//     if (out.is_open()) {
//         out << left << setw(20) << "Name" 
//              << setw(20) << "Gender" 
//              << setw(20) << "Age" 
//              << "Course" << endl;
//         for (int i = 0; i < n; i++) {
//             cout << "Enter name for " << i + 1 << " student:";
//             getline(cin, study[i].name);
            
//             cout << "Enter gender(m/f): ";
//             cin >> study[i].gender;

//             cout << "Enter age:";
//             cin >> study[i].age;

//             cout << "Enter a course: ";
//             cin >> study[i].course;
//             cin.ignore();

//             out << left << setw(20) << study[i].name 
//                 << setw(20) << study[i].gender 
//                 << setw(20) << study[i].age 
//                 << study[i].course << endl;   
//         }
//         out.close();
//     } else {
//         cout << "Couldn't create output file" << endl;
//         return 1;
//     }
    
//     int age = 20;
//     cout << "\nStudents older than 20 years:" << endl;
    
//     ifstream in("lab-9.txt");
//     if (in.is_open()) {
//         string line;
//         getline(in, line);
        
//         STUDY s;
//         cout << left << setw(20) << "Name" 
//              << setw(20) << "Gender" 
//              << setw(20) << "Age" 
//              << "Course" << endl;

//         while (in >> ws && getline(in, s.name, ' ') &&
//                in >> s.gender >> s.age >> s.course) {
//                 if (s.age > 20) {
//                     cout << left << setw(20) << s.name 
//                          << setw(20) << s.gender 
//                          << setw(20) << s.age
//                          << s.course << endl;
//                 }
//         }
//     }
//     in.close();
// }

int main() {

    cout << "Enter amount about students: ";
    int n;
    cin >> n;
    cin.ignore();

    vector<STUDY> study(n);
    cout << "Enter information about " << n << " students" << endl;
    ofstream out("lab-9.txt");

    if (out.is_open()) {
        out << left << setw(20) << "Name" 
             << setw(20) << "Gender" 
             << setw(20) << "Age" 
             << "Course" << endl;
        for (int i = 0; i < n; i++) {
            cout << "Enter name for " << i + 1 << " student:";
            getline(cin, study[i].name);
            
            cout << "Enter gender(m/f): ";
            cin >> study[i].gender;

            cout << "Enter age:";
            cin >> study[i].age;

            cout << "Enter a course: ";
            cin >> study[i].course;
            cin.ignore();

            out << left << setw(20) << study[i].name 
                << setw(20) << study[i].gender 
                << setw(20) << study[i].age 
                << study[i].course << endl;   
        }
        out.close();
    } else {
        cout << "Couldn't create output file" << endl;
        return 1;
    }
    
    cout << "\ninformation about:" << endl;
    
    ifstream in("lab-9.txt");
    if (in.is_open()) {
        string line;
        getline(in, line);
        
        STUDY s;
        cout << left << setw(20) << "Name" 
             << setw(20) << "Gender" 
             << setw(20) << "Age" 
             << "Course" << endl;

        while (in >> ws && getline(in, s.name, ' ') &&
               in >> s.gender >> s.age >> s.course) {
                    cout << left << setw(20) << s.name 
                         << setw(20) << s.gender 
                         << setw(20) << s.age
                         << s.course << endl;
                }
        }
    
    in.close();
}