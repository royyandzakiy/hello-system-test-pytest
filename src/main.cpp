#include <iostream>
#include <thread>
#include <vector>
#include <chrono>

void hello_from_thread(int thread_id) {
    std::this_thread::sleep_for(std::chrono::milliseconds(100 * thread_id));
    std::cout << "Hello from thread " << thread_id << "!" << std::endl;
}

int main() {
    std::cout << "Main thread starting..." << std::endl;
    std::cout << "Creating 5 threads..." << std::endl;
    
    std::vector<std::thread> threads;
    
    // Create 5 threads
    for (int i = 1; i <= 5; ++i) {
        threads.emplace_back(hello_from_thread, i);
    }
    
    std::cout << "All threads created, waiting for completion..." << std::endl;
    
    // Wait for all threads to complete
    for (auto& thread : threads) {
        thread.join();
    }
    
    std::cout << "All threads completed!" << std::endl;
    std::cout << "Main thread exiting." << std::endl;
    
    return 0;
}