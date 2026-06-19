#!/usr/bin/env bash

# prep
set -euo pipefail
STARTDIR=$(pwd)

cleanup() {
    #remove prebuild files
    rm -rf ./LICENSES 2>/dev/null || true
    # remove venv
    [ -n "${VIRTUAL_ENV:-}" ] && deactivate || true
    rm -rf "$TEMP_VENV" 2>/dev/null || true
    # return to start
    cd "$STARTDIR" || true
}
trap cleanup EXIT

# dir change to src
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../../.."

# prebuild
## copy or symlink licenses/docs
ln -sfn ../LICENSES/ ./LICENSES/
## clean out dist
rm -rf ./dist/

# create temporary venv
TEMP_VENV=$(mktemp -d)
python -m venv "$TEMP_VENV"

# shellcheck disable=SC1091
source "$TEMP_VENV/bin/activate"

# update/install deps and then build
python -m pip install --upgrade pip
python -m pip install hatch hatchling
python -m pip install --upgrade hatch hatchling
hatch build --target wheel
hatch build --target wheel-dev
hatch build --target sdist

# find wheel and tarball
shopt -s nullglob
whls=(dist/nohtyP*.whl)
tars=(dist/nohtyP*.tar.gz)
if [[ ${#whls[@]} -eq 0 || ${#tars[@]} -eq 0 ]]; then
    echo "Build failed: artifacts not found"
    exit 1
fi
latest_whl=${whls[0]}
latest_tar=${tars[0]}

# inspect latest wheel and tar.gz
unzip -l "$latest_whl"
tar -tf "$latest_tar"

# TODO: add smoke test

# test install
python -m pip install --no-cache-dir "$latest_whl"
python -c "import nohtyP"

# test dev extra
python -m pip uninstall -y nohtyP
python -m pip install --no-cache-dir "$latest_whl[dev]"
python -c "import nohtyP"

