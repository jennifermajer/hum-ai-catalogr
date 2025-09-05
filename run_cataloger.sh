#!/bin/bash
# 
# Document Cataloger Runner Script
# Automatically uses the correct Python version
#

# Get the directory where this script is located
KB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Document Cataloging System"
echo "=========================="

# Change to the knowledge base directory
cd "$KB_DIR" || {
    echo "Error: Could not change to Knowledge Base directory"
    exit 1
}

# Try to find the right Python with required packages
PYTHON_CMD=""

# Check system Python first
if /usr/local/bin/python3 -c "import PyPDF2, requests, pandas; from docx import Document" 2>/dev/null; then
    PYTHON_CMD="/usr/local/bin/python3"
    echo "Using system Python: $PYTHON_CMD"
elif python3 -c "import PyPDF2, requests, pandas; from docx import Document" 2>/dev/null; then
    PYTHON_CMD="python3"
    echo "Using default Python: $PYTHON_CMD"
else
    echo "Error: Required Python packages not found"
    echo "Please run: pip3 install requests PyPDF2 python-docx pandas"
    exit 1
fi

# Run the cataloger with the correct Python
echo "Running document cataloger..."
echo ""

if [ "$1" = "test" ]; then
    $PYTHON_CMD test_cataloger.py
elif [ "$1" = "help" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    $PYTHON_CMD document_cataloger.py --help
else
    $PYTHON_CMD document_cataloger.py "$@"
fi