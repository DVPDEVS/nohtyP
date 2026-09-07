#!/usr/bin/env bash

# prep
set -euo pipefail
STARTDIR=$(pwd)

cleanup() {
    echo "Cleaning remains..."
    # rm pycache
    ./nohtyP/_dev/scripts/sh/clean_cache.sh
    # remove venv
    [ -n "${VIRTUAL_ENV:-}" ] && deactivate || true
    rm -rf "$TEMP_VENV" 2>/dev/null || true
    # return to start
    cd "$STARTDIR" || true
}
trap cleanup EXIT

# dir change to src
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../../../.."

# define targets
TARGET="dist/*"

# arg handling
if (( $# >= 1 )); then
    _MODE="$1"
    if (( $# == 2 )); then
        if [ "$2" = "install" ]; then
            INSTALL="1"
        fi
    fi
fi

# fast exit
if [ -z "$_MODE" ]; then
    echo "Usage: $0 <mode> [install]" >&2
    exit 1
fi

# create temporary venv
echo "Creating venv..."
TEMP_VENV=$(mktemp -d)
python -m venv "$TEMP_VENV"

# shellcheck disable=SC1091
source "$TEMP_VENV/bin/activate"

# update/install deps and then build
echo "Installing build dependencies..."
python3 -m pip install --upgrade pip  &> 1> 2> /dev/null
python3 -m pip install --upgrade twine  &> 1> 2> /dev/null
echo "Verifying dependencies..."
python3 -m pip check

# try to upload
case "$_MODE" in
    test)
        python3 -m twine upload -r testpypi dist/*
        ;;
    release)
        python3 -m twine upload -r testpypi dist/*
        ;;
    *)
        echo "Unknown upload option: '$_MODE'" >&2
        echo "    Expected 'test' or 'release'!" >&2
        exit 1
        ;;
esac
