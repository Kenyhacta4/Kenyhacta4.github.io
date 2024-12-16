#include <iostream>
#include <string>
#include <cstring>

void safeCopy(const char* input) {
    char buffer[10];
    // Use strncpy_s with buffer limit and the maximum length of buffer
    strncpy_s(buffer, sizeof(buffer), input, _TRUNCATE); // Safe copy
    std::cout << "Copied to buffer: " << buffer << std::endl;
}

int main() {
    std::string userInput;
    bool validInput = false;

    while (!validInput) {
        std::cout << "Enter a string to copy (max 9 characters): ";
        std::getline(std::cin, userInput); // Get input from the user

        if (userInput.length() < 10) {  // Check if input length is within the buffer size
            safeCopy(userInput.c_str()); // Pass the user input to safeCopy function
            validInput = true;           // Set validInput to true to exit the loop
        }
        else {
            std::cerr << "Error: Input exceeds buffer size. Please try again.\n";
        }
    }

    return 0;
}
