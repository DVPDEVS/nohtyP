# guards for importing internal modules

import inspect
import warnings
from pathlib import Path

pkg_root = Path(__file__).resolve().parents[1]

internal = False

for frame_info in inspect.stack():
    filename = Path(frame_info.filename).resolve()
    if filename.is_relative_to(pkg_root):
        internal = True
        break
