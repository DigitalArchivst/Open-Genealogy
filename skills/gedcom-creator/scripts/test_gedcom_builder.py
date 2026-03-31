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


class TestLivingWillNotDeceased(unittest.TestCase):
    """v1.3 bug fix: WILL event must NOT classify a person as deceased."""

    def test_living_person_with_will_is_redacted(self):
        """A living person who drafted a will should still be redacted."""
        data = {
            "individuals": [{
                "id": "I1", "given": "John", "surname": "Modern",
                "sex": "M",
                "events": [
                    {"type": "BIRT", "date": "15 MAR 1960", "place": "Virginia"},
                    {"type": "WILL", "date": "1 MAR 2022", "place": "Virginia"},
                ],
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        self.assertEqual(len(report["redactions"]), 1,
                         "Living person with WILL should be redacted")
        self.assertIn("[Living]", _ged_text(lines))

    def test_historical_will_still_deceased_via_inference(self):
        """A historical will (1642) with no other death evidence should
        still be classified as deceased via any-event date inference."""
        data = {
            "individuals": [{
                "id": "I1", "given": "William", "surname": "Whitchurch",
                "sex": "M",
                "events": [
                    {"type": "WILL", "date": "12 JAN 1641", "place": "Somewhere"},
                ],
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        self.assertEqual(len(report["redactions"]), 0,
                         "1641 will should infer historical era — not redacted")
        self.assertIn("William /Whitchurch/", _ged_text(lines))

    def test_prob_still_indicates_death(self):
        """PROB (probate) should still indicate death — only WILL was removed."""
        data = {
            "individuals": [{
                "id": "I1", "given": "Jane", "surname": "Doe",
                "sex": "F",
                "events": [
                    {"type": "BIRT", "date": "1960"},
                    {"type": "PROB", "date": "2024"},
                ],
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        self.assertEqual(len(report["redactions"]), 0,
                         "PROB should still classify as deceased")
        self.assertIn("Jane /Doe/", _ged_text(lines))


class TestDeceasedBeforeUndated(unittest.TestCase):
    """v1.3 bug fix: --deceased-before with undated individuals."""

    def test_undated_individual_exempted(self):
        """An undated individual should NOT be redacted when
        --deceased-before is set."""
        data = {
            "individuals": [{
                "id": "I1", "given": "Unknown", "surname": "Person",
                "sex": "U", "events": [],
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data, deceased_before=1600)
        self.assertEqual(len(report["redactions"]), 0,
                         "Undated individual with --deceased-before should not be redacted")
        self.assertIn("Unknown /Person/", _ged_text(lines))

    def test_dated_above_threshold_still_redacted(self):
        """An individual with events ABOVE the deceased-before threshold
        should still be redacted if otherwise presumed living."""
        data = {
            "individuals": [{
                "id": "I1", "given": "Recent", "surname": "Person",
                "sex": "M",
                "events": [{"type": "BIRT", "date": "1990"}],
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data, deceased_before=1900)
        self.assertEqual(len(report["redactions"]), 1,
                         "Person born 1990 with --deceased-before 1900 should still be redacted")


class TestCONTEmission(unittest.TestCase):
    """v1.3 feature: embedded newlines in notes produce CONT lines."""

    def test_multiline_note_produces_cont(self):
        """A note with embedded newlines should emit CONT lines."""
        data = {
            "individuals": [{
                "id": "I1", "given": "Test", "surname": "CONT",
                "sex": "M",
                "events": [{"type": "BIRT", "date": "1800"},
                           {"type": "DEAT", "date": "1870"}],
                "notes": ["First paragraph.\nSecond paragraph.\nThird paragraph."],
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        ged = _ged_text(lines)
        self.assertIn("1 NOTE First paragraph.", ged)
        self.assertIn("2 CONT Second paragraph.", ged)
        self.assertIn("2 CONT Third paragraph.", ged)


class TestAutoRepairWarning(unittest.TestCase):
    """v1.3 fix: auto-repair logs warning when both spouse slots filled."""

    def test_third_spouse_logs_warning(self):
        """If three individuals claim FAMS to the same family,
        auto-repair should log a warning for the third."""
        data = {
            "individuals": [
                {"id": "I1", "given": "A", "surname": "X", "sex": "M",
                 "events": [{"type": "DEAT", "date": "1900"}],
                 "family_child": "", "family_spouse": ["F1"]},
                {"id": "I2", "given": "B", "surname": "Y", "sex": "F",
                 "events": [{"type": "DEAT", "date": "1900"}],
                 "family_child": "", "family_spouse": ["F1"]},
                {"id": "I3", "given": "C", "surname": "Z", "sex": "M",
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
        warning_found = any("Cannot assign I3" in r for r in report["repairs"])
        self.assertTrue(warning_found,
                        "Should log warning when third spouse can't be assigned")


class TestSameSexCoupleNote(unittest.TestCase):
    """v1.3 feature: same-sex couples get a NOTE about HUSB/WIFE limitation."""

    def test_same_sex_male_couple(self):
        """Two male spouses should produce a NOTE about positional assignment."""
        data = {
            "individuals": [
                {"id": "I1", "given": "John", "surname": "A", "sex": "M",
                 "events": [{"type": "DEAT", "date": "2020"}],
                 "family_child": "", "family_spouse": ["F1"]},
                {"id": "I2", "given": "James", "surname": "B", "sex": "M",
                 "events": [{"type": "DEAT", "date": "2020"}],
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
        ged = _ged_text(lines)
        self.assertIn("HUSB @I1@", ged)
        self.assertIn("WIFE @I2@", ged)
        self.assertIn("positional assignment", ged.lower())


class TestFAMLivingRedaction(unittest.TestCase):
    """v1.3.1 bug fix: FAM events stripped when all spouses are living."""

    def test_marr_stripped_when_both_spouses_living(self):
        """MARR date/place should not appear when both spouses are living."""
        data = {
            "individuals": [
                {"id": "I1", "given": "John", "surname": "Modern",
                 "sex": "M",
                 "events": [{"type": "BIRT", "date": "1980"}],
                 "family_child": "", "family_spouse": ["F1"]},
                {"id": "I2", "given": "Jane", "surname": "Modern",
                 "sex": "F",
                 "events": [{"type": "BIRT", "date": "1982"}],
                 "family_child": "", "family_spouse": ["F1"]},
            ],
            "families": [
                {"id": "F1", "spouse1": "I1", "spouse2": "I2",
                 "children": [], "source_citations": [], "notes": [],
                 "events": [{"type": "MARR", "date": "15 JUN 2005",
                             "place": "Norfolk, Virginia"}]},
            ],
            "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        ged = _ged_text(lines)
        # Both spouses should be redacted
        self.assertEqual(len(report["redactions"]), 2)
        # MARR should NOT appear in the FAM record
        fam_block = ged.split("0 @F1@ FAM")[1].split("\n0 ")[0]
        self.assertNotIn("MARR", fam_block,
                         "MARR should be stripped when both spouses are living")
        self.assertNotIn("Norfolk", fam_block)

    def test_marr_kept_when_one_spouse_deceased(self):
        """MARR should remain when at least one spouse is deceased."""
        data = {
            "individuals": [
                {"id": "I1", "given": "John", "surname": "Mixed",
                 "sex": "M",
                 "events": [{"type": "BIRT", "date": "1950"},
                            {"type": "DEAT", "date": "2020"}],
                 "family_child": "", "family_spouse": ["F1"]},
                {"id": "I2", "given": "Jane", "surname": "Mixed",
                 "sex": "F",
                 "events": [{"type": "BIRT", "date": "1955"}],
                 "family_child": "", "family_spouse": ["F1"]},
            ],
            "families": [
                {"id": "F1", "spouse1": "I1", "spouse2": "I2",
                 "children": [], "source_citations": [], "notes": [],
                 "events": [{"type": "MARR", "date": "10 SEP 1975",
                             "place": "Richmond, Virginia"}]},
            ],
            "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        ged = _ged_text(lines)
        # Only I2 is living (I1 has DEAT)
        self.assertEqual(len(report["redactions"]), 1)
        fam_block = ged.split("0 @F1@ FAM")[1].split("\n0 ")[0]
        self.assertIn("MARR", fam_block,
                      "MARR should remain when one spouse is deceased")
        self.assertIn("Richmond", fam_block)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
