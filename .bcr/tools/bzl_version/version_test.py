"""A suite of tests ensuring version strings are all in sync."""

import platform
import re
import unittest
from pathlib import Path

from python.runfiles import Runfiles

PKG_NAME = "rules_verilog"


def rlocation(runfiles: Runfiles, rlocationpath: str) -> Path:
    """Look up a runfile and ensure the file exists

    Args:
        runfiles: The runfiles object
        rlocationpath: The runfile key

    Returns:
        The requested runifle.
    """
    # TODO: https://github.com/periareon/rules_venv/issues/37
    source_repo = None
    if platform.system() == "Windows":
        source_repo = ""
    runfile = runfiles.Rlocation(rlocationpath, source_repo)
    if not runfile:
        raise FileNotFoundError(f"Failed to find runfile: {rlocationpath}")
    path = Path(runfile)
    if not path.exists():
        raise FileNotFoundError(f"Runfile does not exist: ({rlocationpath}) {path}")
    return path


class RepoVersionTests(unittest.TestCase):
    """Test that the `{PKG_NAME}` versions match for WORKSPACE and bzlmod."""

    def test_versions(self) -> None:
        """Test that the version.bzl and MOUDLE.bazel versions are synced."""
        runfiles = Runfiles.Create()
        if not runfiles:
            raise EnvironmentError("Failed to locate runfiles.")

        version_bzl = rlocation(runfiles, f"{PKG_NAME}/version.bzl")
        bzl_version = re.findall(
            r'VERSION = "([\w\d\.]+)"',
            version_bzl.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        assert bzl_version, f"Failed to parse version from {version_bzl}"
        assert len(bzl_version) == 1, (
            f"Expect len(bzl_version)=1, but got {len(bzl_version)}"
        )

        bzl_version = bzl_version[0]

        module_bazel = rlocation(runfiles, f"{PKG_NAME}/MODULE.bazel")
        module_versions = re.findall(
            rf'module\(\n\s+name = "{re.escape(PKG_NAME)}",\n\s+version = "([\d\w\.]+)",\n',
            module_bazel.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        assert module_versions, f"Failed to parse version from {module_bazel}"

        readme_bazel = rlocation(runfiles, f"{PKG_NAME}/README.md")
        readme_versions = re.findall(
            rf'bazel_dep\(\s*name\s*=\s*"{re.escape(PKG_NAME)}",\s*version\s*=\s*"([\d\w\.]+)"\s*\)',
            readme_bazel.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        # allow readme_versions is empty

        assert all(e == bzl_version for e in module_versions), (
            "Version in MODULE.bazel do not match"
        )

        assert all(e == bzl_version for e in readme_versions), (
            "Version in README.md do not match"
        )


if __name__ == "__main__":
    unittest.main()
