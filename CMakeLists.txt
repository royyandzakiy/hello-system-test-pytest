cmake_minimum_required(VERSION 3.15)
project(HelloThreads VERSION 1.0.0 DESCRIPTION "A simple threaded Hello World example")

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Threads package
find_package(Threads REQUIRED)

# Add executable
add_executable(hello_threads src/main.cpp)

# Link threads library
target_link_libraries(hello_threads Threads::Threads)

# Install target (optional, for system-wide installation)
install(TARGETS hello_threads DESTINATION bin)

# Add tests subdirectory
enable_testing()
add_subdirectory(tests)