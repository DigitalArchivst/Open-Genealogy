#!/usr/bin/env python3
"""
GEDCOM 5.5.1 Builder — Claude Code Skill Companion Script

License: MIT (this file only; see ../LICENSE)

Converts canonical JSON intermediate to valid GEDCOM 5.5.1 files.
The LLM parses user input into JSON; this script handles mechanics:
pointer wiring, CONC/CONT splitting, validation, and file output.

Usage:
    python gedcom_builder.py input.json --output family.ged --submitter "Jane Doe"
    python gedcom_builder.py input.json  # defaults to <surname>-family.ged
"""

import argparse
import json
import sys
import os
import re
from datetime import datetime, date
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_LINE_LENGTH = 255
MAX_VALUE_LENGTH = 248  # after level + space + tag + space
LIVING_THRESHOLD_YEARS = 110
CRLF = "\r\n"

VALID_INDI_EVENTS = {
    "BIRT", "DEAT", "BURI", "CHR", "BAPM", "RESI", "OCCU",
    "CENS", "IMMI", "EMIG", "NATU", "MILI", "PROB", "WILL", "ADOP",
}
VALID_FAM_EVENTS = {"MARR", "DIV"}

GEDCOM_MONTHS = {
    "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
    "JUL", "AUG", "SEP", "OCT", "NOV", "DEC",
}
GEDCOM_DATE_QUALIFIERS = {"ABT", "BEF", "AFT", "CAL", "EST"}
GEDCOM_YEAR_PATTERN = re.compile(r"^[0-9]{3,4}(?:/[0-9]{2})?$")
GEDCOM_XREF_ID_PATTERN = re.compile(r"^[A-Za-z0-9_]{1,20}$")
GEDCOM_SOURCE_POINTER_PATTERN = re.compile(
    r"^[0-9]+ SOUR @([A-Za-z0-9_]{1,20})@$"
)

HEADER_TEMPLATE = (
    "0 HEAD\r\n"
    "1 SOUR CLAUDE_CODE_GEDCOM\r\n"
    "2 VERS 1.0\r\n"
    "2 NAME Claude Code GEDCOM Skill\r\n"
    "1 DEST ANY\r\n"
    "1 DATE {date}\r\n"
    "1 GEDC\r\n"
    "2 VERS 5.5.1\r\n"
    "2 FORM LINEAGE-LINKED\r\n"
    "1 CHAR UTF-8\r\n"
    "1 LANG English\r\n"
    "1 SUBM @U1@\r\n"
    "0 @U1@ SUBM\r\n"
    "1 NAME {submitter}\r\n"
)


# ---------------------------------------------------------------------------
# CONC/CONT line splitting — character-boundary safe
# ---------------------------------------------------------------------------

def split_long_value(level, tag, value):
    """Split a GEDCOM value across CONC lines if it exceeds MAX_VALUE_LENGTH.

    Splits at character boundaries only — never mid-multibyte UTF-8.
    Prefers splitting at spaces when possible.
    Returns a list of GEDCOM lines (without line terminators).
    """
    first_line = f"{level} {tag} "
    overhead = len(first_line.encode("utf-8"))

    # If the whole thing fits, just return it
    full_line = f"{level} {tag} {value}"
    if len(full_line.encode("utf-8")) <= MAX_LINE_LENGTH:
        return [full_line]

    lines = []
    remaining = value
    is_first = True

    while remaining:
        if is_first:
            prefix = f"{level} {tag} "
            is_first = False
        else:
            prefix = f"{level + 1} CONC "

        budget = MAX_LINE_LENGTH - len(prefix.encode("utf-8"))

        # Find the split point: largest substring that fits in budget bytes
        split_at = 0
        last_space = -1
        byte_count = 0
        for i, ch in enumerate(remaining):
            ch_bytes = len(ch.encode("utf-8"))
            if byte_count + ch_bytes > budget:
                break
            byte_count += ch_bytes
            split_at = i + 1
            if ch == " ":
                last_space = i + 1

        # Prefer splitting at a space if we found one in the last 20% of budget
        if last_space > split_at * 0.8:
            split_at = last_space

        chunk = remaining[:split_at]
        remaining = remaining[split_at:]
        lines.append(f"{prefix}{chunk}")

    return lines


def split_note_value(level, tag, value):
    """Split a note value into GEDCOM lines, preserving paragraph breaks as CONT.

    Embedded newlines become CONT lines (preserving paragraph structure).
    Long lines within a paragraph are split via CONC as usual.
    Returns a list of GEDCOM lines (without line terminators).
    """
    if "\n" not in value:
        return split_long_value(level, tag, value)

    paragraphs = value.split("\n")
    lines = []
    for i, para in enumerate(paragraphs):
        if i == 0:
            lines.extend(split_long_value(level, tag, para))
        else:
            # CONT preserves the line break
            if para:
                lines.extend(split_long_value(level + 1, "CONT", para))
            else:
                # Empty paragraph = blank CONT line
                lines.append(f"{level + 1} CONT")
    return lines


# ---------------------------------------------------------------------------
# Sanitization
# ---------------------------------------------------------------------------

