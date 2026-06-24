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
cd "$SCRIPT_DIR/../../../.."

# prebuild
## copy or symlink licenses/docs
ln -sfn ../LICENSES LICENSES
## clean out dist
rm -rf ./dist/
## clean out pycache ( rember ´chmod +x clean_cache.sh´)
./clean_cahche.sh

# create temporary venv
TEMP_VENV=$(mktemp -d)
python -m venv "$TEMP_VENV"

# shellcheck disable=SC1091
source "$TEMP_VENV/bin/activate"

# update/install deps and then build
python -m pip install --upgrade pip
python -m pip install hatch hatchling
python -m pip install --upgrade hatch hatchling
## include an envvar for build hook
_YP_HATCH_BUILD_MODE=release hatch build --target wheel
_YP_HATCH_BUILD_MODE=sdist   hatch build --target sdist
_YP_HATCH_BUILD_MODE=dev     hatch build --target wheel

# find wheel and tarball
shopt -s nullglob
dwhls=(dist/nohtyP*dev*.whl)
rwhls=(dist/nohtyP*release*.whl)
tars=(dist/nohtyP*.tar.gz)
if [[ ${#rwhls[@]} -eq 0 || ${#dwhls[@]} -eq 0 || ${#tars[@]} -eq 0 ]]; then
    echo "Build failed: artifacts not found"
    exit 1
fi
latest_rel=${rwhls[0]}
latest_dev=${dwhls[0]}
latest_tar=${tars[0]}

# inspect latest wheel and tar.gz
unzip -l "$latest_rel"
unzip -l "$latest_dev"
tar -tf "$latest_tar"

# TODO: add smoke test

# test install
python -m pip install --no-cache-dir "$latest_rel"
python -c "import nohtyP"

# test dev extra
python -m pip uninstall -y nohtyP
python -m pip install --no-cache-dir "$latest_dev"
python -c "import nohtyP"

