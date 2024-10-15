#!/bin/bash

# Check if the .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found."
    exit 1
fi

# Load environment variables from the .env file
export $(grep -v '^#' .env | xargs)

# Check if uvicorn is installed
if ! command -v uvicorn &> /dev/null
then
    echo "uvicorn could not be found, installing it..."
    pip install uvicorn
fi

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8888