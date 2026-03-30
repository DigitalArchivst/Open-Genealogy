#!/usr/bin/env python3
"""
GEDCOM 5.5.1 Builder — Claude Code Skill Companion Script

License: MIT

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

GEDCOM_DATE_PREFIXES = {"ABT", "BEF", "AFT", "CAL", "EST", "INT"}
GEDCOM_DATE_RANGE = {"BET", "FROM"}
GEDCOM_MONTHS = {
    "JAN", "FEB", "MAR", "APR", "MAY", "JUN",
    "JUL", "AUG", "SEP", "OCT", "NOV", "DEC",
}

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


# ---------------------------------------------------------------------------
# Sanitization
# ---------------------------------------------------------------------------

def sanitize_value(value):
    """Strip characters that could corrupt GEDCOM structure."""
    if not value:
        return ""
    # Remove newlines and carriage returns
    value = value.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
    # Strip trailing whitespace
    value = value.rstrip()
    return value


# ---------------------------------------------------------------------------
# Living person detection
# ---------------------------------------------------------------------------

def is_presumed_living(individual):
    """Determine if an individual should be treated as living.

    Conservative default: presume living unless death is confirmed.
    """
    # Check for death event
    for event in individual.get("events", []):
        if event.get("type") == "DEAT":
            return False  # Has death event — deceased

    # Check birth year against threshold
    birth_year = _extract_year(individual)
    if birth_year:
        current_year = date.today().year
        if current_year - birth_year >= LIVING_THRESHOLD_YEARS:
            return False  # Born 110+ years ago, no death — still flag as deceased

    # No death event, and either young enough or no birth date — presume living
    return True


def _extract_year(individual):
    """Extract birth year from an individual's events."""
    for event in individual.get("events", []):
        if event.get("type") == "BIRT" and event.get("date"):
            return _parse_year_from_date(event["date"])
    return None


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

def build_indi_record(ind, living_ids, sources_map):
    """Build a GEDCOM INDI record from the canonical JSON."""
    lines = []
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

        name_str = f"{given} /{surname}/"
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

    # Events (skip if living, except DEAT which won't exist for living)
    for event in ind.get("events", []):
        etype = event.get("type", "")
        if etype not in VALID_INDI_EVENTS:
            continue
        if is_living and etype != "DEAT":
            continue  # Strip events for living persons

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
        if src_id and not is_living:
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
            note = sanitize_value(note)
            if note:
                lines.extend(split_long_value(1, "NOTE", note))

    # Individual-level source citations (non-event)
    if not is_living:
        for src_ref in ind.get("source_citations", []):
            src_id = src_ref.get("source_id", "")
            if src_id:
                lines.append(f"1 SOUR @{src_id}@")
                page = sanitize_value(src_ref.get("source_page", ""))
                if page:
                    lines.extend(split_long_value(2, "PAGE", page))
                quay = src_ref.get("quality", "")
                if quay in (0, 1, 2, 3, "0", "1", "2", "3"):
                    lines.append(f"2 QUAY {quay}")

    return lines


def build_fam_record(fam):
    """Build a GEDCOM FAM record from the canonical JSON."""
    lines = []
    xref = f"@{fam['id']}@"
    lines.append(f"0 {xref} FAM")

    sp1 = fam.get("spouse1", "")
    sp2 = fam.get("spouse2", "")
    if sp1:
        lines.append(f"1 HUSB @{sp1}@")
    if sp2:
        lines.append(f"1 WIFE @{sp2}@")

    for child_id in fam.get("children", []):
        if child_id:
            lines.append(f"1 CHIL @{child_id}@")

    for event in fam.get("events", []):
        etype = event.get("type", "")
        if etype not in VALID_FAM_EVENTS:
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
        if src_id:
            lines.append(f"2 SOUR @{src_id}@")
            src_page = sanitize_value(event.get("source_page", ""))
            if src_page:
                lines.extend(split_long_value(3, "PAGE", src_page))

    for note in fam.get("notes", []):
        note = sanitize_value(note)
        if note:
            lines.extend(split_long_value(1, "NOTE", note))

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
        note = sanitize_value(note)
        if note:
            lines.extend(split_long_value(1, "NOTE", note))

    return lines


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


