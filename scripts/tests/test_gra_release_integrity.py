"""Offline tests for the published GRA release-integrity smoke check."""

from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

import check_gra_release_integrity as release_check  # noqa: E402


ZIP_NAME = "gra-skill-v9.2.0.zip"
CHAT_NAME = "research-assistant-v9.2.0-chat.md"
ZIP_DIGEST = "2" * 64
CHAT_DIGEST = "d" * 64


def sample_release() -> dict[str, object]:
    """Return a minimal coherent GitHub release payload."""
    return {
        "tag_name": "v9.2.0",
        "draft": False,
        "body": (
            "## Editions And Checksums\n\n"
            f"- Agent Skill: `{ZIP_NAME}` — 60,068 bytes — "
            f"SHA-256 `{ZIP_DIGEST}`.\n"
            f"- Chat Edition: `{CHAT_NAME}` — 8,016 bytes and 7,968 "
            f"LF-normalized characters — SHA-256 `{CHAT_DIGEST}`.\n"
        ),
        "assets": [
            {
                "name": ZIP_NAME,
                "size": 60068,
                "digest": f"sha256:{ZIP_DIGEST}",
                "browser_download_url": "https://example.invalid/agent.zip",
            },
            {
                "name": CHAT_NAME,
                "size": 8016,
                "digest": f"sha256:{CHAT_DIGEST}",
                "browser_download_url": "https://example.invalid/chat.md",
            },
        ],
    }


class GraReleaseIntegrityTests(unittest.TestCase):
    def test_exact_tag_derives_required_asset_names(self) -> None:
        self.assertEqual(
            (ZIP_NAME, CHAT_NAME),
            release_check.expected_asset_names("v9.2.0"),
        )

    def test_latest_alias_is_not_an_exact_gra_tag(self) -> None:
        with self.assertRaisesRegex(
            release_check.ReleaseIntegrityError, "exact form"
        ):
            release_check.expected_asset_names("latest")

    def test_release_note_records_match_metadata(self) -> None:
        release = sample_release()
        names = release_check.expected_asset_names("v9.2.0")
        notes = release_check.release_note_records(release, names)
        metadata = release_check.metadata_records(release, names)
        release_check.compare_records(notes, metadata)
        self.assertEqual(60068, notes[ZIP_NAME].size)
        self.assertEqual(CHAT_DIGEST, notes[CHAT_NAME].sha256)

    def test_release_note_digest_mismatch_is_rejected(self) -> None:
        release = sample_release()
        release["body"] = str(release["body"]).replace(
            ZIP_DIGEST, "3" * 64
        )
        names = release_check.expected_asset_names("v9.2.0")
        notes = release_check.release_note_records(release, names)
        metadata = release_check.metadata_records(release, names)
        with self.assertRaisesRegex(
            release_check.ReleaseIntegrityError,
            "release notes SHA-256",
        ):
            release_check.compare_records(notes, metadata)

    def test_missing_expected_asset_is_rejected(self) -> None:
        release = sample_release()
        release["assets"] = list(release["assets"])[1:]
        with self.assertRaisesRegex(
            release_check.ReleaseIntegrityError,
            "Required release asset is missing",
        ):
            release_check.metadata_records(release, (ZIP_NAME, CHAT_NAME))

    def test_public_latest_release_reference_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text(
                "Download from https://github.com/example/repo/releases/latest\n",
                encoding="utf-8",
            )
            findings = release_check.public_latest_release_references(root)
            self.assertEqual(["README.md:1"], findings)
            with self.assertRaisesRegex(
                release_check.ReleaseIntegrityError,
                "must not use /releases/latest",
            ):
                release_check.assert_no_public_latest_release_references(root)

    def test_exact_release_link_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text(
                "Download from https://github.com/example/repo/releases/tag/v9.2.0\n",
                encoding="utf-8",
            )
            release_check.assert_no_public_latest_release_references(root)

    def test_zip_path_traversal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            archive_path = root / "unsafe.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("../outside.txt", "unsafe")
            with self.assertRaisesRegex(
                release_check.ReleaseIntegrityError,
                "Unsafe path",
            ):
                release_check.safely_extract_zip(archive_path, root / "stage")


if __name__ == "__main__":
    unittest.main()
