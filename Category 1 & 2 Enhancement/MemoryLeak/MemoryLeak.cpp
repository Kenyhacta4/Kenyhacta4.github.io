#include <iostream>
using namespace std;

void allocateMemory(int size) {
    int* data = new int[size];
    data[0] = 1;  // Simulate use of memory
    delete[] data; // Ensure memory is freed
    std::cout << "Memory allocation and deallocation test complete.\n";
}

int main() {
    int size;
    std::cout << "Enter the number of integers to allocate: ";
    std::cin >> size;
    allocateMemory(size);

    return 0;
}