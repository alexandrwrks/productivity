#include <iostream>
#include <string>

using namespace std;

// int main() {

//     // abc123def45gh
//     // Hello world 2026!!!

//     cout << "Enter a line: "; 
//     string line;
//     getline(cin, line); 

//     int max_len = 0, current_len = 0;
//     for (size_t i = 0; i < line.length(); i++) {
//         if (not isdigit(line[i])) {
//             current_len++;
//         } else {
//             if (current_len > max_len) {
//                 max_len = current_len;
//                 current_len = 0;
//             } else {
//                 current_len = 0;
//             }
//         }
//     }
//     if (current_len > max_len) {
//         max_len = current_len;
//     }

//     cout << "Max len = " << max_len;
//     return 0;
// }

int main() {

    // Hello (world) 2026
    // (abc)123def45gh

    bool brackets = false;
    string start_line, result; 

    cout << "Enter a line: "; 
    getline(cin, start_line);
    for (size_t i = 0; i < start_line.length(); i++) {
        if (start_line[i] == '(') {
            brackets = true;
        } 
        else if (start_line[i] == ')') {
            brackets = false;
        } 
        else {
            if (!brackets) {
                result += start_line[i];
            }
        }
    }
    cout << "Result's line: " << result << endl;
    return 0;
}