def sanitize_value(value, preserve_newlines=False):
    """Strip characters that could corrupt GEDCOM structure.

    When preserve_newlines is True, embedded newlines are kept so
    they can be emitted as CONT lines (GEDCOM §5.4).
    """
    if not value:
        return ""
    if preserve_newlines:
        # Normalize to \n only, strip trailing whitespace per line
        value = value.replace("\r\n", "\n").replace("\r", "\n")
        lines = [line.rstrip() for line in value.split("\n")]
        return "\n".join(lines).strip()
    # Default: flatten to single line
    value = value.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    value = value.rstrip()
    return value


# ---------------------------------------------------------------------------
# Canonical GEDCOM date validation
# ---------------------------------------------------------------------------

def _is_simple_gedcom_date(tokens):
    """Validate DATE, DATE_MONTH, or DATE_YEAR tokens lexically."""
    if len(tokens) == 1:
        return bool(GEDCOM_YEAR_PATTERN.fullmatch(tokens[0]))
    if len(tokens) == 2:
        month, year = tokens
        return (month in GEDCOM_MONTHS
                and bool(GEDCOM_YEAR_PATTERN.fullmatch(year)))
    if len(tokens) == 3:
        day, month, year = tokens
        return (day.isascii() and day.isdigit() and 1 <= int(day) <= 31
                and month in GEDCOM_MONTHS
                and bool(GEDCOM_YEAR_PATTERN.fullmatch(year)))
    return False


def is_valid_gedcom_date(value):
    """Return True for the canonical GEDCOM date forms this tool accepts.

    Accepted forms are a simple date, a qualified simple date, a
    BET...AND range, or a FROM/TO period. This is lexical validation;
    it does not decide whether a calendar date such as 31 FEB existed.
    """
    if not isinstance(value, str) or not value:
        return False
    if value != " ".join(value.split()):
        return False

    tokens = value.split(" ")
    if _is_simple_gedcom_date(tokens):
        return True

    if tokens[0] in GEDCOM_DATE_QUALIFIERS:
        return _is_simple_gedcom_date(tokens[1:])

    if tokens[0] == "BET":
        if tokens.count("AND") != 1:
            return False
        separator = tokens.index("AND")
        return (_is_simple_gedcom_date(tokens[1:separator])
                and _is_simple_gedcom_date(tokens[separator + 1:]))

    if tokens[0] == "FROM":
        if "TO" not in tokens:
            return _is_simple_gedcom_date(tokens[1:])
        if tokens.count("TO") != 1:
            return False
        separator = tokens.index("TO")
        return (_is_simple_gedcom_date(tokens[1:separator])
                and _is_simple_gedcom_date(tokens[separator + 1:]))

    if tokens[0] == "TO":
        return _is_simple_gedcom_date(tokens[1:])

    return False


# ---------------------------------------------------------------------------
# Living person detection
# ---------------------------------------------------------------------------

DEATH_INDICATORS = {"DEAT", "BURI", "PROB"}
# WILL is intentionally excluded: a living person may draft a will.
# PROB (probate) remains because probate follows death in all jurisdictions.
# Historical wills without PROB are caught by any-event date inference.

# Minimum plausible age for non-birth events (for era inference)
EVENT_MIN_AGE = {
    "BIRT": 0, "BAPM": 0, "CHR": 0, "DEAT": 0, "BURI": 0,
    "RESI": 0, "CENS": 0, "ADOP": 0, "IMMI": 0, "EMIG": 0,
    "OCCU": 15, "MILI": 15, "NATU": 15,
    "MARR": 14, "WILL": 18, "PROB": 18,
}


def is_presumed_living(individual):
    """Determine if an individual should be treated as living.

    Conservative default: presume living unless death is confirmed
    or all evidence places the person in a historical era.
    """
    # Step 1: Death-indicating events (DEAT, BURI, PROB)
    for event in individual.get("events", []):
        if event.get("type") in DEATH_INDICATORS:
            return False

    # Step 2: Birth year check (BIRT, BAPM, CHR)
    birth_year = _extract_year(individual)
    if birth_year:
        current_year = date.today().year
        if current_year - birth_year >= LIVING_THRESHOLD_YEARS:
            return False

    # Step 3: Any-event date inference
    latest_birth = _extract_latest_plausible_birth_year(individual)
    if latest_birth:
        current_year = date.today().year
        if current_year - latest_birth >= LIVING_THRESHOLD_YEARS:
            return False

    # No death evidence, and either young enough or no dates at all
    return True


def _extract_year(individual):
    """Extract birth year from an individual's events.

    Checks BIRT first, then BAPM and CHR as proxies (common in parish
    register data where baptism is the only recorded birth-adjacent event).
    """
    for etype in ("BIRT", "BAPM", "CHR"):
        for event in individual.get("events", []):
            if event.get("type") == etype and event.get("date"):
                return _date_upper_bound_year(event["date"])
    return None


def _extract_latest_plausible_birth_year(individual):
    """Estimate the latest possible birth year from ANY dated event.

    For each dated event, subtract the minimum plausible age for that
    event type. Return the earliest result (most conservative).
    E.g., OCCU in 1794 -> born no later than 1779.
    """
    latest_birth = None
    for event in individual.get("events", []):
        etype = event.get("type", "")
        year = _date_upper_bound_year(event.get("date", ""))
        if year is None:
            continue
        min_age = EVENT_MIN_AGE.get(etype, 0)
        implied_birth = year - min_age
        if latest_birth is None or implied_birth < latest_birth:
            latest_birth = implied_birth
    return latest_birth


