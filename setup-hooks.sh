#!/bin/bash
# Install pre-commit hooks
# Run this after cloning

pip install pre-commit
pre-commit install

echo "✓ Pre-commit hooks installed"
echo "Hooks will run automatically on 'git commit'"
echo ""
echo "To run hooks manually:"
echo "  pre-commit run --all-files"
