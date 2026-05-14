#!/bin/bash
set -e

echo "Installing dependencies..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "Verifying gunicorn installation..."
which gunicorn || pip install gunicorn

echo "Build complete!"
