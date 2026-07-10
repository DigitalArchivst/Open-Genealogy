#!/usr/bin/env python3
"""Regression tests for GRA chat-edition generation."""

import unittest

from generate_chat_edition import generate, normalize_for_comparison, OUTPUT


class ProvenanceNormalizationTests(unittest.TestCase):
    def test_provenance_comments_compare_equal_case_insensitively(self) -> None:
        lower = "<!-- generated from SKILL.md@abc+wt -->\nbody\n"
        upper = "<!-- Generated from SKILL.md@def -->\nbody\n"
        self.assertEqual(
            normalize_for_comparison(lower),
            normalize_for_comparison(upper),
        )

    def test_body_changes_do_not_compare_equal(self) -> None:
        original = "<!-- generated from SKILL.md@abc -->\nbody\n"
        changed = "<!-- generated from SKILL.md@def -->\nchanged body\n"
        self.assertNotEqual(
            normalize_for_comparison(original),
            normalize_for_comparison(changed),
        )

    def test_shipped_artifact_matches_current_generation(self) -> None:
        shipped = OUTPUT.read_text(encoding="utf-8")
        self.assertEqual(
            normalize_for_comparison(shipped),
            normalize_for_comparison(generate()),
        )


if __name__ == "__main__":
    unittest.main()