def validate(data, gedcom_lines):
    """Run all validation checks. Returns list of ValidationError."""
    errors = []

    indi_ids = {ind["id"] for ind in data.get("individuals", [])}
    fam_ids = {fam["id"] for fam in data.get("families", [])}
    sour_ids = {s["id"] for s in data.get("sources", [])}
    repo_ids = {r["id"] for r in data.get("repositories", [])}
    all_ids = indi_ids | fam_ids | sour_ids | repo_ids | {"U1"}

    # --- Pointer resolution ---
    for ind in data.get("individuals", []):
        famc = ind.get("family_child", "")
        if famc and famc not in fam_ids:
            errors.append(ValidationError(
                "DANGLING_POINTER",
                f"{ind['id']} references family_child {famc} which does not exist"
            ))
        for fams in ind.get("family_spouse", []):
            if fams and fams not in fam_ids:
                errors.append(ValidationError(
                    "DANGLING_POINTER",
                    f"{ind['id']} references family_spouse {fams} which does not exist"
                ))
        for event in ind.get("events", []):
            src = event.get("source_id", "")
            if src and src not in sour_ids:
                errors.append(ValidationError(
                    "DANGLING_POINTER",
                    f"{ind['id']} event references source {src} which does not exist"
                ))

    for fam in data.get("families", []):
        for role in ("spouse1", "spouse2"):
            ref = fam.get(role, "")
            if ref and ref not in indi_ids:
                errors.append(ValidationError(
                    "DANGLING_POINTER",
                    f"Family {fam['id']} {role} references {ref} which does not exist"
                ))
        for child in fam.get("children", []):
            if child and child not in indi_ids:
                errors.append(ValidationError(
                    "DANGLING_POINTER",
                    f"Family {fam['id']} child references {child} which does not exist"
                ))

    for src in data.get("sources", []):
        repo = src.get("repository_id", "")
        if repo and repo not in repo_ids:
            errors.append(ValidationError(
                "DANGLING_POINTER",
                f"Source {src['id']} references repository {repo} which does not exist"
            ))

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

    for ind_id in parent_map:
        visited = set()
        queue = [ind_id]
        while queue:
            node = queue.pop(0)
            if node in visited:
                errors.append(ValidationError(
                    "CYCLE_DETECTED",
                    f"Circular parent-child relationship involving {node}"
                ))
                break
            visited.add(node)
            queue.extend(parent_map.get(node, []))

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

    return repairs


# ---------------------------------------------------------------------------
# Main build pipeline
# ---------------------------------------------------------------------------

def build_gedcom(data, submitter="Unknown", include_living=False):
    """Build complete GEDCOM 5.5.1 from canonical JSON data."""
    report = {
        "individuals": 0, "families": 0, "sources": 0, "repositories": 0,
        "redactions": [], "repairs": [], "validation_errors": [], "warnings": [],
    }

    repairs = auto_repair_pointers(data)
    report["repairs"] = repairs

    living_ids = set()
    if not include_living:
        for ind in data.get("individuals", []):
            if is_presumed_living(ind):
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

    for ind in data.get("individuals", []):
        lines.extend(build_indi_record(ind, living_ids, sources_map))
        report["individuals"] += 1

    for fam in data.get("families", []):
        lines.extend(build_fam_record(fam))
        report["families"] += 1

    for source in data.get("sources", []):
        lines.extend(build_sour_record(source))
        report["sources"] += 1

    for repo in data.get("repositories", []):
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

    if report["repairs"]:
        parts.append(f"Auto-repairs applied: {len(report['repairs'])}")
        for r in report["repairs"]:
            parts.append(f"  - {r}")

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
    parser.add_argument("input", help="Path to canonical JSON input file")
    parser.add_argument("--output", "-o", help="Output .ged file path")
    parser.add_argument("--submitter", "-s", default="Unknown",
                        help="Submitter name for SUBM record")
    parser.add_argument("--include-living", action="store_true",
                        help="Include living person details (WARNING: review before sharing)")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error reading input: {e}", file=sys.stderr)
        sys.exit(1)

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
        data, submitter=args.submitter, include_living=args.include_living,
    )

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
