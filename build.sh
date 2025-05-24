#!/usr/bin/env bash
# Build script for Render.com deployment

set -o errexit  # exit on error

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads
mkdir -p results

echo "Build completed successfully!" 