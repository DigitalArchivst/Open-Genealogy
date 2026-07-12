#!/usr/bin/env python3
"""Smoke-test a published GRA release without mutating its assets.

The check deliberately resolves one exact version tag. It compares the two
expected GRA assets with GitHub's release metadata and with the integrity text
printed in the release notes, downloads and hashes both assets, validates the
Agent Skill package, and rejects public documentation that routes readers
through the repository-wide ``/releases/latest`` alias.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from validate_gra_skill_zip import validate as validate_skill


DEFAULT_REPOSITORY = "DigitalArchivst/Open-Genealogy"
PUBLIC_TEXT_SUFFIXES = {".htm", ".html", ".markdown", ".md", ".txt"}
IGNORED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "dist",
    "node_modules",
    "__pycache__",
}
LATEST_RELEASE_TOKEN = "/releases/latest"
TAG_RE = re.compile(r"^v(?P<version>\d+\.\d+\.\d+)$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ReleaseIntegrityError(RuntimeError):
    """A published release failed an integrity requirement."""


@dataclass(frozen=True)
class IntegrityRecord:
    """Expected asset identity recorded in the public release notes."""

    name: str
    size: int
    sha256: str


def version_from_tag(tag: str) -> str:
    """Return the X.Y.Z token from an exact GRA release tag."""
    match = TAG_RE.fullmatch(tag)
    if not match:
        raise ReleaseIntegrityError(
            f"GRA release tag must have exact form vX.Y.Z, got {tag!r}"
        )
    return match.group("version")


def expected_asset_names(tag: str) -> tuple[str, str]:
    """Derive the required Agent and Chat asset names from the exact tag."""
    version = version_from_tag(tag)
    return (
        f"gra-skill-v{version}.zip",
        f"research-assistant-v{version}-chat.md",
    )


def request_headers() -> dict[str, str]:
    """Build GitHub headers, using the workflow token when available."""
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "Open-Genealogy-GRA-release-integrity",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_json(url: str) -> dict[str, Any]:
    """Fetch one JSON object from GitHub."""
    request = Request(url, headers=request_headers())
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError) as error:
        raise ReleaseIntegrityError(f"GitHub request failed: {url}: {error}") from error
    if not isinstance(payload, dict):
        raise ReleaseIntegrityError(f"GitHub returned a non-object payload: {url}")
    return payload


def fetch_release(repository: str, tag: str) -> dict[str, Any]:
    """Resolve a release only by its exact tag, never by a latest alias."""
    if repository.count("/") != 1:
        raise ReleaseIntegrityError(
            f"Repository must have owner/name form, got {repository!r}"
        )
    endpoint = (
        "https://api.github.com/repos/"
        f"{repository}/releases/tags/{quote(tag, safe='')}"
    )
    release = fetch_json(endpoint)
    if release.get("tag_name") != tag:
        raise ReleaseIntegrityError(
            f"GitHub resolved tag {release.get('tag_name')!r}, expected {tag!r}"
        )
    if release.get("draft"):
        raise ReleaseIntegrityError(f"Release {tag} is still a draft")
    return release


def parse_integrity_record(body: str, asset_name: str) -> IntegrityRecord:
    """Parse one asset's bytes and full SHA-256 from release-note prose."""
    pattern = re.compile(
        rf"(?im)^[^\n]*{re.escape(asset_name)}[^\n]*?"
        rf"(?P<size>\d[\d,]*)\s+bytes[^\n]*?"
        rf"SHA-256\s+`?(?P<digest>[0-9a-f]{{64}})`?[^\n]*$"
    )
    matches = list(pattern.finditer(body))
    if len(matches) != 1:
        raise ReleaseIntegrityError(
            f"Release notes must contain exactly one integrity record for "
            f"{asset_name}; found {len(matches)}"
        )
    match = matches[0]
    return IntegrityRecord(
        name=asset_name,
        size=int(match.group("size").replace(",", "")),
        sha256=match.group("digest").lower(),
    )


