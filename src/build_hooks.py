from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import os
from pathlib import Path

class WheelHook(BuildHookInterface):
    """
    Custom hook that renames the wheel file based on the target mode:
    - wheel     -> nohtyP-<version>-<tags>.whl
    - dev       -> nohtyP-<version>-dev-<tags>.whl

    And modifies included/excluded files based on `_YP_HATCH_BUILD_MODE´.
    """

    def _load_common_include(self) -> dict:
        out:dict[str,str] = {
            "nohtyP/py.typed": "nohtyP/py.typed",
            "README.md": "README.md",
        }
        # LICENSES
        ldir:Path = Path("LICENSES")
        if ldir.exists():
            for file in ldir.rglob("*"):
                if file.is_file():
                    rel = file.as_posix()
                    out[rel] = rel
        return out

    def initialize(self, version: str, build_data: dict) -> None:
        mode:str = os.getenv("_YP_HATCH_BUILD_MODE", "release")
        print(f"YP Build mode: '{mode}'")
        build_data.setdefault("force_include", {})
        build_data.setdefault("exclude", [])
        # IMPORTANT: we stop trusting glob exclusion entirely for correctness
        build_data["exclude"].clear()
        # reset-safe include (baseline)
        build_data["force_include"].clear()
        build_data["force_include"].update(self._load_common_include())
        # include helper
        def include_file(path: Path):
            build_data["force_include"][path.as_posix()] = path.as_posix()
        # allow file helper
        def is_allowed(path: Path, *, allow_dev: bool = False, allow_scripts: bool = False) -> bool:
            # hard block bytecode always
            if "__pycache__" in path.parts:
                return False
            # dev isolation rule
            if "_dev" in path.parts:
                # script rule, should only appear in sdist
                if "scripts" in path.parts:
                    return allow_scripts
                else:
                    return allow_dev
            return True
        # -------------------------
        # DEV MODE
        # -------------------------
        if mode == "dev":
            root = Path("nohtyP")
            for file in root.rglob("*"):
                if file.is_file() and is_allowed(file, allow_dev=True):
                    include_file(file)
            include_file(Path("build_hooks.py"))
        # -------------------------
        # SDIST MODE
        # -------------------------
        elif mode == "sdist":
            root = Path("nohtyP")
            for file in root.rglob("*"):
                if file.is_file() and is_allowed(file, allow_dev=True, allow_scripts=True):
                    include_file(file)
            include_file(Path("build_hooks.py"))
            include_file(Path("pyproject.toml"))
        # -------------------------
        # WHEEL (PROD)
        # -------------------------
        elif mode == "release":
            root = Path("nohtyP")
            for file in root.rglob("*"):
                if file.is_file() and is_allowed(file):
                    include_file(file)

    def finalize(self, version: str, build_data: dict, artifact_path: str) -> None:
        """
        Modify name of wheel if dev mode
        """
        mode = os.getenv("_YP_HATCH_BUILD_MODE", "release")
        if not artifact_path.endswith(".whl"):
            return
        base = os.path.splitext(artifact_path)[0]
        filename = os.path.basename(base)
        try:
            name_ver, tags = filename.rsplit("-", 1)
        except ValueError:
            # fallback safety
            return
        if mode == "dev":
            new_filename = f"{name_ver}-dev-{tags}"
        elif mode == "release":
            new_filename = f"{name_ver}-release-{tags}"
        else:
            new_filename = filename
        new_path = os.path.join(os.path.dirname(base), new_filename+".whl")
        os.rename(artifact_path, new_path)
        build_data["artifacts"] = [new_path]
