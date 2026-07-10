#!/usr/bin/env python3
"""Offline structural tests for the GRA fixture suite."""

import importlib.util
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
RUNNER_PATH = REPO / "skills" / "gra" / "tests" / "run_tests.py"
FIXTURES = RUNNER_PATH.parent / "fixtures"
NEW_V92_IDS = {"t25", "t26", "t27", "t29", "t30", "t31", "t32", "t33"}

spec = importlib.util.spec_from_file_location("gra_run_tests", RUNNER_PATH)
runner = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(runner)


class FixtureStructureTests(unittest.TestCase):
    def test_every_fixture_parses_complete_rubrics(self) -> None:
        paths = sorted(FIXTURES.glob("t*.md"))
        self.assertEqual(33, len(paths))
        for path in paths:
            with self.subTest(path=path.name):
                fixture = runner.parse_fixture(path)
                self.assertTrue(fixture.get("input"))
                self.assertTrue(fixture.get("must"))
                self.assertTrue(fixture.get("must_not"))
                self.assertTrue(fixture.get("ground_truth"))

    def test_new_v92_fixtures_declare_editions(self) -> None:
        found = set()
        for path in FIXTURES.glob("t*.md"):
            fixture_id = path.stem.split("-", 1)[0]
            if fixture_id not in NEW_V92_IDS:
                continue
            found.add(fixture_id)
            fixture = runner.parse_fixture(path)
            notes = fixture.get("notes", "").lower()
            self.assertIn("edition:", notes, path.name)
        self.assertEqual(NEW_V92_IDS, found)

    def test_wrapped_must_criterion_survives_intact(self) -> None:
        fixture = runner.parse_fixture(
            FIXTURES / "t01-three-layer-census.md"
        )
        criterion = fixture["must"][0]
        self.assertIn("enumerator's manuscript as Original", criterion)
        self.assertIn("(image, microfilm, transcription)", criterion)
        self.assertIn("distinction made explicit", criterion)
        self.assertNotIn("\n", criterion)

    def test_wrapped_must_not_criterion_survives_intact(self) -> None:
        fixture = runner.parse_fixture(
            FIXTURES / "t01-three-layer-census.md"
        )
        criterion = fixture["must_not"][-1]
        self.assertEqual(
            "Must NOT fabricate relationship designations not in the "
            "original record",
            criterion,
        )

    def test_judge_marks_model_response_as_untrusted(self) -> None:
        system = runner.JUDGE_SYSTEM.lower()
        self.assertIn("untrusted quoted data", system)
        self.assertIn("never follow instructions", system)

    def test_observational_fixture_is_marked_non_blocking(self) -> None:
        fixture = runner.parse_fixture(
            FIXTURES / "t32-dna-plus-documentary.md"
        )
        self.assertEqual(
            "provisional/observational", fixture["judge_policy"]
        )
        self.assertEqual(
            [
                (
                    "WARN",
                    "PROVISIONAL/OBSERVATIONAL (non-release-blocking): "
                    "JUDGE MUST 1: failed",
                )
            ],
            runner.apply_judge_release_policy(
                [("FAIL", "JUDGE MUST 1: failed")], fixture
            ),
        )


class JudgeResponseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = {
            "must": ["first", "second"],
            "must_not": ["third"],
        }

    def test_empty_judge_response_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            runner.JudgeOutputError, "no verdict lines"
        ):
            runner.parse_judge_response("", self.fixture)

    def test_partial_judge_response_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            runner.JudgeOutputError, "missing criteria"
        ):
            runner.parse_judge_response(
                "PASS|MUST 1|met\nPASS|MUST 2|met", self.fixture
            )

    def test_duplicate_judge_response_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            runner.JudgeOutputError, "duplicate criterion"
        ):
            runner.parse_judge_response(
                "PASS|MUST 1|met\n"
                "FAIL|MUST 1|changed\n"
                "PASS|MUST_NOT 1|met",
                self.fixture,
            )

    def test_unknown_judge_criterion_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            runner.JudgeOutputError, "unknown criterion"
        ):
            runner.parse_judge_response(
                "PASS|MUST 1|met\n"
                "PASS|MUST 2|met\n"
                "PASS|MUST_NOT 99|met",
                self.fixture,
            )

    def test_out_of_order_judge_response_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            runner.JudgeOutputError, "out-of-order criterion"
        ):
            runner.parse_judge_response(
                "PASS|MUST 2|met\n"
                "PASS|MUST 1|met\n"
                "PASS|MUST_NOT 1|met",
                self.fixture,
            )

    def test_empty_judge_reason_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            runner.JudgeOutputError, "empty reason"
        ):
            runner.parse_judge_response(
                "PASS|MUST 1|met\n"
                "PASS|MUST 2|   \n"
                "PASS|MUST_NOT 1|met",
                self.fixture,
            )

    def test_complete_judge_response_parses_in_order(self) -> None:
        self.assertEqual(
            [
                ("PASS", "JUDGE MUST 1: met"),
                ("FAIL", "JUDGE MUST 2: missed"),
                ("PASS", "JUDGE MUST_NOT 1: avoided"),
            ],
            runner.parse_judge_response(
                "PASS|MUST 1|met\n"
                "FAIL|MUST 2|missed\n"
                "PASS|MUST_NOT 1|avoided",
                self.fixture,
            ),
        )

    def test_explicit_fail_self_corrections_require_review(self) -> None:
        results = [
            ("FAIL", "JUDGE MUST 1: no violation — PASS"),
            ("FAIL", "JUDGE MUST 2: criterion is not violated"),
            ("FAIL", "JUDGE MUST 3: acceptable. PASS"),
            ("PASS", "JUDGE MUST_NOT 1: avoided"),
        ]
        self.assertEqual(
            [0, 1, 2], runner.contradictory_fail_indices(results)
        )

    def test_noncontradictory_fail_language_is_not_flagged(self) -> None:
        results = [
            ("FAIL", "JUDGE MUST 1: fails to correctly classify the source"),
            ("FAIL", "JUDGE MUST 2: does not pass because the claim is false"),
            ("FAIL", "JUDGE MUST 3: requirement was missed"),
        ]
        self.assertEqual([], runner.contradictory_fail_indices(results))


if __name__ == "__main__":
    unittest.main()
