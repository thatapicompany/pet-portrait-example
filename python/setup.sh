#!/bin/bash
set -e

echo "Installing dependencies for Portrait testing..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment 'venv' created."
fi

# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install requests python-dotenv

echo ""
echo "==========================================="
echo "Setup complete! To run the test, execute:"
echo "source venv/bin/activate && python3 create-portraits.py"
echo "==========================================="
