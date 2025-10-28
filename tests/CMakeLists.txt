# Find Python and pytest
find_package(Python3 COMPONENTS Interpreter REQUIRED)

# Check if pytest is available
execute_process(
    COMMAND ${Python3_EXECUTABLE} -m pytest --version
    RESULT_VARIABLE PYTEST_FOUND
    OUTPUT_QUIET
    ERROR_QUIET
)

if(PYTEST_FOUND EQUAL 0)
    message(STATUS "pytest found: will add system tests")
    
    # Add custom target to run system tests
    add_custom_target(run_system_tests
        COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py -v
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        DEPENDS hello_threads
        COMMENT "Running system tests with pytest"
    )
    
    # Add test that can be run with ctest
    add_test(
        NAME system_test
        COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py -v
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    )
    
    # Set properties for the test
    set_tests_properties(system_test PROPERTIES
        TIMEOUT 30
        LABELS "system"
    )
    
else()
    message(WARNING "pytest not found: system tests will not be available")
endif()

# Add a custom target to build and run all tests
add_custom_target(check
    COMMAND ${CMAKE_CTEST_COMMAND} --output-on-failure
    DEPENDS hello_threads
    COMMENT "Building and running all tests"
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)