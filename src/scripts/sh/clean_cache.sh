#!/usr/bin/env bash
set -euo pipefail
find . -type d -iname "__pycache__" -exec rm -rf {} +
# pycache is gitignored, but to clean it locally this can be nice.