def _get_latest_bounded_event_year(individual):
    """Return the latest event upper bound, or None if any date is open."""
    bounded_years = []
    for event in individual.get("events", []):
        event_date = event.get("date", "")
        if not event_date:
            continue
        year = _date_upper_bound_year(event_date)
        if year is None:
            return None
        bounded_years.append(year)
    return max(bounded_years) if bounded_years else None


def _simple_date_year(tokens):
    """Return the latest year represented by a simple GEDCOM date."""
    if not tokens:
        return None
    year_token = tokens[-1]
    if "/" not in year_token:
        try:
            return int(year_token)
        except (TypeError, ValueError):
            return None

    first_year, second_suffix = year_token.split("/", 1)
    try:
        first_year = int(first_year)
        second_year = ((first_year // 100) * 100) + int(second_suffix)
    except (TypeError, ValueError):
        return None
    if second_year < first_year:
        second_year += 100
    return max(first_year, second_year)


def _date_upper_bound_year(date_str):
    """Return a finite upper-bound year for a GEDCOM date when available."""
    if not isinstance(date_str, str) or not date_str:
        return None

    tokens = date_str.split()
    if tokens[0] == "AFT":
        return None
    if tokens[0] == "FROM":
        if "TO" not in tokens:
            return None
        return _simple_date_year(tokens[tokens.index("TO") + 1:])
    if tokens[0] == "BET":
        if "AND" not in tokens:
            return None
        return _simple_date_year(tokens[tokens.index("AND") + 1:])
    if tokens[0] == "TO":
        return _simple_date_year(tokens[1:])
    if tokens[0] == "BEF":
        year = _simple_date_year(tokens[1:])
        if year is not None and len(tokens) == 2 and "/" not in tokens[1]:
            return year - 1
        return year
    if tokens[0] in {"ABT", "CAL", "EST"}:
        return _simple_date_year(tokens[1:])
    return _simple_date_year(tokens)


def _parse_year_from_date(date_str):
    """Extract the numeric year from a GEDCOM date string."""
    if not date_str:
        return None
    # Strip prefixes
    parts = date_str.replace("/", " ").split()
    for part in reversed(parts):
        try:
            year = int(part)
            if 1000 <= year <= 2100:
                return year
        except ValueError:
            continue
    return None


# ---------------------------------------------------------------------------
# GEDCOM record builders
# ---------------------------------------------------------------------------

def build_indi_record(ind, living_ids, sources_map, suppressed_source_ids=None):
    """Build a GEDCOM INDI record from the canonical JSON."""
    lines = []
    suppressed_source_ids = suppressed_source_ids or set()
    xref = f"@{ind['id']}@"
    lines.append(f"0 {xref} INDI")

    is_living = ind["id"] in living_ids

    # NAME
    if is_living:
        lines.append("1 NAME [Living] /[Living]/")
        lines.append("2 GIVN [Living]")
        lines.append("2 SURN [Living]")
    else:
        given = sanitize_value(ind.get("given", ""))
        surname = sanitize_value(ind.get("surname", ""))
        prefix = sanitize_value(ind.get("prefix", ""))
        suffix = sanitize_value(ind.get("suffix", ""))
        nickname = sanitize_value(ind.get("nickname", ""))

        name_str = f"{given} /{surname}/" if given else f"/{surname}/"
        if suffix:
            name_str += f" {suffix}"
        lines.extend(split_long_value(1, "NAME", name_str))
        if given:
            lines.append(f"2 GIVN {given}")
        if surname:
            lines.append(f"2 SURN {surname}")
        if prefix:
            lines.append(f"2 NPFX {prefix}")
        if suffix:
            lines.append(f"2 NSFX {suffix}")
        if nickname:
            lines.append(f"2 NICK {nickname}")

    # SEX
    sex = ind.get("sex", "U")
    if sex not in ("M", "F", "U"):
        sex = "U"
    lines.append(f"1 SEX {sex}")

    # Events (strip all events for living persons)
    for event in ind.get("events", []):
        etype = event.get("type", "")
        if etype not in VALID_INDI_EVENTS:
            continue
        if is_living:
            continue

        edate = sanitize_value(event.get("date", ""))
        eplace = sanitize_value(event.get("place", ""))

        # Don't emit empty event containers
        if not edate and not eplace:
            continue

        lines.append(f"1 {etype}")
        if edate:
            lines.extend(split_long_value(2, "DATE", edate))
        if eplace:
            lines.extend(split_long_value(2, "PLAC", eplace))

        # Inline source citation
        src_id = event.get("source_id", "")
        if (src_id and not is_living
                and src_id not in suppressed_source_ids):
            lines.append(f"2 SOUR @{src_id}@")
            src_page = sanitize_value(event.get("source_page", ""))
            if src_page:
                lines.extend(split_long_value(3, "PAGE", src_page))

    # FAMC
    famc = ind.get("family_child", "")
    if famc:
        lines.append(f"1 FAMC @{famc}@")
        pedi = ind.get("family_child_pedi", "")
        if pedi and pedi in ("birth", "adopted", "foster"):
            lines.append(f"2 PEDI {pedi}")

    # FAMS
    for fams in ind.get("family_spouse", []):
        if fams:
            lines.append(f"1 FAMS @{fams}@")

    # Notes (skip for living)
    if not is_living:
        for note in ind.get("notes", []):
            note = sanitize_value(note, preserve_newlines=True)
            if note:
                lines.extend(split_note_value(1, "NOTE", note))

    # Individual-level source citations (non-event)
    if not is_living:
        for src_ref in ind.get("source_citations", []):
            src_id = src_ref.get("source_id", "")
            if src_id and src_id not in suppressed_source_ids:
                lines.append(f"1 SOUR @{src_id}@")
                page = sanitize_value(src_ref.get("source_page", ""))
                if page:
                    lines.extend(split_long_value(2, "PAGE", page))
                quay = src_ref.get("quality", "")
                if quay in (0, 1, 2, 3, "0", "1", "2", "3"):
                    lines.append(f"2 QUAY {quay}")

    return lines


def build_fam_record(fam, ind_map=None, living_ids=None,
                     include_redacted_family_details=False,
                     suppressed_source_ids=None):
    """Build a GEDCOM FAM record from the canonical JSON.

    Uses sex fields from ind_map (if provided) to guide HUSB/WIFE
    assignment. GEDCOM 5.5.1 only defines HUSB and WIFE — there is
    no gender-neutral spouse tag. When sex doesn't match the assigned
    tag, a NOTE documents the limitation.

    When any linked spouse is in living_ids, family events, notes, and
    citations are stripped unless the private-use override is enabled.
    Spouse and child links are always retained for structural validity.
    """
    lines = []
    suppressed_source_ids = suppressed_source_ids or set()
    xref = f"@{fam['id']}@"
    lines.append(f"0 {xref} FAM")

    sp1 = fam.get("spouse1", "")
    sp2 = fam.get("spouse2", "")
    ind_map = ind_map or {}
    living_ids = living_ids or set()
    spouses = [spouse for spouse in (sp1, sp2) if spouse]
    has_redacted_spouse = any(spouse in living_ids for spouse in spouses)
    suppress_family_details = (
        has_redacted_spouse and not include_redacted_family_details
    )

    # Determine HUSB/WIFE assignment using sex fields when available
    sp1_sex = ind_map.get(sp1, {}).get("sex", "U") if sp1 else "U"
    sp2_sex = ind_map.get(sp2, {}).get("sex", "U") if sp2 else "U"

    # Default: sp1=HUSB, sp2=WIFE. Swap if sex fields indicate otherwise.
    sp1_tag, sp2_tag = "HUSB", "WIFE"
    sex_note = None
    if sp1 and sp2:
        if sp1_sex == "F" and sp2_sex == "M":
            sp1_tag, sp2_tag = "WIFE", "HUSB"
        elif sp1_sex == sp2_sex and sp1_sex in ("M", "F"):
            sex_note = (f"GEDCOM 5.5.1 requires HUSB/WIFE tags. "
                        f"Both spouses have SEX {sp1_sex}; positional "
                        f"assignment used. No gender assumption intended.")

    if sp1:
        lines.append(f"1 {sp1_tag} @{sp1}@")
    if sp2:
        lines.append(f"1 {sp2_tag} @{sp2}@")
    if sex_note and not suppress_family_details:
        lines.extend(split_long_value(1, "NOTE", sex_note))

    for child_id in fam.get("children", []):
        if child_id:
            lines.append(f"1 CHIL @{child_id}@")

    for event in fam.get("events", []):
        etype = event.get("type", "")
        if etype not in VALID_FAM_EVENTS:
            continue
        if suppress_family_details:
            continue

        edate = sanitize_value(event.get("date", ""))
        eplace = sanitize_value(event.get("place", ""))

        if not edate and not eplace:
            continue

        lines.append(f"1 {etype}")
        if edate:
            lines.extend(split_long_value(2, "DATE", edate))
        if eplace:
            lines.extend(split_long_value(2, "PLAC", eplace))

        src_id = event.get("source_id", "")
        if src_id and src_id not in suppressed_source_ids:
            lines.append(f"2 SOUR @{src_id}@")
            src_page = sanitize_value(event.get("source_page", ""))
            if src_page:
                lines.extend(split_long_value(3, "PAGE", src_page))

    if not suppress_family_details:
        for note in fam.get("notes", []):
            note = sanitize_value(note, preserve_newlines=True)
            if note:
                lines.extend(split_note_value(1, "NOTE", note))

    # Family-level source citations (e.g., wills establishing relationships)
    if not suppress_family_details:
        for src_ref in fam.get("source_citations", []):
            src_id = src_ref.get("source_id", "")
            if src_id and src_id not in suppressed_source_ids:
                lines.append(f"1 SOUR @{src_id}@")
                page = sanitize_value(src_ref.get("source_page", ""))
                if page:
                    lines.extend(split_long_value(2, "PAGE", page))
                quay = src_ref.get("quality", "")
                if quay in (0, 1, 2, 3, "0", "1", "2", "3"):
                    lines.append(f"2 QUAY {quay}")

    return lines


def build_sour_record(source):
    """Build a GEDCOM SOUR record from the canonical JSON."""
    lines = []
    xref = f"@{source['id']}@"
    lines.append(f"0 {xref} SOUR")

    title = sanitize_value(source.get("title", ""))
    if title:
        lines.extend(split_long_value(1, "TITL", title))

    author = sanitize_value(source.get("author", ""))
    if author:
        lines.extend(split_long_value(1, "AUTH", author))

    publ = sanitize_value(source.get("publication", ""))
    if publ:
        lines.extend(split_long_value(1, "PUBL", publ))

    repo_id = source.get("repository_id", "")
    if repo_id:
        lines.append(f"1 REPO @{repo_id}@")

    for note in source.get("notes", []):
        note = sanitize_value(note, preserve_newlines=True)
        if note:
            lines.extend(split_note_value(1, "NOTE", note))

    return lines


def collect_sensitive_source_ids(data, living_ids):
    """Find sources cited by records containing living-person data."""
    sensitive = set()

    for ind in data.get("individuals", []):
        if ind.get("id") not in living_ids:
            continue
        for event in ind.get("events", []):
            if event.get("source_id"):
                sensitive.add(event["source_id"])
        for citation in ind.get("source_citations", []):
            if citation.get("source_id"):
                sensitive.add(citation["source_id"])

    for fam in data.get("families", []):
        member_ids = [fam.get(role, "") for role in ("spouse1", "spouse2")]
        member_ids.extend(fam.get("children", []))
        if not any(member_id in living_ids for member_id in member_ids):
            continue
        for event in fam.get("events", []):
            if event.get("source_id"):
                sensitive.add(event["source_id"])
        for citation in fam.get("source_citations", []):
            if citation.get("source_id"):
                sensitive.add(citation["source_id"])

    return sensitive


def build_repo_record(repo):
    """Build a GEDCOM REPO record from the canonical JSON."""
    lines = []
    xref = f"@{repo['id']}@"
    lines.append(f"0 {xref} REPO")

    name = sanitize_value(repo.get("name", ""))
    if name:
        lines.extend(split_long_value(1, "NAME", name))

    addr = sanitize_value(repo.get("address", ""))
    if addr:
        lines.extend(split_long_value(1, "ADDR", addr))

    return lines


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class ValidationError:
    def __init__(self, code, message, severity="ERROR"):
        self.code = code
        self.message = message
        self.severity = severity

    def __str__(self):
        return f"[{self.severity}] {self.code}: {self.message}"


def validate_identifiers(data):
    """Reject malformed or duplicate record IDs before graph processing."""
    errors = []
    seen = {"U1": "generated submitter record"}

    for collection in ("individuals", "families", "sources", "repositories"):
        for index, record in enumerate(data.get(collection, [])):
            record_id = record.get("id")
            location = f"{collection}[{index}]"
            if (not isinstance(record_id, str)
                    or not GEDCOM_XREF_ID_PATTERN.fullmatch(record_id)):
                errors.append(ValidationError(
                    "MALFORMED_ID",
                    f"{location} has invalid ID {record_id!r}; use 1-20 "
                    "ASCII letters, digits, or underscores without @ signs"
                ))
            if isinstance(record_id, str):
                if record_id in seen:
                    errors.append(ValidationError(
                        "DUPLICATE_ID",
                        f"{location} reuses ID {record_id!r} already used by "
                        f"{seen[record_id]}"
                    ))
                else:
                    seen[record_id] = location

    return errors


def validate_dates(data):
    """Validate every non-empty individual and family event date."""
    errors = []
    for collection in ("individuals", "families"):
        for record in data.get(collection, []):
            record_id = record.get("id", "<missing ID>")
            for event_index, event in enumerate(record.get("events", [])):
                event_date = event.get("date", "")
                if event_date != "" and not is_valid_gedcom_date(event_date):
                    errors.append(ValidationError(
                        "INVALID_DATE",
                        f"{record_id} event {event_index + 1} has unsupported "
                        f"date {event_date!r}"
                    ))
    return errors


def _append_pointer_error(errors, owner, field, reference, target_ids):
    """Append one lexical or resolution error for a pointer value."""
    if reference == "":
        return
    if (not isinstance(reference, str)
            or not GEDCOM_XREF_ID_PATTERN.fullmatch(reference)):
        errors.append(ValidationError(
            "MALFORMED_POINTER",
            f"{owner} {field} has invalid pointer target {reference!r}"
        ))
    elif reference not in target_ids:
        errors.append(ValidationError(
            "DANGLING_POINTER",
            f"{owner} {field} references {reference} which does not exist"
        ))


def validate(data, gedcom_lines):
    """Run all validation checks. Returns list of ValidationError."""
    identifier_errors = validate_identifiers(data)
    if identifier_errors:
        return identifier_errors

    errors = validate_dates(data)

    indi_ids = {ind["id"] for ind in data.get("individuals", [])}
    fam_ids = {fam["id"] for fam in data.get("families", [])}
    sour_ids = {s["id"] for s in data.get("sources", [])}
    repo_ids = {r["id"] for r in data.get("repositories", [])}

    # --- Pointer resolution ---
    for ind in data.get("individuals", []):
        famc = ind.get("family_child", "")
        _append_pointer_error(
            errors, ind["id"], "family_child", famc, fam_ids,
        )
        for fams in ind.get("family_spouse", []):
            _append_pointer_error(
                errors, ind["id"], "family_spouse", fams, fam_ids,
            )
        for event in ind.get("events", []):
            src = event.get("source_id", "")
            _append_pointer_error(
                errors, ind["id"], "event source_id", src, sour_ids,
            )
        for src_ref in ind.get("source_citations", []):
            src = src_ref.get("source_id", "")
            _append_pointer_error(
                errors, ind["id"], "source_citation source_id", src, sour_ids,
            )

    for fam in data.get("families", []):
        for role in ("spouse1", "spouse2"):
            ref = fam.get(role, "")
            _append_pointer_error(
                errors, f"Family {fam['id']}", role, ref, indi_ids,
            )
        for child in fam.get("children", []):
            _append_pointer_error(
                errors, f"Family {fam['id']}", "child", child, indi_ids,
            )
        for event in fam.get("events", []):
            src = event.get("source_id", "")
            _append_pointer_error(
                errors, f"Family {fam['id']}", "event source_id", src,
                sour_ids,
            )

    for src in data.get("sources", []):
        repo = src.get("repository_id", "")
        _append_pointer_error(
            errors, f"Source {src['id']}", "repository_id", repo, repo_ids,
        )

    # --- Bidirectional pointer consistency ---
    for ind in data.get("individuals", []):
        famc = ind.get("family_child", "")
        if famc:
            fam_obj = _find_by_id(data.get("families", []), famc)
            if fam_obj and ind["id"] not in fam_obj.get("children", []):
                errors.append(ValidationError(
                    "BIDIRECTIONAL_MISMATCH",
                    f"{ind['id']} has FAMC={famc} but family {famc} does not list {ind['id']} as CHIL"
                ))
        for fams in ind.get("family_spouse", []):
            if fams:
                fam_obj = _find_by_id(data.get("families", []), fams)
                if fam_obj:
                    if ind["id"] not in (fam_obj.get("spouse1", ""), fam_obj.get("spouse2", "")):
                        errors.append(ValidationError(
                            "BIDIRECTIONAL_MISMATCH",
                            f"{ind['id']} has FAMS={fams} but family {fams} does not list {ind['id']} as spouse"
                        ))

    for fam in data.get("families", []):
        for src_ref in fam.get("source_citations", []):
            src = src_ref.get("source_id", "")
            _append_pointer_error(
                errors, f"Family {fam['id']}",
                "source_citation source_id", src, sour_ids,
            )
        for child in fam.get("children", []):
            if child:
                ind_obj = _find_by_id(data.get("individuals", []), child)
                if ind_obj and ind_obj.get("family_child", "") != fam["id"]:
                    errors.append(ValidationError(
                        "BIDIRECTIONAL_MISMATCH",
                        f"Family {fam['id']} lists {child} as CHIL but {child} FAMC is {ind_obj.get('family_child', 'empty')}"
                    ))
        for role in ("spouse1", "spouse2"):
            sp = fam.get(role, "")
            if sp:
                ind_obj = _find_by_id(data.get("individuals", []), sp)
                if ind_obj and fam["id"] not in ind_obj.get("family_spouse", []):
                    errors.append(ValidationError(
                        "BIDIRECTIONAL_MISMATCH",
                        f"Family {fam['id']} lists {sp} as {role} but {sp} does not have FAMS={fam['id']}"
                    ))

    # --- Cycle detection ---
    parent_map = {}
    for ind in data.get("individuals", []):
        famc = ind.get("family_child", "")
        if famc:
            fam_obj = _find_by_id(data.get("families", []), famc)
            if fam_obj:
                parents = []
                if fam_obj.get("spouse1"):
                    parents.append(fam_obj["spouse1"])
                if fam_obj.get("spouse2"):
                    parents.append(fam_obj["spouse2"])
                parent_map[ind["id"]] = parents

    finished = set()
    active_path = []
    active_nodes = set()

    def find_cycle(node):
        if node in active_nodes:
            cycle_start = active_path.index(node)
            return active_path[cycle_start:] + [node]
        if node in finished:
            return None

        active_path.append(node)
        active_nodes.add(node)
        for parent in parent_map.get(node, []):
            cycle = find_cycle(parent)
            if cycle:
                return cycle
        active_path.pop()
        active_nodes.remove(node)
        finished.add(node)
        return None

    for ind_id in parent_map:
        cycle = find_cycle(ind_id)
        if cycle:
            errors.append(ValidationError(
                "CYCLE_DETECTED",
                "Circular parent-child relationship: " + " -> ".join(cycle)
            ))
            break

    # --- Line length check ---
    for i, line in enumerate(gedcom_lines):
        line_bytes = len(line.encode("utf-8"))
        if line_bytes > MAX_LINE_LENGTH:
            errors.append(ValidationError(
                "LINE_TOO_LONG",
                f"Line {i+1} is {line_bytes} bytes (max {MAX_LINE_LENGTH}): {line[:60]}..."
            ))

    # --- HEAD/TRLR presence ---
    if not gedcom_lines or not gedcom_lines[0].startswith("0 HEAD"):
        errors.append(ValidationError("MISSING_HEAD", "File does not begin with 0 HEAD"))
    if not gedcom_lines or not gedcom_lines[-1].startswith("0 TRLR"):
        errors.append(ValidationError("MISSING_TRLR", "File does not end with 0 TRLR"))

    return errors


def _find_by_id(records, target_id):
    """Find a record by its id field."""
    for rec in records:
        if rec.get("id") == target_id:
            return rec
    return None


# ---------------------------------------------------------------------------
# Auto-repair bidirectional pointers
# ---------------------------------------------------------------------------

def auto_repair_pointers(data):
    """Ensure bidirectional consistency between INDI and FAM records."""
    ind_map = {ind["id"]: ind for ind in data.get("individuals", [])}
    fam_map = {fam["id"]: fam for fam in data.get("families", [])}
    repairs = []

    for fam in data.get("families", []):
        for child_id in fam.get("children", []):
            if child_id in ind_map:
                ind = ind_map[child_id]
                if ind.get("family_child", "") != fam["id"]:
                    ind["family_child"] = fam["id"]
                    repairs.append(f"Set {child_id} FAMC={fam['id']}")

        for role in ("spouse1", "spouse2"):
            sp_id = fam.get(role, "")
            if sp_id and sp_id in ind_map:
                ind = ind_map[sp_id]
                spouse_list = ind.get("family_spouse", [])
                if fam["id"] not in spouse_list:
                    spouse_list.append(fam["id"])
                    ind["family_spouse"] = spouse_list
                    repairs.append(f"Added {fam['id']} to {sp_id} FAMS")

    for ind in data.get("individuals", []):
        famc = ind.get("family_child", "")
        if famc and famc in fam_map:
            fam = fam_map[famc]
            if ind["id"] not in fam.get("children", []):
                fam.setdefault("children", []).append(ind["id"])
                repairs.append(f"Added {ind['id']} to {famc} CHIL")

        for fams_id in ind.get("family_spouse", []):
            if fams_id and fams_id in fam_map:
                fam = fam_map[fams_id]
                if ind["id"] not in (fam.get("spouse1", ""), fam.get("spouse2", "")):
                    if not fam.get("spouse1"):
                        fam["spouse1"] = ind["id"]
                        repairs.append(f"Set {fams_id} spouse1={ind['id']}")
                    elif not fam.get("spouse2"):
                        fam["spouse2"] = ind["id"]
                        repairs.append(f"Set {fams_id} spouse2={ind['id']}")
                    else:
                        repairs.append(
                            f"WARNING: Cannot assign {ind['id']} as spouse "
                            f"in {fams_id} — both spouse slots filled"
                        )

    return repairs


# ---------------------------------------------------------------------------
# Multi-file merge
# ---------------------------------------------------------------------------

def merge_json_files(paths):
    """Merge multiple canonical JSON files into one dataset.

    Returns (merged_data, warnings) where warnings is a list of strings.
    """
    merged = {
        "submitter": "",
        "individuals": [],
        "families": [],
        "sources": [],
        "repositories": [],
    }
    seen_ids = set()
    warnings = []

    for path in paths:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not merged["submitter"] and data.get("submitter"):
            merged["submitter"] = data["submitter"]

        for key in ("individuals", "families", "sources", "repositories"):
            for record in data.get(key, []):
                rid = record.get("id", "")
                if rid in seen_ids:
                    raise ValueError(
                        f"Duplicate ID {rid!r} encountered while merging {path}"
                    )
                seen_ids.add(rid)
                merged[key].append(record)

    return merged, warnings


# ---------------------------------------------------------------------------
# Main build pipeline
# ---------------------------------------------------------------------------

def build_gedcom(data, submitter="Unknown", include_living=False,
                 all_deceased=False, deceased_before=None,
                 include_redacted_family_details=False):
    """Build complete GEDCOM 5.5.1 from canonical JSON data."""
    report = {
        "individuals": 0, "families": 0, "sources": 0, "repositories": 0,
        "redactions": [], "family_redactions": [], "repairs": [],
        "validation_errors": [], "warnings": [],
    }

    identifier_errors = validate_identifiers(data)
    if identifier_errors:
        report["validation_errors"] = [str(e) for e in identifier_errors]
        return [], report

    date_errors = validate_dates(data)
    if date_errors:
        report["validation_errors"] = [str(e) for e in date_errors]
        return [], report

    repairs = auto_repair_pointers(data)
    report["repairs"] = repairs

    living_ids = set()
    skip_redaction = include_living or all_deceased
    if not skip_redaction:
        for ind in data.get("individuals", []):
            if is_presumed_living(ind):
                # Check --deceased-before override
                if deceased_before is not None:
                    latest_yr = _get_latest_bounded_event_year(ind)
                    if (latest_yr is not None
                            and latest_yr < deceased_before):
                        continue  # Events are historical — don't redact
                living_ids.add(ind["id"])
                name = f"{ind.get('given', '')} {ind.get('surname', '')}".strip()
                birth_year = _extract_year(ind)
                reason = "no death date"
                if birth_year:
                    reason += f", born {birth_year}"
                else:
                    reason += ", no birth date"
                report["redactions"].append({
                    "id": ind["id"], "name": name, "reason": reason,
                })

    today = datetime.now().strftime("%d %b %Y").lstrip("0").upper()
    header_text = HEADER_TEMPLATE.format(
        date=today, submitter=sanitize_value(submitter),
    )
    lines = [line for line in header_text.rstrip(CRLF).split(CRLF)]

    sources_map = {s["id"]: s for s in data.get("sources", [])}
    sensitive_source_ids = collect_sensitive_source_ids(data, living_ids)
    suppressed_source_ids = (
        sensitive_source_ids if not include_redacted_family_details else set()
    )
    ind_map = {ind["id"]: ind for ind in data.get("individuals", [])}

    for ind in data.get("individuals", []):
        lines.extend(build_indi_record(
            ind, living_ids, sources_map, suppressed_source_ids
        ))
        report["individuals"] += 1

    for fam in data.get("families", []):
        linked_spouses = [
            fam.get(role, "") for role in ("spouse1", "spouse2")
            if fam.get(role, "")
        ]
        has_redacted_spouse = any(
            spouse in living_ids for spouse in linked_spouses
        )
        if has_redacted_spouse and not include_redacted_family_details:
            report["family_redactions"].append(fam["id"])
        lines.extend(build_fam_record(
            fam,
            ind_map,
            living_ids,
            include_redacted_family_details=include_redacted_family_details,
            suppressed_source_ids=suppressed_source_ids,
        ))
        report["families"] += 1

    if include_redacted_family_details and any(
            any(fam.get(role, "") in living_ids
                for role in ("spouse1", "spouse2"))
            for fam in data.get("families", [])):
        report["warnings"].append(
            "PRIVATE-USE OVERRIDE: family events, notes, and citations "
            "linked to redacted people were included and may identify them."
        )

    referenced_source_ids = set()
    for line in lines:
        match = GEDCOM_SOURCE_POINTER_PATTERN.fullmatch(line)
        if match:
            referenced_source_ids.add(match.group(1))

    retained_sources = [
        source for source in data.get("sources", [])
        if (source["id"] in referenced_source_ids
                and source["id"] not in suppressed_source_ids)
    ]
    retained_repo_ids = {
        source.get("repository_id", "") for source in retained_sources
        if source.get("repository_id", "")
    }

    for source in retained_sources:
        lines.extend(build_sour_record(source))
        report["sources"] += 1

    for repo in data.get("repositories", []):
        if repo["id"] in retained_repo_ids:
            lines.extend(build_repo_record(repo))
            report["repositories"] += 1

    lines.append("0 TRLR")

    errors = validate(data, lines)
    report["validation_errors"] = [str(e) for e in errors]

    return lines, report


def format_report(report, output_path):
    """Format the output report as human-readable text."""
    parts = []
    parts.append("=== GEDCOM File Created ===")
    parts.append(f"File: {output_path}")
    parts.append(
        f"Individuals: {report['individuals']} | "
        f"Families: {report['families']} | "
        f"Sources: {report['sources']}"
    )

    if report["redactions"]:
        parts.append(f"Living persons redacted: {len(report['redactions'])}")
        for r in report["redactions"]:
            parts.append(f"  - {r['name']} ({r['id']}) -- {r['reason']}")

    if report["family_redactions"]:
        family_ids = ", ".join(report["family_redactions"])
        parts.append(
            "Family details suppressed because a linked spouse was redacted: "
            f"{family_ids}"
        )

    if report["repairs"]:
        parts.append(f"Auto-repairs applied: {len(report['repairs'])}")
        for r in report["repairs"]:
            parts.append(f"  - {r}")

    if report["warnings"]:
        parts.append(f"Warnings: {len(report['warnings'])}")
        for w in report["warnings"]:
            parts.append(f"  - {w}")

    if report["validation_errors"]:
        parts.append(f"Validation: FAILED ({len(report['validation_errors'])} errors)")
        for e in report["validation_errors"]:
            parts.append(f"  - {e}")
    else:
        parts.append("Validation: PASSED (0 errors)")

    parts.append("")
    parts.append("Warning: This file may contain personal information.")
    parts.append("Review before sharing, uploading, or publishing.")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Build GEDCOM 5.5.1 files from canonical JSON input."
    )
    parser.add_argument("input", nargs="+",
                        help="Path(s) to canonical JSON input file(s)")
    parser.add_argument("--output", "-o", help="Output .ged file path")
    parser.add_argument("--submitter", "-s", default="Unknown",
                        help="Submitter name for SUBM record")
    parser.add_argument("--include-living", action="store_true",
                        help="Skip all redaction (WARNING: review before sharing). "
                             "For historical data, prefer --all-deceased.")
    parser.add_argument("--all-deceased", action="store_true",
                        help="Treat all individuals as deceased "
                             "(use for historical sources)")
    parser.add_argument("--deceased-before", type=int, metavar="YEAR",
                        help="Treat individuals with at least one dated "
                             "event and all finite date upper bounds before "
                             "YEAR as deceased (e.g., --deceased-before 1900)")
    parser.add_argument(
        "--include-redacted-family-details",
        action="store_true",
        help=("PRIVATE-USE OVERRIDE: include family events, notes, and "
              "citations linked to redacted spouses. These details may "
              "identify living people; review before any sharing."),
    )
    args = parser.parse_args()

    merge_warnings = []
    try:
        if len(args.input) > 1:
            data, merge_warnings = merge_json_files(args.input)
        else:
            with open(args.input[0], "r", encoding="utf-8") as f:
                data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

    # Size limit warnings
    n_indi = len(data.get("individuals", []))
    n_fam = len(data.get("families", []))
    if n_indi > 200 or n_fam > 100:
        print(f"Note: Large dataset (I:{n_indi}, F:{n_fam}). "
              f"Output may be large.", file=sys.stderr)

    output_path = args.output
    if not output_path:
        surname = "family"
        for ind in data.get("individuals", []):
            s = ind.get("surname", "")
            if s:
                surname = s.lower().replace(" ", "-")
                break
        output_path = f"{surname}-family.ged"

    lines, report = build_gedcom(
        data,
        submitter=args.submitter,
        include_living=args.include_living,
        all_deceased=args.all_deceased,
        deceased_before=args.deceased_before,
        include_redacted_family_details=args.include_redacted_family_details,
    )
    report["warnings"].extend(merge_warnings)

    if report["validation_errors"]:
        print(format_report(report, output_path))
        print("\nGEDCOM file NOT written due to validation errors.", file=sys.stderr)
        sys.exit(1)

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        for line in lines:
            f.write(line + CRLF)

    print(format_report(report, output_path))


if __name__ == "__main__":
    main()