def release_note_records(
    release: dict[str, Any], asset_names: Iterable[str]
) -> dict[str, IntegrityRecord]:
    """Read all required integrity records from the release description."""
    body = release.get("body")
    if not isinstance(body, str):
        raise ReleaseIntegrityError("Release notes body is missing")
    return {name: parse_integrity_record(body, name) for name in asset_names}


def metadata_records(
    release: dict[str, Any], asset_names: Iterable[str]
) -> dict[str, IntegrityRecord]:
    """Read required names, sizes, and GitHub SHA-256 metadata."""
    assets = release.get("assets")
    if not isinstance(assets, list):
        raise ReleaseIntegrityError("GitHub release asset list is missing")
    by_name = {
        asset.get("name"): asset
        for asset in assets
        if isinstance(asset, dict) and isinstance(asset.get("name"), str)
    }
    records: dict[str, IntegrityRecord] = {}
    for name in asset_names:
        asset = by_name.get(name)
        if asset is None:
            raise ReleaseIntegrityError(f"Required release asset is missing: {name}")
        size = asset.get("size")
        digest = asset.get("digest")
        if not isinstance(size, int):
            raise ReleaseIntegrityError(f"GitHub size is missing for {name}")
        if not isinstance(digest, str) or not digest.lower().startswith("sha256:"):
            raise ReleaseIntegrityError(f"GitHub SHA-256 digest is missing for {name}")
        sha256 = digest.split(":", 1)[1].lower()
        if not SHA256_RE.fullmatch(sha256):
            raise ReleaseIntegrityError(f"GitHub digest is malformed for {name}: {digest}")
        records[name] = IntegrityRecord(name=name, size=size, sha256=sha256)
    return records


def compare_records(
    notes: dict[str, IntegrityRecord], metadata: dict[str, IntegrityRecord]
) -> None:
    """Require release-note integrity text to match GitHub metadata."""
    errors: list[str] = []
    for name, expected in notes.items():
        actual = metadata[name]
        if expected.size != actual.size:
            errors.append(
                f"{name}: release notes say {expected.size} bytes; "
                f"GitHub metadata says {actual.size}"
            )
        if expected.sha256 != actual.sha256:
            errors.append(
                f"{name}: release notes SHA-256 {expected.sha256}; "
                f"GitHub metadata SHA-256 {actual.sha256}"
            )
    if errors:
        raise ReleaseIntegrityError("\n".join(errors))


