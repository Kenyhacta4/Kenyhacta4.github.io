#include <iostream>
#include <string>

// Function to check if input contains unsafe SQL characters
bool isValidUserInput(const std::string& input) {
    // Block inputs containing `;` or `'`, which are common in SQL injection
    return input.find(';') == std::string::npos && input.find("'") == std::string::npos;
}

int main() {
    std::string userInput;
    bool validInput = false;

    while (!validInput) {
        std::cout << "Enter a username: ";
        std::getline(std::cin, userInput);

        // Check if the input is safe
        if (isValidUserInput(userInput)) {
            std::cout << "Valid user input.\n";
            validInput = true;  // Exit the loop
        }
        else {
            std::cout << "SQL injection attempt blocked. Please try again.\n";
        }
    }

    return 0;
}