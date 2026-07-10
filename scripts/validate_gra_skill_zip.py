#!/usr/bin/env python3
"""Validate the extracted GRA runtime skill package."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional
from urllib.parse import unquote


EXPECTED_FILES = {
    "SKILL.md",
    "README.md",
    "LICENSE",
    "agents/openai.yaml",
    "references/research-assistant-full.md",
    "references/companion-reference.md",
}
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SKILL_VERSION_RE = re.compile(
    r'^\s*version:\s*"?v?(?P<version>\d+\.\d+\.\d+)', re.M
)
VERSION_SURFACES = {
    "SKILL.md heading": (
        "SKILL.md",
        re.compile(
            r"^# Genealogical Research Assistant "
            r"v(?P<version>\d+\.\d+\.\d+) Skill Edition$",
            re.M,
        ),
    ),
    "README.md release declaration": (
        "README.md",
        re.compile(
            r"^v(?P<version>\d+\.\d+\.\d+) is the current release\b",
            re.M,
        ),
    ),
    "agents/openai.yaml heading": (
        "agents/openai.yaml",
        re.compile(
            r"^# GRA v(?P<version>\d+\.\d+\.\d+) Skill Edition$",
            re.M,
        ),
    ),
    "full reference heading": (
        "references/research-assistant-full.md",
        re.compile(
            r"^# Genealogical Research Assistant "
            r"v(?P<version>\d+\.\d+\.\d+) Skill Edition$",
            re.M,
        ),
    ),
    "companion reference heading": (
        "references/companion-reference.md",
        re.compile(
            r"^# GRA v(?P<version>\d+\.\d+\.\d+) Skill Edition "
            r".+$",
            re.M,
        ),
    ),
}


def normalize_rel(path: Path) -> str:
    return path.as_posix()


def iter_markdown_links(text: str) -> list[str]:
    links: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        links.extend(match.group(1).strip() for match in MARKDOWN_LINK_RE.finditer(line))
    return links


def is_external(target: str) -> bool:
    lower = target.lower()
    return (
        lower.startswith("http://")
        or lower.startswith("https://")
        or lower.startswith("mailto:")
        or lower.startswith("#")
    )


def read_skill_version(skill_root: Path) -> str:
    """Derive the X.Y.Z release token from SKILL.md metadata.version."""
    skill_md = skill_root / "SKILL.md"
    if not skill_md.is_file():
        raise ValueError("SKILL.md is missing")
    text = skill_md.read_text(encoding="utf-8")
    match = SKILL_VERSION_RE.search(text)
    if not match:
        raise ValueError("SKILL.md metadata.version is missing or invalid")
    return match.group("version")


def validate_versions(
    skill_root: Path, expected_version: Optional[str] = None
) -> list[str]:
    """Check every runtime version surface against SKILL.md metadata."""
    try:
        metadata_version = read_skill_version(skill_root)
    except ValueError as error:
        return [str(error)]

    errors = []
    if expected_version is not None and expected_version != metadata_version:
        errors.append(
            f"Requested version {expected_version} does not match "
            f"SKILL.md metadata version {metadata_version}"
        )

    for label, (relative, pattern) in VERSION_SURFACES.items():
        path = skill_root / relative
        if not path.is_file():
            continue
        match = pattern.search(path.read_text(encoding="utf-8"))
        if not match:
            errors.append(f"Version declaration missing: {label}")
        elif match.group("version") != metadata_version:
            errors.append(
                f"Version mismatch in {label}: {match.group('version')} "
                f"!= {metadata_version}"
            )
    return errors


def validate(
    skill_root: Path, expected_version: Optional[str] = None
) -> list[str]:
    errors: list[str] = []
    if not skill_root.is_dir():
        return [f"Skill root not found: {skill_root}"]

    files = {
        normalize_rel(path.relative_to(skill_root))
        for path in skill_root.rglob("*")
        if path.is_file()
    }

    missing = sorted(EXPECTED_FILES - files)
    for rel in missing:
        errors.append(f"Missing required file: {rel}")

    unexpected = sorted(files - EXPECTED_FILES)
    for rel in unexpected:
        errors.append(f"Unexpected runtime file: {rel}")

    for markdown_path in skill_root.rglob("*.md"):
        text = markdown_path.read_text(encoding="utf-8")
        for raw_target in iter_markdown_links(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or is_external(target):
                continue

            target = unquote(target)
            candidate = (markdown_path.parent / target).resolve()
            try:
                candidate.relative_to(skill_root.resolve())
            except ValueError:
                errors.append(
                    f"Link escapes skill root in {markdown_path.name}: "
                    f"{raw_target}"
                )
                continue
            if not candidate.exists():
                errors.append(
                    f"Broken link in {markdown_path.name}: {raw_target}"
                )

    skill_md = skill_root / "SKILL.md"
    if skill_md.is_file():
        text = skill_md.read_text(encoding="utf-8")

        # v9 checks: edition markers must be intact (the chat edition is
        # generated from this file), and the version display form must be
        # present in frontmatter and H1 (release-gate 7 sweep surface).
        for marker in ("<!-- v9:body:start -->", "<!-- v9:body:end -->"):
            if marker not in text:
                errors.append(f"Missing v9 edition marker: {marker}")
        starts = len(re.findall(r"<!-- v9:(?:agent-only|chat-swap:[a-z0-9-]+):start -->", text))
        ends = len(re.findall(r"<!-- v9:(?:agent-only|chat-swap:[a-z0-9-]+):end -->", text))
        if starts != ends:
            errors.append(
                f"Unbalanced v9 edition markers: {starts} start vs {ends} end"
            )
    errors.extend(validate_versions(skill_root, expected_version))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an extracted GRA runtime skill package."
    )
    parser.add_argument(
        "skill_root",
        type=Path,
        help="Path to the extracted gra/ skill directory.",
    )
    parser.add_argument(
        "--version",
        help="Expected X.Y.Z version; must match SKILL.md metadata.",
    )
    args = parser.parse_args()

    errors = validate(args.skill_root, expected_version=args.version)
    if errors:
        print("GRA runtime package validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GRA runtime package is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
