#!/usr/bin/env bash
set -euo pipefail

# prebuild
## copy or symlink licenses and readme/other docs

# build
python -m build

# inspect, optional
unzip -l dist/*.whl
tar -tf dist/*.tar.gz

# optional test
pip install dist/nohtyP-0.0.1-py3-none-any.whl
echo "import nohtyP" | python -


