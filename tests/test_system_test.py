#!/usr/bin/env python3
"""
System test for the hello_threads executable using pytest.
"""

import subprocess
import os
import sys
import pytest

def find_executable(build_dir=None):
    """Find the hello_threads executable."""
    # If build_dir is provided, check there first
    if build_dir:
        possible_paths = [
            os.path.join(build_dir, "hello_threads"),
            os.path.join(build_dir, "hello_threads.exe"),
        ]
    else:
        # Check common build directories
        possible_paths = [
            "./hello_threads",
            "./hello_threads.exe",
            "../hello_threads", 
            "../hello_threads.exe",
            "../../hello_threads",
            "../../hello_threads.exe",
            "hello_threads",
            "hello_threads.exe"
        ]
    
    for path in possible_paths:
        if os.path.exists(path) and os.path.isfile(path):
            return os.path.abspath(path)
    
    # Try to find in system PATH
    try:
        import shutil
        path = shutil.which("hello_threads")
        if path:
            return path
    except:
        pass
    
    return None

class TestHelloThreads:
    """Test cases for the hello_threads executable."""
    
    @classmethod
    def setup_class(cls):
        """Find the executable before running tests."""
        # Try to get build directory from environment (set by CMake/CTest)
        build_dir = os.environ.get('CMAKE_BINARY_DIR')
        cls.executable_path = find_executable(build_dir)
        
        if cls.executable_path is None:
            pytest.skip("hello_threads executable not found")
        else:
            print(f"Testing executable: {cls.executable_path}")
    
    def test_executable_exists(self):
        """Test that the executable exists and is executable."""
        assert os.path.exists(self.executable_path), f"Executable not found at {self.executable_path}"
        assert os.path.isfile(self.executable_path), f"Path is not a file: {self.executable_path}"
        assert os.access(self.executable_path, os.X_OK), f"Executable not executable: {self.executable_path}"
    
    def test_program_runs(self):
        """Test that the program runs without errors."""
        result = subprocess.run([self.executable_path], 
                              capture_output=True, text=True, timeout=10)
        
        assert result.returncode == 0, f"Program failed with return code {result.returncode}"
        assert result.stderr == "", f"Program produced stderr: {result.stderr}"
    
    def test_output_contains_expected_messages(self):
        """Test that the output contains expected messages."""
        result = subprocess.run([self.executable_path], 
                              capture_output=True, text=True, timeout=10)
        
        output = result.stdout
        expected_messages = [
            "Main thread starting...",
            "Creating 5 threads...",
            "All threads created, waiting for completion...",
            "All threads completed!",
            "Main thread exiting."
        ]
        
        for message in expected_messages:
            assert message in output, f"Expected message '{message}' not found in output"
    
    def test_thread_messages_in_output(self):
        """Test that thread hello messages appear in output."""
        result = subprocess.run([self.executable_path], 
                              capture_output=True, text=True, timeout=10)
        
        output = result.stdout
        
        # Check that we have thread messages
        thread_messages = [line for line in output.split('\n') if "Hello from thread" in line]
        
        assert len(thread_messages) >= 5, f"Expected at least 5 thread messages, got {len(thread_messages)}"
        
        # Verify thread IDs 1-5 are present
        thread_ids_found = []
        for message in thread_messages:
            for i in range(1, 6):
                if f"Hello from thread {i}!" in message:
                    thread_ids_found.append(i)
                    break
        
        # We should find all thread IDs 1-5 (order doesn't matter due to threading)
        assert set(thread_ids_found) == set(range(1, 6)), f"Not all thread IDs found. Found: {thread_ids_found}"

def test_output_in_correct_order():
    """Test that main thread messages appear in logical order."""
    build_dir = os.environ.get('CMAKE_BINARY_DIR')
    executable_path = find_executable(build_dir)
    
    if executable_path is None:
        pytest.skip("hello_threads executable not found")
    
    result = subprocess.run([executable_path], 
                          capture_output=True, text=True, timeout=10)
    
    output = result.stdout
    lines = [line.strip() for line in output.split('\n') if line.strip()]
    
    # Find indices of key messages
    main_start_idx = None
    creating_threads_idx = None
    waiting_idx = None
    completed_idx = None
    exiting_idx = None
    
    for i, line in enumerate(lines):
        if "Main thread starting..." in line:
            main_start_idx = i
        elif "Creating 5 threads..." in line:
            creating_threads_idx = i
        elif "All threads created, waiting for completion..." in line:
            waiting_idx = i
        elif "All threads completed!" in line:
            completed_idx = i
        elif "Main thread exiting." in line:
            exiting_idx = i
    
    # Verify logical order of main thread messages
    assert main_start_idx is not None and creating_threads_idx is not None, "Required messages not found"
    assert main_start_idx < creating_threads_idx, "Main start should come before creating threads"
    assert creating_threads_idx < waiting_idx, "Creating threads should come before waiting"
    assert waiting_idx < completed_idx, "Waiting should come before completion"
    assert completed_idx < exiting_idx, "Completion should come before exiting"

if __name__ == "__main__":
    # Allow running the test directly
    pytest.main([__file__, "-v"])