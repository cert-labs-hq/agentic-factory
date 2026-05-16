#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Check for the virtual environment (.venv) and activate it if present.
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to activate virtual environment. Exiting."
        exit 1
    fi
fi

# Execute the tests using pytest, outputting a verbose log.
echo "Executing tests in /tests folder with pytest -v..."
pytest -v tests/
TEST_EXIT_CODE=$?

# Deactivate the virtual environment if it was activated.
# This ensures a clean state, particularly important if the script is sourced
# or for consistent behavior in CI/CD pipelines.
if [ -d ".venv" ] && type deactivate &> /dev/null; then
    echo "Deactivating virtual environment..."
    deactivate
fi

# Include clean exit codes to integrate cleanly into an upstream IDP/CI pipeline.
# The script exits with pytest's exit code.
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "All tests passed successfully."
else
    echo "Tests failed. Pytest exited with code: $TEST_EXIT_CODE"
fi

exit $TEST_EXIT_CODE