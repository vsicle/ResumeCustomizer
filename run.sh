#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "=== Resume Compiler ==="
echo "Running builder..."
python src/builder.py

echo ""
echo "Done!"
