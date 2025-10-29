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
    
    # Add custom target to run system tests with verbose output
    add_custom_target(run_system_tests_verbose
        COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py -v --tb=short
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        DEPENDS hello_threads
        COMMENT "Running system tests with verbose pytest output"
    )
    
    # Add custom target with full output
    add_custom_target(run_system_tests_full
        COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py -v -s --tb=short
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        DEPENDS hello_threads
        COMMENT "Running system tests with full output (no capture)"
    )
    
    # Test 0: Minimal output with Report (for CI)
    add_test(
        NAME system_test_minimal_report
        COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py --tb=short
		--junitxml=${CMAKE_BINARY_DIR}/pytest-results/system_test_minimal_report.xml
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    )
    
    # Test 1: Minimal output (for CI/quick runs)
    add_test(
        NAME system_test_minimal
        COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py --tb=short
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    )
    
    # Test 2: Verbose output (shows test names)
    add_test(
        NAME system_test_verbose
        COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py -v --tb=short
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    )
    
    # Test 3: Full output with print statements (for debugging)
    add_test(
        NAME system_test_full_output
        COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py -v -s --tb=short
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    )
    
    # Set properties for the tests
    set_tests_properties(system_test_minimal_report PROPERTIES
        TIMEOUT 30
        LABELS "system;minimal;report"
    )

    set_tests_properties(system_test_minimal PROPERTIES
        TIMEOUT 30
        LABELS "system;minimal"
    )
    
    set_tests_properties(system_test_verbose PROPERTIES
        TIMEOUT 30
        LABELS "system;verbose"
        PASS_REGULAR_EXPRESSION "PASSED"
        FAIL_REGULAR_EXPRESSION "FAILED|ERROR"
    )
    
    set_tests_properties(system_test_full_output PROPERTIES
        TIMEOUT 30
        LABELS "system;full;debug"
        PASS_REGULAR_EXPRESSION "PASSED|SUCCESS"
        FAIL_REGULAR_EXPRESSION "FAILED|ERROR"
    )
    
    # ============================================================================
    # DIRECT PYTEST TARGETS (Bypass CTest completely - Clean output)
    # ============================================================================
    
    # Pytest minimal - clean dots output
    add_custom_target(pytest_minimal
        COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py --tb=short
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        DEPENDS hello_threads
        COMMENT "Running pytest directly with minimal output (clean dots)"
    )
    
    # Pytest verbose - clean test names with progress
    add_custom_target(pytest_verbose
        COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py -v --tb=short
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        DEPENDS hello_threads
        COMMENT "Running pytest directly with verbose output (clean test names)"
    )
    
    # Pytest full - clean output with all prints
    add_custom_target(pytest_full
        COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py -v -s --tb=short
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        DEPENDS hello_threads
        COMMENT "Running pytest directly with full output (clean with all prints)"
    )
    
    # Alias targets for backward compatibility
    add_custom_target(pytest_direct
        COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py -v --tb=short
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        DEPENDS hello_threads
        COMMENT "Running pytest directly (bypass CTest)"
    )
    
    add_custom_target(pytest_direct_full
        COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py -v -s --tb=short
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        DEPENDS hello_threads
        COMMENT "Running pytest directly with full output"
    )
    
else()
    message(WARNING "pytest not found: system tests will not be available")
endif()

# ============================================================================
# CTest-based targets (for compatibility)
# ============================================================================

# Add a custom target to build and run all tests
add_custom_target(check
    COMMAND ${CMAKE_CTEST_COMMAND} --output-on-failure
    DEPENDS hello_threads
    COMMENT "Building and running all tests"
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)

# Add custom target for verbose testing
add_custom_target(check_verbose
    COMMAND ${CMAKE_CTEST_COMMAND} --verbose --output-on-failure
    DEPENDS hello_threads
    COMMENT "Building and running all tests with verbose output"
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)

# Add custom target that shows ALL output (like running pytest directly)
add_custom_target(check_full_output
    COMMAND ${CMAKE_CTEST_COMMAND} -R system_test_full_output --verbose --output-on-failure
    DEPENDS hello_threads
    COMMENT "Running tests with full output (like direct pytest)"
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)

# ============================================================================
# Combined build+test targets for direct pytest
# ============================================================================

# Build and run pytest minimal
add_custom_target(build_and_pytest_minimal
    COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py --tb=short
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    DEPENDS hello_threads
    COMMENT "Building and running pytest with minimal output"
)

# Build and run pytest verbose  
add_custom_target(build_and_pytest_verbose
    COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py -v --tb=short
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    DEPENDS hello_threads
    COMMENT "Building and running pytest with verbose output"
)

# Build and run pytest full (recommended for development)
add_custom_target(build_and_pytest_full
    COMMAND ${Python3_EXECUTABLE} -m pytest ${CMAKE_CURRENT_SOURCE_DIR}/test_system_test.py -v -s --tb=short
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    DEPENDS hello_threads
    COMMENT "Building and running pytest with full output (recommended for development)"
)