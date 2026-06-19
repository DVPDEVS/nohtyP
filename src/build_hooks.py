from hatchling.builders.hooks.plugin.interface import BuildHookInterface
# hatchling 1.30.1+

class RenameWheelHook(BuildHookInterface):
    """
    Custom hook that renames the wheel file based on the target name:
    - wheel       -> nohtyP-<version>-<metadata>.whl
    - wheel-dev   -> nohtyP-<version>-dev.<metadata>.whl
    """

    PLUGIN_NAME = "rename_wheel"

    def initialize(self, version: str, build_data: dict) -> None:
        # We don't need to change build_data here for renaming.
        pass

    def finalize(self, version: str, build_data: dict, artifact_path: str) -> None:
        """
        artifact_path is the full path to the generated wheel file.
        We rename it based on the target name.
        """
        import os
        target_name = self.target_name  # e.g. "wheel" or "wheel-dev"
        if not artifact_path.endswith(".whl"):
            # Not a wheel, skip
            return
        base, ext = os.path.splitext(artifact_path)
        # Extract project name and version from the original filename
        # Original: nohtyP-0.0.1-<tags>.whl
        # We want to keep the same base but insert "dev" for wheel-dev target.
        parts = base.split(os.sep)
        filename = parts[-1]
        # Split into: name-version-tags.whl
        # Example: nohtyP-0.0.1-py3-none-any.whl
        name_ver, tags = filename.rsplit("-", 1)
        # name_ver is "nohtyP-0.0.1"
        if target_name == "wheel-dev":
            # Insert "dev" between version and tags:
            # nohtyP-0.0.1-py3-none-any -> nohtyP-0.0.1-dev-py3-none-any
            new_filename = f"{name_ver}-dev-{tags}"
        else:
            # release or sdist wheel: keep original
            new_filename = filename
        new_path = os.path.join(os.path.dirname(base), new_filename)
        # Rename the file
        os.rename(artifact_path, new_path)
        # Tell Hatchling the new artifact path
        build_data["artifacts"] = [new_path]
