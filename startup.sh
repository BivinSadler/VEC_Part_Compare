#!/bin/bash

# Optional: Print the working directory and environment variables for debugging
echo "Starting Streamlit app..."
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"

# Run the Streamlit app on the port Azure provides
streamlit run VEC.py --server.port $PORT --server.enableCORS false

