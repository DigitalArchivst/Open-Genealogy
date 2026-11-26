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

    def test_same_inputs_with_different_mtimes_and_modes_match_sha256(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            copy_a = self.stage_runtime(root / "checkout_a")
            copy_b = self.stage_runtime(root / "checkout_b")
            version = package.read_default_version()

            base_ts = 1752130800.0
            for idx, relative in enumerate(package.RUNTIME_FILES):
                file_a = copy_a / relative
                file_b = copy_b / relative
                self.assertEqual(file_a.read_bytes(), file_b.read_bytes())
                os.utime(file_a, (base_ts + idx * 10, base_ts + idx * 10))
                os.utime(
                    file_b,
                    (base_ts + 86400 + idx * 10, base_ts + 86400 + idx * 10),
                )
                os.chmod(file_b, stat.S_IREAD)

            zip_a = root / "out_a" / f"gra-skill-v{version}.zip"
            zip_b = root / "out_b" / f"gra-skill-v{version}.zip"
            try:
                with patch.object(package, "SKILL_ROOT", copy_a):
                    package.build_zip(version, zip_a)
                with patch.object(package, "SKILL_ROOT", copy_b):
                    package.build_zip(version, zip_b)
            finally:
                for relative in package.RUNTIME_FILES:
                    os.chmod(copy_b / relative, stat.S_IWRITE | stat.S_IREAD)

            self.assertEqual(package.sha256(zip_a), package.sha256(zip_b))
            with zipfile.ZipFile(zip_a) as archive:
                for relative in package.RUNTIME_FILES:
                    self.assertEqual(
                        (copy_a / relative).read_bytes(),
                        archive.read(f"gra/{relative}"),
                    )

    def test_zip_member_order_and_metadata_are_canonical(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            version = package.read_default_version()
            output = Path(temp_dir) / f"gra-skill-v{version}.zip"
            package.build_zip(version, output)
            with zipfile.ZipFile(output) as archive:
                names = archive.namelist()
                self.assertEqual(sorted(names), names)
                self.assertLess(
                    names.index("gra/LICENSE"),
                    names.index("gra/agents/openai.yaml"),
                )
                self.assertEqual(
                    validator.EXPECTED_FILES,
                    {name.removeprefix("gra/") for name in names},
                )
                for info in archive.infolist():
                    self.assertFalse(info.filename.endswith("/"))
                    self.assertEqual(
                        package.DETERMINISTIC_DATE_TIME, info.date_time
                    )
                    self.assertEqual(
                        package.DETERMINISTIC_CREATE_SYSTEM,
                        info.create_system,
                    )
                    self.assertEqual(
                        package.DETERMINISTIC_EXTERNAL_ATTR,
                        info.external_attr,
                    )
                    self.assertEqual(zipfile.ZIP_DEFLATED, info.compress_type)

    def test_extracted_members_match_source_bytes_and_validate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            version = package.read_default_version()
            output = root / f"gra-skill-v{version}.zip"
            package.build_zip(version, output)
            extracted = root / "extracted"
            with zipfile.ZipFile(output) as archive:
                archive.extractall(extracted)
            self.assertEqual(
                [], validator.validate(extracted / "gra", version)
            )
            for relative in package.RUNTIME_FILES:
                self.assertEqual(
                    (package.SKILL_ROOT / relative).read_bytes(),
                    (extracted / "gra" / relative).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()
