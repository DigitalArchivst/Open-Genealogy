#!/usr/bin/env python3
"""Build the installable GRA Agent Skill ZIP.

The runtime ZIP intentionally includes only files an agent should load or
inspect during normal use. Developer tests and examples remain in the repo.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import stat
import tempfile
import zipfile
from pathlib import Path

from validate_gra_skill_zip import validate


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "gra"
RUNTIME_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "agents/openai.yaml",
    "references/research-assistant-full.md",
    "references/companion-reference.md",
]
TEXT_RUNTIME_FILES = frozenset(RUNTIME_FILES)

# Canonical ZIP metadata for byte-reproducible future release artifacts.
# The immutable v9.2.0 tag retains the packager used for the published v9.2.0
# assets; changes on main apply to packages built after that release.
ZIP_DATE_TIME = (1980, 1, 1, 0, 0, 0)
ZIP_CREATE_SYSTEM = 3  # Unix, independent of the build host.
ZIP_FILE_MODE = stat.S_IFREG | 0o644
ZIP_COMPRESSION = zipfile.ZIP_DEFLATED
ZIP_COMPRESSLEVEL = 9


def canonical_runtime_bytes(relative_path: str) -> bytes:
    """Read one runtime file with canonical UTF-8/LF text bytes."""
    path = SKILL_ROOT / relative_path
    data = path.read_bytes()
    if relative_path not in TEXT_RUNTIME_FILES:
        return data

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SystemExit(
            f"Runtime text file is not valid UTF-8: {relative_path}"
        ) from exc
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def canonical_zip_info(archive_name: str) -> zipfile.ZipInfo:
    """Return fixed, host-independent metadata for one ZIP file entry."""
    info = zipfile.ZipInfo(archive_name, date_time=ZIP_DATE_TIME)
    info.create_system = ZIP_CREATE_SYSTEM
    info.external_attr = ZIP_FILE_MODE << 16
    info.compress_type = ZIP_COMPRESSION
    return info


def read_default_version() -> str:
    """Extract the machine version token (X.Y.Z) from metadata.version.

    Since v9, metadata.version carries the display form (e.g.
    "v9.2.0 Skill Edition"); the ZIP name uses the machine token per the
    PRD's version discipline. Pre-v9 forms ("8.5.3c") are still handled.
    """
    text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r'^\s*version:\s*"?(?P<version>[^"\n]+)"?', text, re.M)
    if not match:
        raise SystemExit("Could not find metadata.version in skills/gra/SKILL.md")

    display = match.group("version").strip()
    token = re.search(r"v?(\d+(?:\.\d+)*)", display)
    if not token:
        raise SystemExit(f"Could not parse a version token from: {display}")
    return token.group(1)


def require_matching_version(version: str) -> str:
    """Require an explicit package version to match SKILL.md metadata."""
    metadata_version = read_default_version()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise SystemExit(
            f"Invalid --version {version!r}; expected X.Y.Z "
            f"matching {metadata_version}"
        )
    if version != metadata_version:
        raise SystemExit(
            f"Mismatched --version {version}; SKILL.md metadata "
            f"declares {metadata_version}"
        )
    return version


def build_zip(version: str, output: Path) -> Path:
    version = require_matching_version(version)
    output = output.resolve()
    expected_name = f"gra-skill-v{version}.zip"
    if output.name != expected_name:
        raise SystemExit(
            f"Package filename {output.name!r} must be {expected_name!r}"
        )

    missing = [
        rel for rel in RUNTIME_FILES
        if not (SKILL_ROOT / rel).is_file()
    ]
    if missing:
        raise SystemExit("Missing runtime file(s): " + ", ".join(missing))

    with tempfile.TemporaryDirectory(prefix="gra-skill-") as tmp_name:
        stage_root = Path(tmp_name) / "gra"
        for rel in RUNTIME_FILES:
            dest = stage_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(canonical_runtime_bytes(rel))

        validation_errors = validate(
            stage_root, expected_version=version
        )
        if validation_errors:
            raise SystemExit(
                "Runtime package validation failed:\n- "
                + "\n- ".join(validation_errors)
            )

        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, "w") as zf:
            for rel in sorted(RUNTIME_FILES):
                archive_name = (Path("gra") / rel).as_posix()
                zf.writestr(
                    canonical_zip_info(archive_name),
                    (stage_root / rel).read_bytes(),
                    compress_type=ZIP_COMPRESSION,
                    compresslevel=ZIP_COMPRESSLEVEL,
                )

    return output


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Package the GRA skill runtime ZIP."
    )
    parser.add_argument(
        "--version",
        default=None,
        help="Release version without leading v. Defaults to SKILL metadata.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output ZIP path. Defaults to dist/gra-skill-vVERSION.zip.",
    )
    args = parser.parse_args()
    version = require_matching_version(
        args.version or read_default_version()
    )

    output = args.output or (
        REPO_ROOT / "dist" / f"gra-skill-v{version}.zip"
    )
    zip_path = build_zip(version, output)

    print(f"Built {zip_path}")
    print(f"Size: {zip_path.stat().st_size} bytes")
    print(f"SHA256: {sha256(zip_path)}")
    print("Included:")
    for rel in RUNTIME_FILES:
        print(f"  gra/{rel}")


if __name__ == "__main__":
    main()
