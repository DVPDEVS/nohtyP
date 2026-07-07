#!/usr/bin/env bash

# prep
set -euo pipefail
STARTDIR=$(pwd)

# build stage def (only 'beta', 'alpha' or nothing)
NOHTYP_STAGE="beta"
# formatted date
_N_formatted_date=$(date '+%d%m%Y')

modify_buildinfo() {
    case "$1" in
        dev)
            cat <<EOF > ./nohtyP/_buildinfo.py
class BUILD_DATA:
    _BUILD_DATE = "$_N_formatted_date"
    _BUILD_DEVMODE = True
    _BUILD_STAGE = "$NOHTYP_STAGE"
EOF
            ;;
        release)
            cat <<EOF > ./nohtyP/_buildinfo.py
class BUILD_DATA:
    _BUILD_DATE = "$_N_formatted_date"
    _BUILD_DEVMODE = False
    _BUILD_STAGE = "$NOHTYP_STAGE"
EOF
            ;;
        sdist)
            cat <<EOF > ./nohtyP/_buildinfo.py
# modified by build script

class BUILD_DATA:
    _BUILD_DATE = "$_N_formatted_date"
    _BUILD_DEVMODE = False
    _BUILD_STAGE = "$NOHTYP_STAGE"

EOF
            ;;
        source)
            # source baseline
            cat <<EOF > ./nohtyP/_buildinfo.py
# modified by build script

class BUILD_DATA:
    _BUILD_DATE = ""
    _BUILD_DEVMODE = False
    _BUILD_STAGE = ""

EOF
            ;;
    esac
}

cleanup() {
    echo "Cleaning remains..."
    # back to src
    cd ./src || cd "$SCRIPT_DIR/../../../.."
    #remove prebuild files
    rm -rf ./LICENSES 2>/dev/null || true
    # rm pycache
    ./nohtyP/_dev/scripts/sh/clean_cache.sh
    # remove venv
    [ -n "${VIRTUAL_ENV:-}" ] && deactivate || true
    rm -rf "$TEMP_VENV" 2>/dev/null || true
    # reset bi
    modify_buildinfo "source"
    # return to start
    cd "$STARTDIR" || true
}
trap cleanup EXIT

# dir change to src
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../../../.."

# prebuild
## copy or symlink licenses/docs
echo "Copying in files..."
ln -sfn ../LICENSES LICENSES
## clean out dist
echo "Emptying build directory..."
rm -rf ./dist/
## clean out pycache ( rember ´chmod +x clean_cache.sh´)
echo "Removing pycache..."
./nohtyP/_dev/scripts/sh/clean_cache.sh || true

# create temporary venv
echo "Creating venv..."
TEMP_VENV=$(mktemp -d)
python -m venv "$TEMP_VENV"

# shellcheck disable=SC1091
source "$TEMP_VENV/bin/activate"

# update/install deps and then build
echo "Installing build dependencies..."
python -m pip install --upgrade pip
python -m pip install hatch hatchling
echo "Verifying dependencies..."
python -m pip install --upgrade hatch hatchling 1>/dev/null
python -m pip check
## include an envvar for build hook
### starting with non-dev mode
echo "Building..."
modify_buildinfo "release"
_YP_HATCH_BUILD_MODE=release hatch build --target wheel
modify_buildinfo "sdist"
_YP_HATCH_BUILD_MODE=sdist   hatch build --target sdist
modify_buildinfo "dev"
_YP_HATCH_BUILD_MODE=dev     hatch build --target wheel

# find wheels and tarball
shopt -s nullglob
## dev wheels
dwhls=(dist/nohtyp*dev*.whl)
## release wheels
rwhls=(dist/nohtyp*.whl) ; tmp=()
for f in "${rwhls[@]}"; do
    [[ $f == *dev* ]] || tmp+=("$f")
done
rwhls=("${tmp[@]}")
## tarballs
tars=(dist/nohtyp*.tar.gz)
# report count
echo
echo Release wheels found: ${#rwhls[@]}
echo Dev wheels found:     ${#dwhls[@]}
echo Tarballs found:       ${#tars[@]}
# ensure non-zero count
if [[ ${#rwhls[@]} -eq 0 || ${#dwhls[@]} -eq 0 || ${#tars[@]} -eq 0 ]]; then
    echo "Build failed: artifacts not found"
    exit 1
fi
## pick latest of each
latest_rel=${rwhls[0]}
latest_dev=${dwhls[0]}
latest_tar=${tars[0]}

# inspect wheels and tarball
echo
echo === Inspecting release wheel ===
unzip -l "$latest_rel"
echo
echo ===== Inspecting dev wheel =====
unzip -l "$latest_dev"
echo
echo === Inspecting sdist tarball ===
tar -tf "$latest_tar"

# TODO: add smoke test

# cd back so python pulls modules from site-packages instead
cd ..

# bc of set -euo pipefail i dont need to check for errors.
# this script just exits immediately if anything goes wrong
# and then immediately hits the cleanup() trap on EXIT

# test install
echo
echo Testing release install
python -m pip install --no-cache-dir "src/$latest_rel"
echo Executing...
python -m nohtyP
echo "Metadata:"
python -c "from importlib.metadata import metadata; [print(f'{k}: {v}') for k,v in metadata('nohtyP').items() if not k == 'Description']"
echo

# test dev extra
echo
echo Testing dev install
python -m pip uninstall -y nohtyP
python -m pip install --no-cache-dir "src/$latest_dev"
echo Executing...
python -m nohtyP
echo "Metadata:"
python -c "from importlib.metadata import metadata; [print(f'{k}: {v}') for k,v in metadata('nohtyP').items() if not k == 'Description']"
echo

