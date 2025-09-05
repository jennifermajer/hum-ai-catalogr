#!/bin/bash

echo "Setting up Document Cataloging System"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    exit 1
fi

# Install requirements
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Warning: Ollama is not installed"
    echo "Please install Ollama from: https://ollama.ai"
    echo "Then run: ollama pull llama3.2"
else
    echo "Ollama found, checking if llama3.2 model is available..."
    if ! ollama list | grep -q "llama3.2"; then
        echo "Pulling llama3.2 model..."
        ollama pull llama3.2
    else
        echo "llama3.2 model is already available"
    fi
fi

echo ""
echo "Setup complete!"
echo "To run the cataloger:"
echo "  python3 document_cataloger.py"
echo ""
echo "Make sure Ollama is running before executing:"
echo "  ollama serve"