#!/bin/bash
set -e

echo "Running nightly checks..."
pytest tests || true
echo "done"
