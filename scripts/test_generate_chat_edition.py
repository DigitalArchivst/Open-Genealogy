#!/usr/bin/env python3
"""Regression tests for GRA chat-edition generation."""

import re
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_chat_edition as generator
from generate_chat_edition import (
    CHAT_CHAR_LIMIT,
    OUTPUT,
    generate,
    normalize_line_endings,
    provenance_line,
)

MEASURE_PATH = Path(__file__).with_name("measure_gra_compact.py")
measure_spec = importlib.util.spec_from_file_location(
    "measure_gra_compact_test", MEASURE_PATH
)
measure = importlib.util.module_from_spec(measure_spec)
assert measure_spec.loader is not None
measure_spec.loader.exec_module(measure)


class ProvenanceValidationTests(unittest.TestCase):
    def test_provenance_names_and_hashes_both_inputs(self) -> None:
        line = provenance_line()
        self.assertRegex(
            line,
            r"^<!-- generated from "
            r"SKILL\.md@sha256:[0-9a-f]{64} \+ "
            r"generate_chat_edition\.py@sha256:[0-9a-f]{64}; "
            r"input_commit:[0-9a-f]{40} -->$",
        )

    def test_content_hash_normalizes_line_endings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            lf_path = Path(temp_dir) / "lf.txt"
            crlf_path = Path(temp_dir) / "crlf.txt"
            lf_path.write_bytes(b"one\ntwo\n")
            crlf_path.write_bytes(b"one\r\ntwo\r\n")
            self.assertEqual(
                generator.content_hash(lf_path),
                generator.content_hash(crlf_path),
            )

    def test_provenance_only_change_does_not_compare_equal(self) -> None:
        original = generate()
        changed = re.sub(
            r"SKILL\.md@sha256:[0-9a-f]{64}",
            "SKILL.md@sha256:" + ("0" * 64),
            original,
            count=1,
        )
        self.assertNotEqual(
            normalize_line_endings(original),
            normalize_line_endings(changed),
        )

    def test_body_changes_do_not_compare_equal(self) -> None:
        original = generate()
        changed = original.replace("## 1. RULES", "## 1. CHANGED", 1)
        self.assertNotEqual(
            normalize_line_endings(original),
            normalize_line_endings(changed),
        )

    def test_skill_change_requires_regeneration(self) -> None:
        shipped = OUTPUT.read_text(encoding="utf-8")
        source = generator.SOURCE.read_text(encoding="utf-8")
        commit = generator.input_commit()
        with tempfile.TemporaryDirectory() as temp_dir:
            changed_source = Path(temp_dir) / "SKILL.md"
            changed_source.write_text(
                source.replace(
                    "Say when evidence is insufficient.",
                    "Say clearly when evidence is insufficient.",
                    1,
                ),
                encoding="utf-8",
            )
            with patch.object(generator, "SOURCE", changed_source), patch.object(
                generator, "input_commit", return_value=commit
            ):
                changed = generator.generate()
        self.assertNotEqual(
            normalize_line_endings(shipped),
            normalize_line_endings(changed),
        )

    def test_generator_hash_change_requires_regeneration(self) -> None:
        shipped = OUTPUT.read_text(encoding="utf-8")
        actual_hash = generator.content_hash

        def changed_generator_hash(path: Path) -> str:
            if path == generator.GENERATOR:
                return "0" * 64
            return actual_hash(path)

        with patch.object(
            generator, "content_hash", side_effect=changed_generator_hash
        ):
            changed = generator.generate()
        self.assertNotEqual(
            normalize_line_endings(shipped),
            normalize_line_endings(changed),
        )

    def test_shipped_artifact_matches_current_generation_exactly(self) -> None:
        shipped = OUTPUT.read_text(encoding="utf-8")
        self.assertEqual(
            normalize_line_endings(shipped),
            normalize_line_endings(generate()),
        )

    def test_generator_refuses_oversized_body_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "chat.md"
            output.write_text("sentinel", encoding="utf-8")
            with patch.object(generator, "OUTPUT", output):
                with patch.object(
                    generator,
                    "generate",
                    return_value="x" * CHAT_CHAR_LIMIT,
                ):
                    with patch.object(
                        sys, "argv", ["generate_chat_edition.py"]
                    ):
                        with self.assertRaisesRegex(
                            SystemExit, "CHAT GATE FAILED"
                        ):
                            generator.main()
            self.assertEqual("sentinel", output.read_text(encoding="utf-8"))

    def test_generator_refuses_missing_body_during_check(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "chat.md"
            output.write_text("sentinel", encoding="utf-8")
            with patch.object(generator, "OUTPUT", output):
                with patch.object(generator, "generate", return_value=""):
                    with patch.object(
                        sys,
                        "argv",
                        ["generate_chat_edition.py", "--check"],
                    ):
                        with self.assertRaisesRegex(
                            SystemExit, "CHAT GATE FAILED"
                        ):
                            generator.main()


class MeasureChatGateTests(unittest.TestCase):
    def test_measure_rejects_missing_chat_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing.md"
            with self.assertRaisesRegex(measure.ChatSizeError, "missing"):
                measure.load_valid_chat(missing)

    def test_measure_rejects_empty_chat_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            empty = Path(temp_dir) / "empty.md"
            empty.write_text("\n", encoding="utf-8")
            with self.assertRaisesRegex(measure.ChatSizeError, "empty"):
                measure.load_valid_chat(empty)

    def test_measure_rejects_8000_character_chat_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            oversized = Path(temp_dir) / "oversized.md"
            oversized.write_text(
                "x" * measure.CHAT_CHAR_LIMIT, encoding="utf-8"
            )
            with self.assertRaisesRegex(measure.ChatSizeError, "hard gate"):
                measure.load_valid_chat(oversized)


if __name__ == "__main__":
    unittest.main()
