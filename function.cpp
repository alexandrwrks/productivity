#include <iostream>

double choice(int abonement);

int main() {
    int abonement;

    std::cout << "Abonement" << std::endl;
    std::cout << "1. Super Abonement" << std::endl;
    std::cout << "2. VIP Abonement" << std::endl;
    std::cout << "Choose your abonement: " << std::endl;

    std::cin >> abonement;

    double price = choice(abonement);
    std::cout << "Abonement's price is: " << price << std::endl;

    return 0;
}


double choice(int abonement) {

    double price = 0.0;

    if (abonement == 1) {
        std::cout << "You chose Super Abonement" << std::endl;
        return 19.99;
    }
    else if (abonement == 2) {
        std::cout << "You chose VIP Abonement" << std::endl;
        return 15.99;
    }
    else {
        std::cout << "Invalid choice" << std::endl;
    }
    return price;
}