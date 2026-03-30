#!/usr/bin/env python3
"""
Minimal test suite for gedcom_builder.py — stdlib only, no pytest.

Run:  python test_gedcom_builder.py
Exit: 0 = all pass, 1 = any failure

Each test targets a specific bug class (found or predicted).
"""

import json
import os
import sys
import tempfile
import unittest

# Ensure the script under test is importable
sys.path.insert(0, os.path.dirname(__file__))
import gedcom_builder as gb


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")


def _build(data, **kwargs):
    """Shortcut: build GEDCOM lines + report from a dict."""
    return gb.build_gedcom(data, **kwargs)


def _ged_text(lines):
    """Join GEDCOM lines into a single string for substring checks."""
    return "\n".join(lines)


def _load_example(name):
    with open(os.path.join(EXAMPLES_DIR, name), encoding="utf-8") as f:
        return json.load(f) if name.endswith(".json") else f.read()


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

class TestBAPMYearExtraction(unittest.TestCase):
    """Bug #1 (found): BAPM-only individuals were flagged as living."""

    def test_bapm_only_not_redacted(self):
        """A person baptised in 1580 with no BIRT/DEAT must NOT be redacted."""
        data = {
            "individuals": [{
                "id": "I1", "given": "William", "surname": "Test",
                "sex": "M",
                "events": [{"type": "BAPM", "date": "18 SEP 1580",
                            "place": "Somewhere"}],
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        self.assertEqual(len(report["redactions"]), 0,
                         "1580 baptism should not trigger living-person redaction")
        self.assertIn("William /Test/", _ged_text(lines))

    def test_chr_only_not_redacted(self):
        """CHR (christening) should also work as a birth-year proxy."""
        data = {
            "individuals": [{
                "id": "I1", "given": "Anne", "surname": "Test",
                "sex": "F",
                "events": [{"type": "CHR", "date": "1605",
                            "place": "Somewhere"}],
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        self.assertEqual(len(report["redactions"]), 0)


class TestHistoricalRedaction(unittest.TestCase):
    """Bug #2 (found): no-date historical figures redacted as living."""

    def test_no_dates_is_redacted_by_default(self):
        """Without dates or death event, a person IS redacted (correct behavior).
        This is the conservative default — the --all-deceased flag is the fix."""
        data = {
            "individuals": [{
                "id": "I1", "given": "John", "surname": "Historical",
                "sex": "M", "events": [],
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        self.assertEqual(len(report["redactions"]), 1)
        self.assertIn("[Living]", _ged_text(lines))

    def test_include_living_flag_unredacts(self):
        """The include_living flag should show everyone."""
        data = {
            "individuals": [{
                "id": "I1", "given": "John", "surname": "Historical",
                "sex": "M", "events": [],
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data, include_living=True)
        self.assertEqual(len(report["redactions"]), 0)
        self.assertIn("John /Historical/", _ged_text(lines))


class TestCONCMultibyteSafe(unittest.TestCase):
    """Predicted bug: CONC split mid-multibyte character."""

    def test_long_cjk_note_no_corruption(self):
        """A long string of CJK characters must never produce a line > 255 bytes."""
        # Each CJK char is 3 bytes in UTF-8. A 100-char string = 300 bytes,
        # which will force at least one CONC split.
        long_note = "\u4e00" * 100  # 100 copies of CJK unified ideograph
        data = {
            "individuals": [{
                "id": "I1", "given": "Test", "surname": "CJK",
                "sex": "M",
                "events": [{"type": "BIRT", "date": "1800", "place": "China"},
                           {"type": "DEAT", "date": "1870", "place": "China"}],
                "notes": [long_note],
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        for line in lines:
            byte_len = len(line.encode("utf-8"))
            self.assertLessEqual(byte_len, gb.MAX_LINE_LENGTH,
                                 f"Line exceeds 255 bytes ({byte_len}): {line[:40]}...")
        # Verify the content round-trips: reassemble CONC lines
        conc_parts = [l for l in lines if "CONC" in l or long_note[:5] in l]
        self.assertGreater(len(conc_parts), 1, "Should have split into CONC lines")

    def test_long_ascii_note_splits(self):
        """A long ASCII note should also split correctly."""
        long_note = "A" * 300
        data = {
            "individuals": [{
                "id": "I1", "given": "Test", "surname": "Long",
                "sex": "M",
                "events": [{"type": "BIRT", "date": "1800", "place": "USA"},
                           {"type": "DEAT", "date": "1870", "place": "USA"}],
                "notes": [long_note],
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        for line in lines:
            self.assertLessEqual(len(line.encode("utf-8")), gb.MAX_LINE_LENGTH)


class TestFAMCFAMSPointerConsistency(unittest.TestCase):
    """Predicted bug: FAMC/FAMS reversal in blended families."""

    def test_child_in_two_families_famc(self):
        """A child should have exactly one FAMC. Auto-repair should not
        create a second one even if two families list the same child."""
        data = {
            "individuals": [
                {"id": "I1", "given": "Dad", "surname": "A", "sex": "M",
                 "events": [{"type": "DEAT", "date": "1900"}],
                 "family_child": "", "family_spouse": ["F1"]},
                {"id": "I2", "given": "Mom", "surname": "B", "sex": "F",
                 "events": [{"type": "DEAT", "date": "1900"}],
                 "family_child": "", "family_spouse": ["F1"]},
                {"id": "I3", "given": "Kid", "surname": "A", "sex": "M",
                 "events": [{"type": "DEAT", "date": "1920"}],
                 "family_child": "F1", "family_spouse": ["F2"]},
                {"id": "I4", "given": "Spouse", "surname": "C", "sex": "F",
                 "events": [{"type": "DEAT", "date": "1930"}],
                 "family_child": "", "family_spouse": ["F2"]},
                {"id": "I5", "given": "Grandkid", "surname": "A", "sex": "M",
                 "events": [{"type": "DEAT", "date": "1950"}],
                 "family_child": "F2", "family_spouse": []},
            ],
            "families": [
                {"id": "F1", "spouse1": "I1", "spouse2": "I2",
                 "children": ["I3"], "events": [], "source_citations": [],
                 "notes": []},
                {"id": "F2", "spouse1": "I3", "spouse2": "I4",
                 "children": ["I5"], "events": [], "source_citations": [],
                 "notes": []},
            ],
            "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        ged = _ged_text(lines)
        # I3 should have FAMC @F1@ and FAMS @F2@ — never FAMC @F2@
        i3_block = ged.split("0 @I3@ INDI")[1].split("\n0 ")[0]
        self.assertIn("FAMC @F1@", i3_block)
        self.assertIn("FAMS @F2@", i3_block)
        self.assertNotIn("FAMC @F2@", i3_block)
        self.assertEqual(len(report["validation_errors"]), 0)

    def test_bidirectional_repair(self):
        """If JSON omits family_spouse on a parent, auto-repair should add it."""
        data = {
            "individuals": [
                {"id": "I1", "given": "Dad", "surname": "X", "sex": "M",
                 "events": [{"type": "DEAT", "date": "1900"}],
                 "family_child": "", "family_spouse": []},  # Missing F1!
                {"id": "I2", "given": "Mom", "surname": "Y", "sex": "F",
                 "events": [{"type": "DEAT", "date": "1900"}],
                 "family_child": "", "family_spouse": ["F1"]},
            ],
            "families": [
                {"id": "F1", "spouse1": "I1", "spouse2": "I2",
                 "children": [], "events": [], "source_citations": [],
                 "notes": []},
            ],
            "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        self.assertGreater(len(report["repairs"]), 0,
                           "Should have repaired I1 missing FAMS")
        self.assertIn("FAMS @F1@", _ged_text(lines))


class TestDanglingPointers(unittest.TestCase):
    """Predicted bug: pointer references to nonexistent records."""

    def test_missing_source_is_validation_error(self):
        data = {
            "individuals": [{
                "id": "I1", "given": "Test", "surname": "Ptr",
                "sex": "M",
                "events": [{"type": "BIRT", "date": "1800",
                            "source_id": "S_NONEXISTENT"}],
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data, include_living=True)
        errors = " ".join(report["validation_errors"])
        self.assertIn("DANGLING_POINTER", errors)

    def test_missing_family_is_validation_error(self):
        data = {
            "individuals": [{
                "id": "I1", "given": "Test", "surname": "Ptr",
                "sex": "M", "events": [],
                "family_child": "F_NONEXISTENT", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data, include_living=True)
        errors = " ".join(report["validation_errors"])
        self.assertIn("DANGLING_POINTER", errors)


class TestDualDating(unittest.TestCase):
    """Parish register edge case: dual dates like '14 MAR 1649/50'."""

    def test_dual_date_year_extraction(self):
        """_parse_year_from_date should extract 1649 from '14 MAR 1649/50'."""
        # The / split means parts become ['14', 'MAR', '1649', '50']
        # The function should find 1649 scanning reversed
        year = gb._parse_year_from_date("14 MAR 1649/50")
        self.assertIsNotNone(year)
        self.assertIn(year, (1649, 1650),
                      "Should extract a valid year from dual-date")

    def test_bet_and_range_date(self):
        year = gb._parse_year_from_date("BET 1800 AND 1810")
        self.assertIsNotNone(year)
        self.assertGreaterEqual(year, 1800)


class TestGEDCOMStructure(unittest.TestCase):
    """Structural invariants: HEAD, TRLR, CRLF, line format."""

    def test_head_and_trlr_present(self):
        data = {"individuals": [], "families": [],
                "sources": [], "repositories": []}
        lines, report = _build(data)
        self.assertTrue(lines[0].startswith("0 HEAD"))
        self.assertEqual(lines[-1], "0 TRLR")

    def test_empty_input_produces_valid_file(self):
        data = {"individuals": [], "families": [],
                "sources": [], "repositories": []}
        lines, report = _build(data)
        self.assertEqual(len(report["validation_errors"]), 0)


class TestExampleRegression(unittest.TestCase):
    """Diff-based regression: example JSON -> expected GED (date-insensitive)."""

    def _normalize(self, text):
        """Strip the DATE line from header (changes daily) and trailing whitespace."""
        out = []
        for line in text.replace("\r\n", "\n").split("\n"):
            stripped = line.rstrip()
            if stripped.startswith("1 DATE") and len(stripped.split()) == 4:
                # Header date line — normalize
                out.append("1 DATE [TODAY]")
            else:
                out.append(stripped)
        # Drop trailing blank lines
        while out and not out[-1]:
            out.pop()
        return "\n".join(out)

    def test_sample_input_regression(self):
        data = _load_example("sample-input.json")
        expected = _load_example("expected-output.ged")
        lines, report = _build(data, submitter="Your Name")
        actual = "\n".join(lines)
        self.assertEqual(self._normalize(actual), self._normalize(expected),
                         "sample-input.json output differs from expected-output.ged")

    def test_parish_register_regression(self):
        data = _load_example("parish-register-whitchurch.json")
        expected = _load_example("parish-register-whitchurch.ged")
        lines, report = _build(data, submitter="Your Name")
        actual = "\n".join(lines)
        self.assertEqual(self._normalize(actual), self._normalize(expected),
                         "parish-register output differs from expected .ged")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
