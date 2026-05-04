#!/usr/bin/env python3
"""Build the installable GRA Agent Skill ZIP.

The runtime ZIP intentionally includes only files an agent should load or
inspect during normal use. Developer tests and examples remain in the repo.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import tempfile
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "gra"
RUNTIME_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "agents/openai.yaml",
    "references/research-assistant-v8.5-full.md",
    "references/companion-reference.md",
]


def read_default_version() -> str:
    text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r'^\s*version:\s*"?(?P<version>[^"\n]+)"?', text, re.M)
    if not match:
        raise SystemExit("Could not find metadata.version in skills/gra/SKILL.md")

    version = match.group("version").strip()
    if version.startswith("v"):
        version = version[1:]
    return re.sub(r"c$", "", version)


def build_zip(version: str, output: Path) -> Path:
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    missing = [
        rel for rel in RUNTIME_FILES
        if not (SKILL_ROOT / rel).is_file()
    ]
    if missing:
        raise SystemExit("Missing runtime file(s): " + ", ".join(missing))

    with tempfile.TemporaryDirectory(prefix="gra-skill-") as tmp_name:
        stage_root = Path(tmp_name) / "gra"
        for rel in RUNTIME_FILES:
            src = SKILL_ROOT / rel
            dest = stage_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)

        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(stage_root.rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(stage_root.parent).as_posix())

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
        default=read_default_version(),
        help="Release version without leading v. Defaults to SKILL metadata.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output ZIP path. Defaults to dist/gra-skill-vVERSION.zip.",
    )
    args = parser.parse_args()

    output = args.output or (
        REPO_ROOT / "dist" / f"gra-skill-v{args.version}.zip"
    )
    zip_path = build_zip(args.version, output)

    print(f"Built {zip_path}")
    print(f"Size: {zip_path.stat().st_size} bytes")
    print(f"SHA256: {sha256(zip_path)}")
    print("Included:")
    for rel in RUNTIME_FILES:
        print(f"  gra/{rel}")


if __name__ == "__main__":
    main()
