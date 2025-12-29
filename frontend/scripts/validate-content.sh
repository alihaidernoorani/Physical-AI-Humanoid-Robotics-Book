#!/bin/bash
# T012: Build-time artifact validation script
# This script checks for conversion artifacts that should not exist in production

set -e

DOCS_DIR="${1:-frontend/docs}"
EXIT_CODE=0

echo "=== Content Validation ==="
echo "Checking directory: $DOCS_DIR"
echo ""

# Check for custom Diagram components
echo "Checking for custom <Diagram> components..."
if grep -rn "<Diagram" "$DOCS_DIR" 2>/dev/null; then
  echo "ERROR: Found custom <Diagram> components - these should be converted to Mermaid"
  EXIT_CODE=1
else
  echo "PASS: No custom <Diagram> components found"
fi
echo ""

# Check for "Diagram Description:" artifacts
echo "Checking for 'Diagram Description:' artifacts..."
if grep -rn "Diagram Description:" "$DOCS_DIR" 2>/dev/null; then
  echo "ERROR: Found 'Diagram Description:' artifacts - these should be removed"
  EXIT_CODE=1
else
  echo "PASS: No 'Diagram Description:' artifacts found"
fi
echo ""

# Check for "Figure shows:" placeholders
echo "Checking for 'Figure shows:' placeholders..."
if grep -rn "Figure shows:" "$DOCS_DIR" 2>/dev/null; then
  echo "ERROR: Found 'Figure shows:' placeholder text - these should be removed"
  EXIT_CODE=1
else
  echo "PASS: No 'Figure shows:' placeholders found"
fi
echo ""

# Check for Diagram imports
echo "Checking for Diagram import statements..."
if grep -rn "import Diagram from" "$DOCS_DIR" 2>/dev/null; then
  echo "ERROR: Found Diagram import statements - these should be removed"
  EXIT_CODE=1
else
  echo "PASS: No Diagram import statements found"
fi
echo ""

# Summary
echo "=== Validation Summary ==="
if [ $EXIT_CODE -eq 0 ]; then
  echo "All content validation checks PASSED"
else
  echo "Some content validation checks FAILED"
fi

exit $EXIT_CODE
