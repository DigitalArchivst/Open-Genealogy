#!/usr/bin/env python3
"""Validate the extracted GRA runtime skill package."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


REQUIRED_FILES = {
    "SKILL.md",
    "README.md",
    "LICENSE",
    "agents/openai.yaml",
    "references/research-assistant-v8.5-full.md",
    "references/companion-reference.md",
}
FORBIDDEN_PARTS = {"tests", "examples"}
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


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


def validate(skill_root: Path) -> list[str]:
    errors: list[str] = []
    if not skill_root.is_dir():
        return [f"Skill root not found: {skill_root}"]

    files = {
        normalize_rel(path.relative_to(skill_root))
        for path in skill_root.rglob("*")
        if path.is_file()
    }

    missing = sorted(REQUIRED_FILES - files)
    for rel in missing:
        errors.append(f"Missing required file: {rel}")

    for path in skill_root.rglob("*"):
        rel_parts = path.relative_to(skill_root).parts
        bad_parts = FORBIDDEN_PARTS.intersection(rel_parts)
        if bad_parts:
            errors.append(
                "Forbidden runtime path present: "
                + normalize_rel(path.relative_to(skill_root))
            )

    skill_md = skill_root / "SKILL.md"
    if skill_md.is_file():
        text = skill_md.read_text(encoding="utf-8")
        for raw_target in iter_markdown_links(text):
            target = raw_target.split("#", 1)[0].strip()
            if not target or is_external(target):
                continue

            target = unquote(target)
            candidate = (skill_md.parent / target).resolve()
            try:
                candidate.relative_to(skill_root.resolve())
            except ValueError:
                errors.append(f"Link escapes skill root: {raw_target}")
                continue
            if not candidate.exists():
                errors.append(f"Broken SKILL.md link: {raw_target}")

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
    args = parser.parse_args()

    errors = validate(args.skill_root)
    if errors:
        print("GRA runtime package validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("GRA runtime package is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
