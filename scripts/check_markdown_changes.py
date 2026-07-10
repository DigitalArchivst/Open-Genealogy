#!/usr/bin/env python3
"""Lint every changed Markdown file except explicit runtime exemptions."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Optional


REPO = Path(__file__).resolve().parent.parent
IGNORE_FILE = REPO / ".markdownlintignore"
MARKDOWN_SUFFIXES = {".md", ".markdown"}
APPROVED_BOOTSTRAP_EXEMPTIONS = {
    "assistants/gedcom-builder-v1.md",
    "assistants/gedcom-creator-mini.md",
    "hebrew-headstones/hebrew-headstone-helper-v9.md",
    "photo-restoration/damage-removal-v3.md",
    "photo-restoration/photo-conservator-v2.md",
    "photo-restoration/photo-reconstructor-v3.md",
    "photo-restoration/restoration-v2.md",
    "research/archive/research-with-citations-v2.md",
    "research/contract-first-genealogy-v3.1.md",
    "research/research-assistant-v6.1.md",
    "research/research-assistant-v7.md",
    "transcription/jewish-transcription-v2.md",
    "writing-tools/fact-narrator-v4.md",
}


class MarkdownGateError(RuntimeError):
    """Raised when the changed-file lint gate cannot run completely."""


def _git_z(repo: Path, *args: str) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), "-c", "core.quotepath=false", *args],
        capture_output=True,
        check=True,
    )
    return [
        item.decode("utf-8")
        for item in result.stdout.split(b"\0")
        if item
    ]


def _git_text(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def discover_base(repo: Path, explicit: Optional[str] = None) -> str:
    """Find a comparison base that includes committed branch changes."""
    candidates = []
    if explicit:
        candidates.append(explicit)
    elif os.environ.get("MARKDOWNLINT_BASE"):
        candidates.append(os.environ["MARKDOWNLINT_BASE"])
    elif os.environ.get("GITHUB_BASE_REF"):
        candidates.append(f"origin/{os.environ['GITHUB_BASE_REF']}")
    else:
        candidates.extend(("origin/main", "main", "origin/master", "master"))

    for candidate in candidates:
        try:
            return _git_text(repo, "merge-base", "HEAD", candidate)
        except subprocess.CalledProcessError:
            continue

    tried = ", ".join(candidates) or "no candidate refs"
    raise MarkdownGateError(
        f"could not determine a comparison base from {tried}; "
        "pass --base REF"
    )


def changed_paths(repo: Path, base: str) -> set[str]:
    """Collect committed, staged, unstaged, and untracked changed paths."""
    paths = set()
    paths.update(
        _git_z(
            repo,
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            "-z",
            f"{base}..HEAD",
        )
    )
    paths.update(
        _git_z(
            repo,
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            "-z",
        )
    )
    paths.update(
        _git_z(
            repo,
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=ACMR",
            "-z",
        )
    )
    paths.update(
        _git_z(repo, "ls-files", "--others", "--exclude-standard", "-z")
    )
    return {
        path.replace("\\", "/")
        for path in paths
        if (repo / path).is_file()
    }


def load_explicit_exemptions(path: Path = IGNORE_FILE) -> set[str]:
    """Load exact ignored Markdown paths; wildcard ignores are not allowed."""
    exemptions = set()
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        normalized = line.removeprefix("./").replace("\\", "/")
        if any(character in normalized for character in "*?[]!"):
            raise MarkdownGateError(
                f"{path.name}:{line_number} is not an explicit path: {line}"
            )
        exemptions.add(normalized)
    return exemptions


def load_base_explicit_exemptions(repo: Path, base: str) -> set[str]:
    """Read exemptions that already existed at the comparison base."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "show", f"{base}:{IGNORE_FILE.name}"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        return set()

    exemptions = set()
    for line_number, raw_line in enumerate(result.stdout.splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        normalized = line.removeprefix("./").replace("\\", "/")
        if any(character in normalized for character in "*?[]!"):
            raise MarkdownGateError(
                f"base .markdownlintignore:{line_number} is not an explicit path: {line}"
            )
        exemptions.add(normalized)
    return exemptions


def validate_no_new_exemptions(
    exemptions: set[str], base_exemptions: set[str]
) -> None:
    unapproved = exemptions - (
        base_exemptions | APPROVED_BOOTSTRAP_EXEMPTIONS
    )
    if unapproved:
        raise MarkdownGateError(
            "unapproved Markdown exemptions are not permitted: "
            + ", ".join(sorted(unapproved))
        )


def select_markdown_files(
    paths: Iterable[str], exemptions: set[str]
) -> tuple[list[str], list[str]]:
    """Partition changed Markdown into linted and explicitly exempt paths."""
    markdown = sorted(
        {
            path.replace("\\", "/")
            for path in paths
            if Path(path).suffix.lower() in MARKDOWN_SUFFIXES
        }
    )
    exempt = [path for path in markdown if path in exemptions]
    lint = [path for path in markdown if path not in exemptions]
    return lint, exempt


def _chunks(paths: list[str], limit: int = 7000) -> Iterable[list[str]]:
    """Keep linter commands below conservative Windows command limits."""
    chunk = []
    size = 0
    for path in paths:
        path_size = len(path) + 3
        if chunk and size + path_size > limit:
            yield chunk
            chunk = []
            size = 0
        chunk.append(path)
        size += path_size
    if chunk:
        yield chunk


def run_markdownlint(repo: Path, paths: list[str]) -> int:
    """Run the pinned local markdownlint-cli against every selected path."""
    node = shutil.which("node")
    cli = repo / "node_modules" / "markdownlint-cli" / "markdownlint.js"
    if not node or not cli.is_file():
        raise MarkdownGateError(
            "pinned markdownlint-cli is unavailable; run npm ci first"
        )

    status = 0
    for chunk in _chunks(paths):
        result = subprocess.run([node, str(cli), *chunk], cwd=repo)
        if result.returncode:
            status = result.returncode
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        help=(
            "Git comparison ref. Defaults to MARKDOWNLINT_BASE, the GitHub "
            "base branch, origin/main, or main."
        ),
    )
    args = parser.parse_args()

    try:
        base = discover_base(REPO, args.base)
        paths = changed_paths(REPO, base)
        exemptions = load_explicit_exemptions()
        base_exemptions = load_base_explicit_exemptions(REPO, base)
        validate_no_new_exemptions(exemptions, base_exemptions)
        lint, exempt = select_markdown_files(paths, exemptions)
        print(f"Markdown comparison base: {base}")
        for path in exempt:
            print(f"EXEMPT runtime Markdown: {path}")
        if not lint:
            print("No non-exempt changed Markdown files to lint.")
            return 0
        print(f"Linting {len(lint)} changed Markdown file(s).")
        return run_markdownlint(REPO, lint)
    except (MarkdownGateError, subprocess.CalledProcessError) as error:
        print(f"Markdown changed-file gate failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
