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


class TestCycleDetection(unittest.TestCase):
    """Cycles are recursion-path repeats, not shared ancestors."""

    @staticmethod
    def _person(person_id, family_child="", family_spouse=None):
        return {
            "id": person_id, "given": person_id, "surname": "Cycle",
            "sex": "U", "events": [{"type": "DEAT", "date": "1900"}],
            "family_child": family_child,
            "family_spouse": family_spouse or [],
        }

    def test_pedigree_collapse_shared_ancestor_is_valid(self):
        data = {
            "individuals": [
                self._person("I1", "F1"),
                self._person("I2", "F2", ["F1"]),
                self._person("I3", "F3", ["F1"]),
                self._person("I4", "", ["F2", "F3"]),
                self._person("I5", "", ["F2"]),
                self._person("I6", "", ["F3"]),
            ],
            "families": [
                {"id": "F1", "spouse1": "I2", "spouse2": "I3",
                 "children": ["I1"], "events": [],
                 "source_citations": [], "notes": []},
                {"id": "F2", "spouse1": "I4", "spouse2": "I5",
                 "children": ["I2"], "events": [],
                 "source_citations": [], "notes": []},
                {"id": "F3", "spouse1": "I4", "spouse2": "I6",
                 "children": ["I3"], "events": [],
                 "source_citations": [], "notes": []},
            ],
            "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        self.assertNotEqual(lines, [])
        self.assertNotIn("CYCLE_DETECTED", " ".join(
            report["validation_errors"]
        ))

    def test_true_parent_child_cycle_fails(self):
        data = {
            "individuals": [
                self._person("I1", "F1", ["F2"]),
                self._person("I2", "F2", ["F1"]),
            ],
            "families": [
                {"id": "F1", "spouse1": "I2", "spouse2": "",
                 "children": ["I1"], "events": [],
                 "source_citations": [], "notes": []},
                {"id": "F2", "spouse1": "I1", "spouse2": "",
                 "children": ["I2"], "events": [],
                 "source_citations": [], "notes": []},
            ],
            "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        self.assertNotEqual(lines, [])
        self.assertIn("CYCLE_DETECTED", " ".join(
            report["validation_errors"]
        ))


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


class TestIdentifierValidation(unittest.TestCase):
    """Record IDs are unique and lexically valid before graph processing."""

    def _person(self, record_id):
        return {
            "id": record_id, "given": "Test", "surname": "Identifier",
            "sex": "U", "events": [{"type": "DEAT", "date": "1900"}],
            "family_child": "", "family_spouse": [],
        }

    def test_duplicate_same_type_stops_before_pointer_validation(self):
        first = self._person("I1")
        second = self._person("I1")
        second["family_child"] = "F_MISSING"
        data = {
            "individuals": [first, second],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        errors = " ".join(report["validation_errors"])
        self.assertEqual(lines, [])
        self.assertEqual(report["repairs"], [])
        self.assertIn("DUPLICATE_ID", errors)
        self.assertNotIn("DANGLING_POINTER", errors)

    def test_duplicate_across_record_types_is_rejected(self):
        data = {
            "individuals": [self._person("X1")],
            "families": [],
            "sources": [{
                "id": "X1", "title": "Duplicate", "author": "",
                "publication": "", "repository_id": "", "notes": [],
            }],
            "repositories": [],
        }
        lines, report = _build(data)
        self.assertEqual(lines, [])
        self.assertIn("DUPLICATE_ID", " ".join(report["validation_errors"]))

    def test_malformed_record_ids_are_rejected(self):
        malformed_ids = ("", "@I1@", "I 1", "I-1", "X" * 21, 1, None)
        for record_id in malformed_ids:
            with self.subTest(record_id=record_id):
                data = {
                    "individuals": [self._person(record_id)],
                    "families": [], "sources": [], "repositories": [],
                }
                lines, report = _build(data)
                errors = " ".join(report["validation_errors"])
                self.assertEqual(lines, [])
                self.assertIn("MALFORMED_ID", errors)
                self.assertNotIn("DANGLING_POINTER", errors)

    def test_generated_submitter_id_is_reserved(self):
        data = {
            "individuals": [self._person("U1")],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        self.assertEqual(lines, [])
        self.assertIn("DUPLICATE_ID", " ".join(report["validation_errors"]))

    def test_batch_merge_rejects_cross_file_duplicate(self):
        first = {
            "individuals": [self._person("X1")],
            "families": [], "sources": [], "repositories": [],
        }
        second = {
            "individuals": [], "families": [],
            "sources": [{"id": "X1", "title": "Duplicate"}],
            "repositories": [],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = [os.path.join(temp_dir, name)
                     for name in ("first.json", "second.json")]
            for path, payload in zip(paths, (first, second)):
                with open(path, "w", encoding="utf-8") as handle:
                    json.dump(payload, handle)
            with self.assertRaisesRegex(ValueError, "Duplicate ID"):
                gb.merge_json_files(paths)


class TestMalformedPointers(unittest.TestCase):
    """Pointer values must use canonical unwrapped xref syntax."""

    def test_malformed_pointer_forms_are_rejected(self):
        data = {
            "individuals": [
                {
                    "id": "I1", "given": "One", "surname": "Pointer",
                    "sex": "M", "events": [
                        {"type": "DEAT", "date": "1900",
                         "source_id": "@S1@"},
                    ],
                    "source_citations": [{"source_id": "S1@"}],
                    "family_child": "@F1@", "family_spouse": ["F1"],
                },
                {
                    "id": "I2", "given": "Two", "surname": "Pointer",
                    "sex": "F", "events": [{"type": "DEAT", "date": "1900"}],
                    "family_child": "", "family_spouse": ["F1"],
                },
            ],
            "families": [{
                "id": "F1", "spouse1": "I1", "spouse2": "I2",
                "children": [],
                "events": [{"type": "MARR", "date": "1890",
                            "source_id": "S 1"}],
                "source_citations": [{"source_id": None}], "notes": [],
            }],
            "sources": [{
                "id": "S1", "title": "Source", "author": "",
                "publication": "", "repository_id": "@R1@", "notes": [],
            }],
            "repositories": [{"id": "R1", "name": "Archive", "address": ""}],
        }
        lines, report = _build(data)
        errors = " ".join(report["validation_errors"])
        self.assertNotEqual(lines, [])
        self.assertEqual(errors.count("MALFORMED_POINTER"), 6)
        self.assertNotIn("DANGLING_POINTER", errors)


class TestDateValidation(unittest.TestCase):
    """Canonical JSON accepts only the documented GEDCOM date lexicon."""

    def test_documented_date_forms_are_accepted(self):
        valid_dates = (
            "1868", "MAR 1845", "15 MAR 1845", "ABT 1868",
            "BEF 1870", "AFT 1865", "CAL 1769", "EST 1800",
            "BET 1860 AND 1870", "FROM 1870 TO 1880", "FROM 1870",
            "TO 1880", "2 FEB 1731/32",
        )
        for value in valid_dates:
            with self.subTest(value=value):
                self.assertTrue(gb.is_valid_gedcom_date(value))

    def test_unsupported_date_forms_are_rejected(self):
        invalid_dates = (
            "March 15, 1845", "15 mar 1845", "0 JAN 1900",
            "32 JAN 1900", "15 XYZ 1900", "15 MAR", "ABT",
            "BET 1860 1870", "FROM 1870 AND 1880", "2026-07-10",
            " 15 MAR 1845", "15  MAR 1845", "INT 1900 (estimated)",
            "99", "10000", None, 0,
        )
        for value in invalid_dates:
            with self.subTest(value=value):
                self.assertFalse(gb.is_valid_gedcom_date(value))

    def test_invalid_individual_date_stops_before_rendering(self):
        data = {
            "individuals": [{
                "id": "I1", "given": "Bad", "surname": "Date", "sex": "U",
                "events": [{"type": "BIRT", "date": "Spring 1900"}],
                "family_child": "F_MISSING", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        errors = " ".join(report["validation_errors"])
        self.assertEqual(lines, [])
        self.assertIn("INVALID_DATE", errors)
        self.assertNotIn("DANGLING_POINTER", errors)

    def test_invalid_family_date_stops_before_rendering(self):
        data = {
            "individuals": [],
            "families": [{
                "id": "F1", "spouse1": "", "spouse2": "", "children": [],
                "events": [{"type": "MARR", "date": "1900-ish"}],
                "source_citations": [], "notes": [],
            }],
            "sources": [], "repositories": [],
        }
        lines, report = _build(data)
        self.assertEqual(lines, [])
        self.assertIn("INVALID_DATE", " ".join(report["validation_errors"]))


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
        """Normalize the dynamic header DATE and trailing whitespace."""
        out = []
        in_header = False
        for line in text.replace("\r\n", "\n").split("\n"):
            stripped = line.rstrip()
            if stripped == "0 HEAD":
                in_header = True
            elif stripped.startswith("0 "):
                in_header = False
            if in_header and stripped.startswith("1 DATE "):
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

    def test_normalizer_preserves_event_dates(self):
        text = (
            "0 HEAD\n"
            "1 DATE 10 JUL 2026\n"
            "0 @I1@ INDI\n"
            "1 BIRT\n"
            "2 DATE 10 JUL 2026\n"
            "0 TRLR\n"
        )
        normalized = self._normalize(text)
        self.assertIn("1 DATE [TODAY]", normalized)
        self.assertIn("2 DATE 10 JUL 2026", normalized)


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


class TestDeceasedBeforeInference(unittest.TestCase):
    """The cutoff applies only when every available date is bounded."""

    @staticmethod
    def _data(events):
        return {
            "individuals": [{
                "id": "I1", "given": "Unknown", "surname": "Person",
                "sex": "U", "events": events,
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }

    def test_undated_individual_remains_redacted(self):
        """A cutoff is not evidence that an undated person is deceased."""
        lines, report = _build(self._data([]), deceased_before=1600)
        self.assertEqual(len(report["redactions"]), 1)
        self.assertIn("[Living] /[Living]/", _ged_text(lines))

    def test_open_ended_dates_do_not_supply_upper_bound(self):
        for event_date in ("AFT 1800", "FROM 1800"):
            for kwargs in ({}, {"deceased_before": 1900}):
                with self.subTest(event_date=event_date, kwargs=kwargs):
                    data = self._data([{
                        "type": "BIRT", "date": event_date,
                    }])
                    lines, report = _build(data, **kwargs)
                    self.assertEqual(len(report["redactions"]), 1)
                    self.assertIn("[Living] /[Living]/", _ged_text(lines))

    def test_cutoff_requires_all_available_dates_bounded(self):
        data = self._data([
            {"type": "BIRT", "date": "1950"},
            {"type": "RESI", "date": "AFT 1980"},
        ])
        lines, report = _build(data, deceased_before=2000)
        self.assertEqual(len(report["redactions"]), 1)
        self.assertIn("[Living] /[Living]/", _ged_text(lines))

    def test_cutoff_unredacts_when_all_dates_are_bounded(self):
        data = self._data([
            {"type": "BIRT", "date": "1950"},
            {"type": "RESI", "date": "FROM 1970 TO 1980"},
        ])
        lines, report = _build(data, deceased_before=2000)
        self.assertEqual(report["redactions"], [])
        self.assertIn("Unknown /Person/", _ged_text(lines))

    def test_cutoff_does_not_unredact_latest_year_at_cutoff(self):
        data = {
            "individuals": [{
                "id": "I1", "given": "Boundary", "surname": "Person",
                "sex": "U", "events": [{"type": "BIRT", "date": "2000"}],
                "family_child": "", "family_spouse": [],
            }],
            "families": [], "sources": [], "repositories": [],
        }
        lines, report = _build(data, deceased_before=2000)
        self.assertEqual(len(report["redactions"]), 1)

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
    """Family details are private whenever any linked spouse is redacted."""

    def _family_data(self, spouse1_living, spouse2_living):
        def person(person_id, given, sex, living):
            events = ([{"type": "BIRT", "date": "1980"}]
                      if living else [{"type": "DEAT", "date": "2020"}])
            return {
                "id": person_id, "given": given, "surname": "Privacy",
                "sex": sex, "events": events,
                "family_child": "", "family_spouse": ["F1"],
            }

        return {
            "individuals": [
                person("I1", "Alex", "M", spouse1_living),
                person("I2", "Blair", "F", spouse2_living),
                {
                    "id": "I3", "given": "Casey", "surname": "Privacy",
                    "sex": "U", "events": [{"type": "DEAT", "date": "2021"}],
                    "family_child": "F1", "family_spouse": [],
                },
            ],
            "families": [{
                "id": "F1", "spouse1": "I1", "spouse2": "I2",
                "children": ["I3"],
                "events": [{
                    "type": "MARR", "date": "10 SEP 2015",
                    "place": "Richmond, Virginia", "source_id": "S1",
                    "source_page": "Private marriage citation",
                }],
                "source_citations": [{
                    "source_id": "S1", "source_page": "Private family citation",
                    "quality": 3,
                }],
                "notes": ["Private family note"],
            }],
            "sources": [{
                "id": "S1", "title": "Family source", "author": "",
                "publication": "", "repository_id": "", "notes": [],
            }],
            "repositories": [],
        }

    def _family_block(self, lines):
        ged = _ged_text(lines)
        return ged.split("0 @F1@ FAM")[1].split("\n0 ")[0]

    def _assert_private_details_absent(self, fam_block):
        self.assertNotIn("MARR", fam_block)
        self.assertNotIn("10 SEP 2015", fam_block)
        self.assertNotIn("Richmond, Virginia", fam_block)
        self.assertNotIn("Private family note", fam_block)
        self.assertNotIn("Private marriage citation", fam_block)
        self.assertNotIn("Private family citation", fam_block)
        self.assertNotIn("SOUR @S1@", fam_block)

    def _assert_private_details_present(self, fam_block):
        self.assertIn("MARR", fam_block)
        self.assertIn("10 SEP 2015", fam_block)
        self.assertIn("Richmond, Virginia", fam_block)
        self.assertIn("Private family note", fam_block)
        self.assertIn("Private marriage citation", fam_block)
        self.assertIn("Private family citation", fam_block)
        self.assertIn("SOUR @S1@", fam_block)

    def test_marr_stripped_when_both_spouses_living(self):
        """All private family details are suppressed for two living spouses."""
        data = self._family_data(True, True)
        data["individuals"][1]["sex"] = "M"
        lines, report = _build(data)
        self.assertEqual(len(report["redactions"]), 2)
        self.assertEqual(report["family_redactions"], ["F1"])
        fam_block = self._family_block(lines)
        self._assert_private_details_absent(fam_block)
        self.assertNotIn("positional assignment", fam_block)

    def test_mixed_family_suppresses_details_but_keeps_links(self):
        """One redacted spouse suppresses facts but not structural pointers."""
        data = self._family_data(False, True)
        lines, report = _build(data)
        self.assertEqual(len(report["redactions"]), 1)
        self.assertEqual(report["family_redactions"], ["F1"])
        fam_block = self._family_block(lines)
        self._assert_private_details_absent(fam_block)
        self.assertIn("HUSB @I1@", fam_block)
        self.assertIn("WIFE @I2@", fam_block)
        self.assertIn("CHIL @I3@", fam_block)

    def test_neither_spouse_living_keeps_family_details(self):
        """A fully deceased family retains events, notes, and citations."""
        data = self._family_data(False, False)
        lines, report = _build(data)
        self.assertEqual(report["redactions"], [])
        self.assertEqual(report["family_redactions"], [])
        self._assert_private_details_present(self._family_block(lines))

    def test_narrow_override_keeps_individual_redaction(self):
        """The private-use family override does not expose individual facts."""
        data = self._family_data(False, True)
        lines, report = _build(
            data, include_redacted_family_details=True,
        )
        self.assertEqual(len(report["redactions"]), 1)
        self.assertEqual(report["family_redactions"], [])
        self._assert_private_details_present(self._family_block(lines))
        i2_block = _ged_text(lines).split("0 @I2@ INDI")[1].split("\n0 ")[0]
        self.assertIn("[Living] /[Living]/", i2_block)
        self.assertNotIn("1980", i2_block)
        self.assertTrue(any("PRIVATE-USE OVERRIDE" in warning
                            for warning in report["warnings"]))

    def test_broad_overrides_include_all_details(self):
        """The existing all-data overrides continue to bypass redaction."""
        for kwargs in ({"include_living": True}, {"all_deceased": True}):
            with self.subTest(kwargs=kwargs):
                data = self._family_data(False, True)
                lines, report = _build(data, **kwargs)
                self.assertEqual(report["redactions"], [])
                self.assertEqual(report["family_redactions"], [])
                self._assert_private_details_present(self._family_block(lines))
                self.assertIn("Blair /Privacy/", _ged_text(lines))


class TestGlobalPrivacyFiltering(unittest.TestCase):
    """Suppressed citations cannot leak source or repository metadata."""

    @staticmethod
    def _data():
        return {
            "individuals": [
                {
                    "id": "I1", "given": "Living", "surname": "Person",
                    "sex": "U", "events": [{
                        "type": "BIRT", "date": "1980",
                        "source_id": "S_PRIVATE",
                        "source_page": "Private birth citation",
                    }],
                    "source_citations": [{
                        "source_id": "S_PRIVATE",
                        "source_page": "Private person citation",
                    }],
                    "family_child": "", "family_spouse": ["F1"],
                },
                {
                    "id": "I2", "given": "Deceased", "surname": "Person",
                    "sex": "U", "events": [{
                        "type": "DEAT", "date": "2020",
                        "source_id": "S_PUBLIC",
                        "source_page": "Public death citation",
                    }],
                    "family_child": "", "family_spouse": ["F1"],
                },
            ],
            "families": [{
                "id": "F1", "spouse1": "I1", "spouse2": "I2",
                "children": [],
                "events": [{
                    "type": "MARR", "date": "2005",
                    "source_id": "S_PRIVATE",
                    "source_page": "Private marriage citation",
                }],
                "source_citations": [{
                    "source_id": "S_PRIVATE",
                    "source_page": "Private family citation",
                }],
                "notes": [],
            }],
            "sources": [
                {
                    "id": "S_PRIVATE", "title": "Private source title",
                    "author": "Private source author",
                    "publication": "Private publication details",
                    "repository_id": "R_PRIVATE",
                    "notes": ["Private source note"],
                },
                {
                    "id": "S_PUBLIC", "title": "Retained source title",
                    "author": "", "publication": "",
                    "repository_id": "R_PUBLIC", "notes": [],
                },
                {
                    "id": "S_UNUSED", "title": "Unused source title",
                    "author": "", "publication": "",
                    "repository_id": "R_UNUSED", "notes": [],
                },
            ],
            "repositories": [
                {
                    "id": "R_PRIVATE", "name": "Private repository name",
                    "address": "Private repository address",
                },
                {
                    "id": "R_PUBLIC", "name": "Retained repository name",
                    "address": "Retained repository address",
                },
                {
                    "id": "R_UNUSED", "name": "Unused repository name",
                    "address": "Unused repository address",
                },
            ],
        }

    def test_whole_output_suppresses_unemitted_source_metadata(self):
        lines, report = _build(self._data())
        ged = _ged_text(lines)

        self.assertNotIn("0 @S_PRIVATE@ SOUR", ged)
        self.assertNotIn("Private source title", ged)
        self.assertNotIn("Private publication details", ged)
        self.assertNotIn("Private source note", ged)
        self.assertNotIn("0 @R_PRIVATE@ REPO", ged)
        self.assertNotIn("Private repository name", ged)
        self.assertNotIn("Private repository address", ged)
        self.assertNotIn("0 @S_UNUSED@ SOUR", ged)
        self.assertNotIn("0 @R_UNUSED@ REPO", ged)

        self.assertIn("0 @S_PUBLIC@ SOUR", ged)
        self.assertIn("Retained source title", ged)
        self.assertIn("0 @R_PUBLIC@ REPO", ged)
        self.assertEqual(report["sources"], 1)
        self.assertEqual(report["repositories"], 1)
        self.assertEqual(report["validation_errors"], [])

    def test_family_details_override_retains_required_source(self):
        lines, report = _build(
            self._data(), include_redacted_family_details=True,
        )
        ged = _ged_text(lines)
        self.assertIn("0 @S_PRIVATE@ SOUR", ged)
        self.assertIn("0 @R_PRIVATE@ REPO", ged)
        self.assertNotIn("0 @S_UNUSED@ SOUR", ged)
        self.assertNotIn("0 @R_UNUSED@ REPO", ged)
        self.assertEqual(report["sources"], 2)
        self.assertEqual(report["repositories"], 2)

    def test_shared_source_cited_by_living_and_deceased_is_suppressed(self):
        data = self._data()
        data["sources"].append({
            "id": "S_SHARED",
            "title": "Shared source contains private metadata",
            "author": "Private author",
            "publication": "Private publication",
            "repository_id": "R_SHARED",
            "notes": ["Private shared note"],
        })
        data["repositories"].append({
            "id": "R_SHARED",
            "name": "Private shared repository",
            "address": "Private shared address",
        })
        data["individuals"][0]["source_citations"].append({
            "source_id": "S_SHARED",
            "source_page": "Living-person page",
        })
        data["individuals"][1].setdefault("source_citations", []).append({
            "source_id": "S_SHARED",
            "source_page": "Deceased-person page",
        })

        lines, report = _build(data)
        ged = _ged_text(lines)

        self.assertNotIn("S_SHARED", ged)
        self.assertNotIn("Private shared", ged)
        self.assertNotIn("R_SHARED", ged)
        self.assertEqual(report["validation_errors"], [])


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
