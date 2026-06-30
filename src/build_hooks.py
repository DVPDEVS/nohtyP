from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from hashlib import sha256
import base64
import csv
import io
from hatchling.metadata.plugin.interface import MetadataHookInterface
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import os

class ContentHook(BuildHookInterface):
    """
    Custom hook that renames the wheel file based on the target mode:
    - `wheel     -> nohtyP-<version>-<tags>.whl`
    - `dev       -> nohtyP-<version>-dev-<tags>.whl`  \n
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
        build_data["dev_optional_dependencies"] = (self.metadata.config.get("project", {}).get("optional-dependencies", {}).get("dev", []))
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
            if "_dev" in path.parts and not allow_dev:
                return False
            # script rule, should only appear in sdist
            if "scripts" in path.parts and not allow_scripts:
                return False
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

    def finalize(self, version, build_data, artifact_path):
        """
        Modify METADATA
        """
        mode: str = os.getenv("_YP_HATCH_BUILD_MODE", "release")
        dev_deps = build_data.get("dev_optional_dependencies", [])
        if (mode == "dev" and not dev_deps) or mode not in ["dev", "release"]:
            return
        wheel_path = Path(artifact_path)
        tmp_path = wheel_path.with_suffix(".tmp.whl")
        with ZipFile(wheel_path, "r") as zin, ZipFile(tmp_path, "w", compression=ZIP_DEFLATED) as zout:
            names = zin.namelist()
            dist_info = next(n for n in names if n.endswith(".dist-info/METADATA")).rsplit("/", 1)[0]
            metadata_name = f"{dist_info}/METADATA"
            record_name = f"{dist_info}/RECORD"
            metadata = zin.read(metadata_name).decode("utf-8")
            # Remove dev optional dependencies
            metadata_lines = []
            inserted = False
            for line in metadata.splitlines():
                if not inserted and mode == "dev" and line == "":
                    existing = set(metadata_lines)
                    for dep in dev_deps:
                        req = f"Requires-Dist: {dep}"
                        if req not in existing:
                            metadata_lines.append(req)
                            existing.add(req)
                    inserted = True
                if (line.startswith("Requires-Dist:") and ("extra == 'dev'" in line or 'extra == "dev"' in line)) or line == "Provides-Extra: dev":
                    continue
                metadata_lines.append(line)
            metadata = "\n".join(metadata_lines) + "\n"
            # Rewrite wheel, skipping old RECORD
            for name in names:
                if name == metadata_name:
                    data = metadata.encode("utf-8")
                elif name == record_name:
                    continue
                else:
                    data = zin.read(name)
                zout.writestr(name, data)
            # Recreate RECORD
            rows = []
            for name in zout.namelist():
                if name == record_name:
                    continue
                data = zout.read(name)
                digest = base64.urlsafe_b64encode(sha256(data).digest()).rstrip(b"=").decode("ascii")
                rows.append([name, f"sha256={digest}", str(len(data))])
            rows.append([record_name, "", ""])
            buf = io.StringIO()
            writer = csv.writer(buf, lineterminator="\n")
            writer.writerows(rows)
            zout.writestr(record_name, buf.getvalue().encode("utf-8"))
        tmp_path.replace(wheel_path)
