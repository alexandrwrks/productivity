/*
Начало работ положено. Потихоньку начать программировать на C++. 
Начать работать с множествами значений/чисел(списки, словари, множества, кортежи)
Понять синтаксис онсовынх программ и буду готов к учёбе и/или работе.
*/ 
#include <iostream>
#include <list>
#include <set>

int greet(int a, int b); // вызов функции которая написана ниже
int add_set(); // вызов функции которая написана ниже

int add() { 
    // базовый функционал цикла for
    int min = 0; 
    int max = 10;
    int sum = 0;
    for (int i = min; i <= max; i++) {

        if (i % 2 == 0) {
            continue;
        } else {
            sum += i;     
        }
    }
    return sum;
}

int add2(int x, int y) {
    // базовый функционал цикла while
    int sum = 0;
    while (x <= y) {
        if (x % 2 != 0) {
            sum += x;
        }
        x++;
    }
    return sum;
}    

int main() {
    // основная функция 
    std::cout << "Sum of odd numbers between 0 and 10 (for loop): " << add_set() << std::endl;
}   

int add_list() {
    std::list<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    int sum = 0;
    for (int num : numbers) {
        sum += num;
    }

    return sum;
}

int greet(int a, int b) {
    // чтобы эту функции использовать в main нужно вызвать выше чем main. показал в начале файла
        if (a > b) {
        std::cout << "The greater number is: " << a << std::endl;
        return 0;
    } else {
        std::cout << "The greater number is: " << b << std::endl;
        return 0;
    }
}

int add_set() {
    std::set<int> num_set;
    int sum = 0;
    // цикл ввода чисел в множество
    while (true) {
        int num;
        std::cin >> num;
        if (num <= 0) {
            break;
        } else {
            num_set.insert(num);
        }
    }
    for (int n : num_set) {
        std::cout << n << " ";
        sum += n;
    }
    return sum;
}   