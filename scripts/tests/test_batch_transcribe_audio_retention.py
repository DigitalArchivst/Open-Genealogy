"""Offline regression tests for batch full-audio retention."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "batch_transcribe_v2.py"


def _load_batch_script():
    module_name = "batch_transcribe_v2_retention_test"
    spec = importlib.util.spec_from_file_location(module_name, SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {SCRIPT_PATH}")

    module = importlib.util.module_from_spec(spec)
    fake_pydub = types.ModuleType("pydub")
    fake_pydub.AudioSegment = object
    with patch.dict(sys.modules, {"pydub": fake_pydub}):
        spec.loader.exec_module(module)
    return module


class FakeAudioSegment:
    """Writes a deterministic MP3 placeholder instead of converting media."""

    @classmethod
    def from_file(cls, source: str):
        return cls()

    def export(self, destination: str, **_kwargs) -> None:
        Path(destination).write_bytes(b"offline test MP3")


class BatchAudioRetentionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.batch = _load_batch_script()

    def test_default_batch_does_not_copy_full_audio(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "sensitive interview.wav"
            source.write_bytes(b"not real audio")
            transcriber = root / "transcribe-4o-chunk-v2.py"
            transcriber.write_text("# test stub\n", encoding="utf-8")
            calls = []

            def fake_transcriber(*args):
                calls.append(args)
                return 0

            with patch.object(self.batch, "_extract_full_audio") as extract_audio:
                result = self.batch._process_batch(
                    [source],
                    transcriber=transcriber,
                    output_choice="1",
                    custom_output_dir=None,
                    skip_existing=False,
                    retain_audio=False,
                    run_one=fake_transcriber,
                )

            self.assertEqual((1, 0, 0), result)
            self.assertEqual(1, len(calls))
            extract_audio.assert_not_called()
            self.assertFalse((root / "transcripts").exists())
            self.assertEqual([], list(root.rglob("audio_*.mp3")))

    def test_opt_in_retains_audio_in_selected_transcripts_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "sensitive interview.wav"
            source.write_bytes(b"not real audio")
            transcriber = root / "tool" / "transcribe-4o-chunk-v2.py"
            transcriber.parent.mkdir()
            transcriber.write_text("# test stub\n", encoding="utf-8")
            destination = root / "retained-output"

            with patch.object(self.batch, "AudioSegment", FakeAudioSegment):
                result = self.batch._process_batch(
                    [source],
                    transcriber=transcriber,
                    output_choice="3",
                    custom_output_dir=destination,
                    skip_existing=False,
                    retain_audio=True,
                    run_one=lambda *_args: 0,
                )

            retained_copy = destination / "transcripts" / "audio_sensitive interview.mp3"
            self.assertEqual((1, 0, 0), result)
            self.assertEqual(b"offline test MP3", retained_copy.read_bytes())
            self.assertEqual([retained_copy], list(root.rglob("audio_*.mp3")))

    def test_failed_retention_extraction_does_not_transcribe(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "sensitive interview.wav"
            source.write_bytes(b"not real audio")
            transcriber = root / "transcribe-4o-chunk-v2.py"
            transcriber.write_text("# test stub\n", encoding="utf-8")
            calls = []

            def fake_transcriber(*args):
                calls.append(args)
                return 0

            with patch.object(
                self.batch, "_extract_full_audio", return_value=None
            ):
                result = self.batch._process_batch(
                    [source],
                    transcriber=transcriber,
                    output_choice="1",
                    custom_output_dir=None,
                    skip_existing=False,
                    retain_audio=True,
                    run_one=fake_transcriber,
                )

            self.assertEqual((0, 0, 1), result)
            self.assertEqual([], calls)

    def test_partial_existing_mp3_is_replaced_without_completion_marker(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = root / "interview.wav"
            source.write_bytes(b"not real audio")
            destination = root / "transcripts"
            destination.mkdir()
            partial = destination / "audio_interview.mp3"
            partial.write_bytes(b"partial")

            with patch.object(self.batch, "AudioSegment", FakeAudioSegment):
                retained = self.batch._extract_full_audio(source, destination)

            self.assertEqual(partial, retained)
            self.assertEqual(b"offline test MP3", partial.read_bytes())
            self.assertEqual(
                "complete\n",
                partial.with_name(partial.name + ".ok").read_text(
                    encoding="ascii"
                ),
            )


if __name__ == "__main__":
    unittest.main()
