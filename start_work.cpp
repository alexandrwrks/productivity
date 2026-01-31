/*
Начало работ положено. Потихоньку начать программировать на C++. 
Начать работать с множествами значений/чисел(списки, словари, множества, кортежи)
Понять синтаксис онсовынх программ и буду готов к учёбе и/или работе.
*/ 
#include <iostream>

int greet(int a, int b); // вызов функции которая написана ниже

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
    int x, y;
    std::cin >> x >> y;

    int sum = add2(x, y);
    std::cout << "Summa = " << sum << std::endl;
    return 0;

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