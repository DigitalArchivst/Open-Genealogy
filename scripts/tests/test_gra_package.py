"""Offline tests for the exact GRA runtime package contract."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
