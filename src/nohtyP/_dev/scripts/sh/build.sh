#!/usr/bin/env bash

# prep
set -euo pipefail
STARTDIR=$(pwd)

# build stage def
NOHTYP_STAGE="beta"
# formatted date
_N_formatted_date=$(date '+%d%m%Y')

modify_buildinfo() {
    case "$1" in
        dev)
            cat <<'EOF' > ./nohtyP/_buildinfo.py
class BUILD_DATA:
    _BUILD_DATE = "$_N_formatted_date"
    _BUILD_DEVMODE = True
    _BUILD_STAGE = "$NOHTYP_STAGE"
EOF
            ;;
        release)
            cat <<'EOF' > ./nohtyP/_buildinfo.py
class BUILD_DATA:
    _BUILD_DATE = "$_N_formatted_date"
    _BUILD_DEVMODE = False
    _BUILD_STAGE = "$NOHTYP_STAGE"
EOF
            ;;
        sdist)
            cat <<'EOF' > ./nohtyP/_buildinfo.py
# modified by build script

class BUILD_DATA:
    _BUILD_DATE = "$_N_formatted_date"
    _BUILD_DEVMODE = False
    _BUILD_STAGE = "$NOHTYP_STAGE"

EOF
            ;;
        source)
            # source baseline
            cat <<'EOF' > ./nohtyP/_buildinfo.py
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
ln -sfn ../LICENSES LICENSES
## clean out dist
rm -rf ./dist/
## clean out pycache ( rember ´chmod +x clean_cache.sh´)
./nohtyP/_dev/scripts/sh/clean_cache.sh || true

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
### starting with non-dev mode
echo "_BUILD_DEVMODE = False" >> ./nohtyP/__about__.py
_YP_HATCH_BUILD_MODE=release hatch build --target wheel
_YP_HATCH_BUILD_MODE=sdist   hatch build --target sdist
### switch to dev mode
head -n -1 ./nohtyP/__about__.py > tmp && mv tmp ./nohtyP/__about__.py
echo "_BUILD_DEVMODE = True" >> ./nohtyP/__about__.py
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

# test install
echo
echo Testing release install
python -m pip install --no-cache-dir "$latest_rel"
echo Executing...
python -m nohtyP

# test dev extra
echo
echo Testing dev install
python -m pip uninstall -y nohtyP
python -m pip install --no-cache-dir "$latest_dev"
echo Executing...
python -m nohtyP

