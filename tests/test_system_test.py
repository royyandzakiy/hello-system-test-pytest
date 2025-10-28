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
    print(f"[SEARCH] Looking for hello_threads executable...")
    
    # If build_dir is provided, check there first
    if build_dir:
        possible_paths = [
            os.path.join(build_dir, "hello_threads"),
            os.path.join(build_dir, "hello_threads.exe"),
            os.path.join(build_dir, "Debug/hello_threads.exe"),
            os.path.join(build_dir, "Release/hello_threads.exe"),
        ]
    else:
        # Check common build directories
        possible_paths = [
            "./hello_threads",
            "./hello_threads.exe",
            "./build/hello_threads",
            "./build/hello_threads.exe", 
            "./build/Debug/hello_threads.exe",
            "./build/Release/hello_threads.exe",
            "../hello_threads",
            "../hello_threads.exe",
            "hello_threads",
            "hello_threads.exe"
        ]
    
    for path in possible_paths:
        if os.path.exists(path) and os.path.isfile(path):
            print(f"[SUCCESS] Found executable at: {os.path.abspath(path)}")
            return os.path.abspath(path)
        else:
            print(f"[MISSING] Not found: {path}")
    
    # Try to find in system PATH
    try:
        import shutil
        path = shutil.which("hello_threads")
        if path:
            print(f"[SUCCESS] Found executable in PATH: {path}")
            return path
    except:
        pass
    
    print("[ERROR] Executable not found in any common locations")
    return None

class TestHelloThreads:
    """Test cases for the hello_threads executable."""
    
    @classmethod
    def setup_class(cls):
        """Find the executable before running tests."""
        print("\n" + "="*60)
        print("[SETUP] Setting up HelloThreads tests")
        print("="*60)
        
        # Try to get build directory from environment (set by CMake/CTest)
        build_dir = os.environ.get('CMAKE_BINARY_DIR')
        if not build_dir:
            build_dir = "./build"  # Default build directory
        
        print(f"[INFO] Build directory: {build_dir}")
        cls.executable_path = find_executable(build_dir)
        
        if cls.executable_path is None:
            pytest.skip("hello_threads executable not found")
        else:
            print(f"[INFO] Testing executable: {cls.executable_path}")
    
    def test_executable_exists(self):
        """Test that the executable exists and is executable."""
        print(f"\n[TEST] Running test: test_executable_exists")
        assert os.path.exists(self.executable_path), f"Executable not found at {self.executable_path}"
        assert os.path.isfile(self.executable_path), f"Path is not a file: {self.executable_path}"
        assert os.access(self.executable_path, os.X_OK), f"Executable not executable: {self.executable_path}"
        print("[SUCCESS] Executable exists and is executable")
    
    def test_program_runs(self):
        """Test that the program runs without errors."""
        print(f"\n[TEST] Running test: test_program_runs")
        print(f"[COMMAND] Running: {self.executable_path}")
        
        result = subprocess.run([self.executable_path], 
                              capture_output=True, text=True, timeout=10)
        
        print(f"[OUTPUT] Program stdout ({len(result.stdout)} chars):")
        print("--- stdout begin ---")
        print(result.stdout)
        print("--- stdout end ---")
        
        if result.stderr:
            print(f"[OUTPUT] Program stderr ({len(result.stderr)} chars):")
            print("--- stderr begin ---")
            print(result.stderr)
            print("--- stderr end ---")
        
        assert result.returncode == 0, f"Program failed with return code {result.returncode}"
        assert result.stderr == "", f"Program produced stderr: {result.stderr}"
        print("[SUCCESS] Program runs successfully without errors")
    
    def test_output_contains_expected_messages(self):
        """Test that the output contains expected messages."""
        print(f"\n[TEST] Running test: test_output_contains_expected_messages")
        
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
        
        print("[CHECK] Checking for expected messages:")
        for message in expected_messages:
            if message in output:
                print(f"   [FOUND] '{message}'")
            else:
                print(f"   [MISSING] '{message}'")
            assert message in output, f"Expected message '{message}' not found in output"
        
        print("[SUCCESS] All expected messages found in output")
    
    def test_thread_messages_in_output(self):
        """Test that thread hello messages appear in output."""
        print(f"\n[TEST] Running test: test_thread_messages_in_output")
        
        result = subprocess.run([self.executable_path], 
                              capture_output=True, text=True, timeout=10)
        
        output = result.stdout
        
        # Check that we have thread messages
        thread_messages = [line for line in output.split('\n') if "Hello from thread" in line]
        
        print(f"[INFO] Found {len(thread_messages)} thread messages:")
        for msg in thread_messages:
            print(f"   [THREAD] {msg}")
        
        assert len(thread_messages) >= 5, f"Expected at least 5 thread messages, got {len(thread_messages)}"
        
        # Verify thread IDs 1-5 are present
        thread_ids_found = []
        for message in thread_messages:
            for i in range(1, 6):
                if f"Hello from thread {i}!" in message:
                    thread_ids_found.append(i)
                    break
        
        print(f"[INFO] Thread IDs found: {sorted(thread_ids_found)}")
        print(f"[INFO] Thread IDs expected: {list(range(1, 6))}")
        
        # We should find all thread IDs 1-5 (order doesn't matter due to threading)
        assert set(thread_ids_found) == set(range(1, 6)), f"Not all thread IDs found. Found: {thread_ids_found}"
        print("[SUCCESS] All thread IDs (1-5) found in output")

def test_output_in_correct_order():
    """Test that main thread messages appear in logical order."""
    print(f"\n[TEST] Running test: test_output_in_correct_order")
    
    build_dir = os.environ.get('CMAKE_BINARY_DIR')
    if not build_dir:
        build_dir = "./build"
    
    executable_path = find_executable(build_dir)
    
    if executable_path is None:
        pytest.skip("hello_threads executable not found")
    
    result = subprocess.run([executable_path], 
                          capture_output=True, text=True, timeout=10)
    
    output = result.stdout
    lines = [line.strip() for line in output.split('\n') if line.strip()]
    
    print("[OUTPUT] Program output lines:")
    for i, line in enumerate(lines):
        print(f"   {i:2d}: {line}")
    
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
    
    print("[POSITIONS] Message positions:")
    print(f"   Main start: {main_start_idx}")
    print(f"   Creating threads: {creating_threads_idx}") 
    print(f"   Waiting: {waiting_idx}")
    print(f"   Completed: {completed_idx}")
    print(f"   Exiting: {exiting_idx}")
    
    # Verify logical order of main thread messages
    assert main_start_idx is not None and creating_threads_idx is not None, "Required messages not found"
    assert main_start_idx < creating_threads_idx, "Main start should come before creating threads"
    assert creating_threads_idx < waiting_idx, "Creating threads should come before waiting"
    assert waiting_idx < completed_idx, "Waiting should come before completion"
    assert completed_idx < exiting_idx, "Completion should come before exiting"
    
    print("[SUCCESS] Main thread messages in correct logical order")

if __name__ == "__main__":
    # Allow running the test directly
    pytest.main([__file__, "-v", "-s", "--tb=short"])