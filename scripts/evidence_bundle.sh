#!/bin/bash
set -e

echo "Bundling evidence..."
mkdir -p evidence
cp -r policies evidence/
cp -r spec evidence/
echo "done"
