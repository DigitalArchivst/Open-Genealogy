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
    "references/research-assistant-full.md",
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
        if "v9.0.0 Skill Edition" not in text:
            errors.append("Version display form 'v9.0.0 Skill Edition' not found in SKILL.md")

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
