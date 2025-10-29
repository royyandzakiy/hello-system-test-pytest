pipeline {
    agent any

    parameters {
        choice(name: 'CMAKE_PRESET', choices: ['default', 'release'], description: 'Select CMake build preset')
        choice(name: 'TEST_PRESET', choices: ['minimal', 'verbose', 'full-output'], description: 'Select CTest preset')
        choice(name: 'PYTEST_MODE', choices: ['pytest-minimal', 'pytest-verbose', 'pytest-full'], description: 'Select Pytest run mode')
    }

    environment {
        BUILD_DIR = "build"
        PYTHON = "python" // or "python3" if needed
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Configure') {
            steps {
                powershell '''
                if (Test-Path $env:BUILD_DIR) {
                    Remove-Item -Recurse -Force $env:BUILD_DIR
                }
                cmake --preset $env:CMAKE_PRESET
                '''
            }
        }

        stage('Build') {
            steps {
                powershell '''
                if (Test-Path "$env:BUILD_DIR/Makefile") {
                    Write-Host "Detected Makefile - using make"
                    cmake --build --preset $env:CMAKE_PRESET
                } else {
                    Write-Host "Using MSBuild"
                    cmake --build --preset $env:CMAKE_PRESET -- /m
                }
                '''
            }
        }

        stage('CTest') {
            steps {
                powershell '''
                # Run tests and produce XML output Jenkins can read
                ctest -T Test --preset $env:TEST_PRESET --output-on-failure
                '''
            }
        }

        stage('Pytest') {
            steps {
                powershell '''
                if ($env:PYTEST_MODE -eq "pytest-minimal") {
                    pytest -q
                } elseif ($env:PYTEST_MODE -eq "pytest-verbose") {
                    pytest -v
                } else {
                    pytest -s -v
                }
                '''
            }
        }
    }

    post {
        always {
            echo "Archiving CTest and Pytest results..."

            // Archive CTest XML results
            catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                junit allowEmptyResults: true, testResults: 'build/Testing/**/*.xml'
            }

            // (Optional) archive pytest results if they exist
            catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                junit allowEmptyResults: true, testResults: 'pytest-results.xml'
            }
        }

        failure {
            echo "Pipeline failed."
        }
    }
}