def public_latest_release_references(root: Path) -> list[str]:
    """Return public text locations containing the repository-wide alias."""
    findings: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in PUBLIC_TEXT_SUFFIXES:
            continue
        if any(part in IGNORED_DIRECTORIES for part in path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if LATEST_RELEASE_TOKEN in line.lower():
                findings.append(f"{path.relative_to(root).as_posix()}:{line_number}")
    return findings


def assert_no_public_latest_release_references(root: Path) -> None:
    """Reject public instructions that can route to another product family."""
    findings = public_latest_release_references(root)
    if findings:
        raise ReleaseIntegrityError(
            "Public documentation must not use /releases/latest:\n- "
            + "\n- ".join(findings)
        )


def download_asset(url: str, destination: Path) -> None:
    """Download one immutable release asset to a temporary path."""
    request = Request(url, headers=request_headers())
    try:
        with urlopen(request, timeout=60) as response, destination.open("wb") as handle:
            while chunk := response.read(1024 * 1024):
                handle.write(chunk)
    except (HTTPError, URLError, TimeoutError) as error:
        raise ReleaseIntegrityError(f"Asset download failed: {url}: {error}") from error


def sha256_file(path: Path) -> str:
    """Return a lower-case SHA-256 digest for a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assert_download_matches(path: Path, expected: IntegrityRecord) -> None:
    """Compare downloaded bytes with the public integrity record."""
    size = path.stat().st_size
    digest = sha256_file(path)
    if size != expected.size or digest != expected.sha256:
        raise ReleaseIntegrityError(
            f"Downloaded {expected.name} does not match GitHub metadata: "
            f"size={size}, SHA-256={digest}; expected size={expected.size}, "
            f"SHA-256={expected.sha256}"
        )


def safely_extract_zip(archive_path: Path, destination: Path) -> None:
    """Extract a ZIP after rejecting traversal and symbolic-link entries."""
    destination = destination.resolve()
    with zipfile.ZipFile(archive_path) as archive:
        for info in archive.infolist():
            relative = PurePosixPath(info.filename)
            if relative.is_absolute() or ".." in relative.parts:
                raise ReleaseIntegrityError(
                    f"Unsafe path in Agent Skill ZIP: {info.filename}"
                )
            unix_mode = info.external_attr >> 16
            if stat.S_ISLNK(unix_mode):
                raise ReleaseIntegrityError(
                    f"Symbolic link in Agent Skill ZIP: {info.filename}"
                )
            target = (destination / Path(*relative.parts)).resolve()
            try:
                target.relative_to(destination)
            except ValueError as error:
                raise ReleaseIntegrityError(
                    f"Unsafe extraction target in Agent Skill ZIP: {info.filename}"
                ) from error
        archive.extractall(destination)


def validate_agent_zip(archive_path: Path, version: str, stage: Path) -> None:
    """Extract and run the repository's exact runtime-package validator."""
    safely_extract_zip(archive_path, stage)
    errors = validate_skill(stage / "gra", expected_version=version)
    if errors:
        raise ReleaseIntegrityError(
            "Downloaded Agent Skill ZIP failed runtime validation:\n- "
            + "\n- ".join(errors)
        )


def asset_download_urls(
    release: dict[str, Any], asset_names: Iterable[str]
) -> dict[str, str]:
    """Return browser download URLs for required assets."""
    assets = release.get("assets", [])
    by_name = {
        asset.get("name"): asset
        for asset in assets
        if isinstance(asset, dict)
    }
    urls: dict[str, str] = {}
    for name in asset_names:
        url = by_name[name].get("browser_download_url")
        if not isinstance(url, str) or not url.startswith("https://"):
            raise ReleaseIntegrityError(f"Download URL is missing for {name}")
        urls[name] = url
    return urls


def run_check(repository: str, tag: str, source_root: Path) -> None:
    """Run the complete read-only release-integrity smoke test."""
    version = version_from_tag(tag)
    asset_names = expected_asset_names(tag)
    assert_no_public_latest_release_references(source_root)

    release = fetch_release(repository, tag)
    notes = release_note_records(release, asset_names)
    metadata = metadata_records(release, asset_names)
    compare_records(notes, metadata)
    urls = asset_download_urls(release, asset_names)

    with tempfile.TemporaryDirectory(prefix=f"gra-release-{tag}-") as temp_dir:
        temp_root = Path(temp_dir)
        downloaded: dict[str, Path] = {}
        for name in asset_names:
            path = temp_root / name
            download_asset(urls[name], path)
            assert_download_matches(path, metadata[name])
            downloaded[name] = path
        validate_agent_zip(
            downloaded[asset_names[0]], version, temp_root / "extracted"
        )

    print(f"GRA release integrity check passed: {repository} {tag}")
    for name in asset_names:
        record = metadata[name]
        print(f"- {name}: {record.size} bytes; SHA-256 {record.sha256}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify an exact published GRA release and its public links."
    )
    parser.add_argument(
        "--repository",
        default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPOSITORY),
        help="GitHub owner/name (default: current workflow repository).",
    )
    parser.add_argument(
        "--tag",
        required=True,
        help="Exact GRA release tag in vX.Y.Z form; latest aliases are forbidden.",
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root whose public documentation should be scanned.",
    )
    args = parser.parse_args()

    try:
        run_check(args.repository, args.tag, args.source_root.resolve())
    except ReleaseIntegrityError as error:
        print(f"GRA release integrity check failed:\n{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
