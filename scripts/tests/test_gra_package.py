"""Offline tests for the exact GRA runtime package contract."""

from __future__ import annotations

import os
import shutil
import stat
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1]
REPO = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

import package_gra_skill as package  # noqa: E402
import validate_gra_skill_zip as validator  # noqa: E402


class GraPackageTests(unittest.TestCase):
    def stage_runtime(self, root: Path) -> Path:
        stage = root / "gra"
        for relative in package.RUNTIME_FILES:
            source = package.SKILL_ROOT / relative
            destination = stage / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        return stage

    def stage_packaging_source(
        self,
        root: Path,
        *,
        crlf: bool,
        mtime: int,
    ) -> Path:
        """Copy canonical runtime content with controlled line endings/mtime."""
        source_root = root / "source"
        for relative in package.RUNTIME_FILES:
            data = package.canonical_runtime_bytes(relative)
            if crlf:
                data = data.replace(b"\n", b"\r\n")
            destination = source_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            os.utime(destination, (mtime, mtime))
        return source_root

    def test_exact_runtime_manifest_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            stage = self.stage_runtime(Path(temp_dir))
            self.assertEqual([], validator.validate(stage, "9.2.0"))

    def test_extra_runtime_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            stage = self.stage_runtime(Path(temp_dir))
            extra = stage / "tests" / "unexpected.md"
            extra.parent.mkdir()
            extra.write_text("extra\n", encoding="utf-8")
            errors = validator.validate(stage, "9.2.0")
            self.assertIn(
                "Unexpected runtime file: tests/unexpected.md", errors
            )

    def test_mismatched_runtime_version_surface_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            stage = self.stage_runtime(Path(temp_dir))
            openai = stage / "agents" / "openai.yaml"
            text = openai.read_text(encoding="utf-8")
            openai.write_text(
                text.replace("v9.2.0", "v9.9.0", 1), encoding="utf-8"
            )
            errors = validator.validate(stage, "9.2.0")
            self.assertTrue(
                any("Version mismatch" in error for error in errors), errors
            )

    def test_explicit_v99_package_version_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "gra-skill-v99.zip"
            with self.assertRaisesRegex(SystemExit, "Invalid --version"):
                package.build_zip("99", output)
            self.assertFalse(output.exists())

    def test_package_filename_must_match_validated_version(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "gra-skill-v9.9.0.zip"
            with self.assertRaisesRegex(SystemExit, "must be"):
                package.build_zip("9.2.0", output)
            self.assertFalse(output.exists())

    def test_built_zip_contains_exact_six_file_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "gra-skill-v9.2.0.zip"
            package.build_zip("9.2.0", output)
            with zipfile.ZipFile(output) as archive:
                files = {
                    name.removeprefix("gra/")
                    for name in archive.namelist()
                    if not name.endswith("/")
                }
            self.assertEqual(validator.EXPECTED_FILES, files)

    def test_build_is_byte_identical_across_mtimes_and_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first_source = self.stage_packaging_source(
                root / "first", crlf=False, mtime=946684800
            )
            second_source = self.stage_packaging_source(
                root / "second", crlf=True, mtime=1735689600
            )
            first_zip = root / "first-output" / "gra-skill-v9.2.0.zip"
            second_zip = root / "second-output" / "gra-skill-v9.2.0.zip"

            with patch.object(package, "SKILL_ROOT", first_source):
                package.build_zip("9.2.0", first_zip)
            with patch.object(package, "SKILL_ROOT", second_source):
                package.build_zip("9.2.0", second_zip)

            self.assertEqual(first_zip.read_bytes(), second_zip.read_bytes())

    def test_built_zip_uses_fixed_metadata_and_canonical_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "gra-skill-v9.2.0.zip"
            package.build_zip("9.2.0", output)

            expected_names = [
                (Path("gra") / relative).as_posix()
                for relative in sorted(package.RUNTIME_FILES)
            ]
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(expected_names, archive.namelist())
                self.assertEqual(b"", archive.comment)
                for info in archive.infolist():
                    with self.subTest(path=info.filename):
                        mode = info.external_attr >> 16
                        self.assertEqual(package.ZIP_DATE_TIME, info.date_time)
                        self.assertEqual(package.ZIP_CREATE_SYSTEM, info.create_system)
                        self.assertEqual(stat.S_IFREG, stat.S_IFMT(mode))
                        self.assertEqual(0o644, stat.S_IMODE(mode))
                        self.assertEqual(package.ZIP_COMPRESSION, info.compress_type)
                        self.assertEqual(b"", info.extra)
                        self.assertEqual(b"", info.comment)
                        self.assertNotIn(b"\r", archive.read(info))


if __name__ == "__main__":
    unittest.main()
