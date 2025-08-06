#!/bin/bash

# Debug information
echo "=== ClassCompass Execution Log - $(date) ==="
echo "Current directory: $(pwd)"
echo "User: $(whoami)"

# Set environment variables explicitly (fallback if not set by cron)
export VENV="${VENV:-/opt/venv/bin/activate}"
export SOURCE="${SOURCE:-/home/navigator/classcompass}"
export DB_PATH="${DB_PATH:-/home/navigator/classcompass/maps.db}"

echo "Environment variables:"
echo "  SOURCE: $SOURCE"
echo "  DB_PATH: $DB_PATH" 
echo "  VENV: $VENV"

# Try to source bashrc (may not work in cron, but won't hurt)
if [ -f /home/navigator/.bashrc ]; then
    source /home/navigator/.bashrc
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [ -f "$VENV" ]; then
    source "$VENV"
    echo "Virtual environment activated"
else
    echo "Warning: Virtual environment not found at $VENV"
fi

# Change to source directory
echo "Changing to source directory: $SOURCE"
cd "$SOURCE" || {
    echo "ERROR: Cannot change to directory $SOURCE"
    exit 1
}

# Verify we're in the right place
echo "Current directory after cd: $(pwd)"

# Execute the main script
echo "Executing athena.py..."
python3 "$SOURCE/main/athena.py"
exit_code=$?

echo "Execution completed with exit code: $exit_code"
echo "=== End of execution - $(date) ==="
echo ""

exit $exit_code