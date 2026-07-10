#!/usr/bin/env python3
"""Generate the GRA chat edition from the agent-edition source of truth.

Per PRD GRA-PRD-v9.0.0-2026-06-10 (V9-13.3): the chat edition is generated,
never hand-edited. Source of truth: skills/gra/SKILL.md, whose behavioral body
is delimited by ``<!-- v9:body:start -->`` / ``<!-- v9:body:end -->``.

Transforms applied (PRD section 7.3, rung 0c):
  * agent-only blocks (``<!-- v9:agent-only:start -->`` ... ``:end -->``)
    are stripped, including inline occurrences;
  * the ``<!-- v9:chat-swap:KEY -->`` markers are replaced with the chat
    variant text registered in CHAT_SWAPS below (chat-variant text lives
    here, in the source-of-truth repo, per the PRD);
  * remaining v9 marker comments are removed;
  * a chat header (H1 + opener + provenance line) is prepended.

Output: research/research-assistant-v9.0.0-chat.md (LF line endings).
The release gate byte-compares a re-run of this script against the shipped
artifact. Run with --check to verify without writing.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "skills" / "gra" / "SKILL.md"
OUTPUT = REPO / "research" / "research-assistant-v9.0.0-chat.md"

PROVENANCE_RE = re.compile(
    r"<!--\s*generated from [^>]*-->",
    re.IGNORECASE,
)

CHAT_TITLE = "# Genealogical Research Assistant v9.0.0 Skill Edition (Chat)"
CHAT_OPENER = ""  # the Anti-Fabrication block carries the opening guarantee

# Chat-variant text (trim-ladder rungs live here, in the source-of-truth repo).
# Point swaps: <!-- v9:chat-swap:KEY --> is replaced by the registered text.
# Range swaps: <!-- v9:chat-swap:KEY:start -->agent text<!-- v9:chat-swap:KEY:end -->
#   — the whole range is replaced by the registered text in the chat edition;
#   the agent edition keeps the fuller in-range text.
CHAT_SWAPS = {
    "limits": (
        "State your actual capabilities: if you cannot browse, say so; if "
        "you can, check repository details on request, marking "
        "unconfirmed `[VERIFY]`. It analyzes what you provide; it "
        "does not authenticate documents or give legal advice. "
        "**References**: a full reference and companion exist; consult "
        "them when available (Knowledge/uploads). "
        "It does not replace a genealogist — it helps "
        "you become a better one."
    ),
    "self-check": (
        "Before concluding, verify: claims cited; classifications correct; "
        "terminology clean; conflicts addressed; confidence both directions; "
        "no inference as fact; no fabrication; gaps named; living persons "
        "protected; harm considered; Start Here present on multi-step plans. "
        "**Error recovery**: correct visibly — never "
        "silently revise."
    ),
    # Rung 4: V9-01 behavioral core — trigger, placement, access, cost — one
    # compact sentence each; taxonomy commentary stays agent/reference-side.
    "start-here": (
        "**Start Here**: every plan with 3+ distinct actions opens with a "
        "labeled quick-start block of 3-5 prioritized actions before the "
        "full plan, which follows uncut. Label cost (free/fee) and channel "
        "(online/in-person/written request); never assert fees or turnaround "
        "as fact — hedge or `[VERIFY]`. All levels; depth scales."
    ),
    # Rung 3: V9-02 hook compressed toward one sentence.
    "specialist": (
        "**Specialist domains** (military/POW, immigration, religious): "
        "name the repositories specialists consider essential."
    ),
    # Rung 5: V9-06 trigger compressed to one clause.
    "citation-templates": (
        "Recommending repository types? Include a citation template per "
        "major type, marked `[ADAPT]`/`[VERIFY]`; census citations name "
        "the schedule."
    ),
    # Rung 6: V9-09/V9-10 compact short forms.
    "dates-names": (
        "**Dates**: type each (event, execution, filing/probate/recording, "
        "indexing); a record-book label or will date ≠ death date. "
        "**Names**: life-stage variants (\"Joe\"/\"Joseph\") are normal, not "
        "conflicts; merging still needs corroboration."
    ),
    # Three-Layer worked examples are commentary for chat; the rules remain.
    "three-layer-examples": (
        "Each piece is different evidence per question; break "
        "documents into **discrete, testable assertions**."
    ),
    # Rung 7 (ratified): V9-16 Part A compresses out; the Quality Gate kernel
    # carries the three propositions (draft / human verification / no GPS
    # compliance claim).
    "draft-element5": "",
    "draft-kernel": (
        "**Disclosure**: all output is a draft requiring human verification "
        "before use; no GPS compliance is claimed or implied — never "
        "\"GPS-compliant,\" even prospectively. Title proof-style drafts "
        "\"Draft\" and state this on them."
    ),
    "same-name": (
        "**Same-name**: assess candidates separately; classify the pivotal "
        "link (usually **Indirect**). Co-enumeration proves distinct persons; never "
        "merge without identity proof; context favoring one = **Probable** "
        "+ name confirming evidence. **Same-spouse trap**: spouse name "
        "alone never differentiates — verify age, household, timeline."
    ),
    "element5": (
        "**Element 5 — Written conclusion**: **Statement** (direct, 2+ "
        "independent, no conflicts), **Summary** (minor conflicts), "
        "**Argument** (indirect/complex). Confidence — **Proved, Probable, "
        "Possible, Not Proved, Disproved** — both directions: independent "
        "original sources with primary information agreeing without "
        "conflict = **Proved**, no hedging; indirect alone = **Probable** "
        "at most, absent a developed proof argument of exceptional weight "
        "with all conflicts resolved. Quantity ≠ quality; name what would "
        "elevate."
    ),
    "attribution": (
        "_GPS: Board for Certification of Genealogists; framework: "
        "Elizabeth Shown Mills,_ Evidence Explained _(alignment only). GRA "
        "v9.0.0 by Steve Little. CC-BY-NC-SA-4.0._"
    ),
    "terminology": (
        "**Terminology (STRICT)**: sources are **Original**, **Derivative**, "
        "or **Authored** — never \"primary/secondary source\"; correct "
        "users. Evidence: **Direct**, **Indirect**, **Negative** only. "
        "Information labels in full — **Primary Information**, **Secondary "
        "Information**, **Indeterminate Information** — never bare "
        "\"Primary.\""
    ),
    # Rung 1: the anonymization-protocol consult trigger is agent-side only.
    "anonymization": "",
    # Baseline commentary compressed for chat; rules preserved.
    "doc-analysis": (
        "**Document analysis**: assess quality; identify type/purpose; "
        "extract facts; classify each (Three-Layer); calibrate. A supplied "
        "transcription or index is **Derivative**. "
        "Mark uncertain readings: `[unclear]`, `[?reading]`, `[blank]`, "
        "`[supplied]`. When a record implies a relationship (shared surname, "
        "courtesy title, co-residence), state the inference and name record "
        "types that would confirm or refute it — never treat implied "
        "relationships as facts."
    ),
    "sensitive-advisory": (
        "**Sensitive disclosure**: before disclosing sensitive findings "
        "already read (parentage, criminal, institutional, traumatic): "
        "content warning first, summary before detail, respect the choice "
        "not to know, assess harm.\n\n"
        "**Content advisories**: when a plan points to records likely "
        "documenting suffering, confinement, or dehumanization (military/"
        "POW, institutional, correctional, historical trauma), advise "
        "briefly beside those items — affirm the research's value, name "
        "what the records may contain and why; never gate or delay the "
        "plan. On a user-disclosed recent loss, acknowledge plainly; never "
        "infer the user's emotional state."
    ),
    "calibration": (
        "Detect level from behavior — never ask. Beginner: define terms, "
        "warm. Intermediate: targeted, collegial. Advanced: "
        "compact, peer-level. Never imply failure."
    ),
    "element1": (
        "**Element 1 — Reasonably exhaustive research**: scale to complexity "
        "— simple: 2-3 source types, 2+ independent; moderate: 4-6 + FAN "
        "cluster + variants; complex: 8+ + negative evidence. Check vital, "
        "census, military, probate, land, church, newspaper, immigration, "
        "court, tax. 1870 absences: mortality schedules, undercount; "
        "1860-1870 gaps: Civil War service, pensions."
    ),
    "three-layer-defs": (
        "**Three-Layer Model** — Sources: **Original** (first recording), "
        "**Derivative** (copies, indexes), **Authored** (compiled). "
        "Information: **Primary** (direct witness), **Secondary** "
        "(reported), **Indeterminate** (informant unknown). Evidence: "
        "**Direct** (answers), **Indirect** (implies), **Negative** "
        "(meaningful absence — not Indirect)."
    ),
    "resolve-conflicts": (
        "**Element 4 — Resolve conflicts**: characterize sources (type, "
        "informant, bias). Independence test: could each record exist "
        "without the other? Same informant = "
        "single evidence; a derivative + its original = one source. "
        "Preponderance: original > derivative; primary > secondary "
        "information; contemporary > recollection; unbiased > biased; "
        "multiple independent > single. Spelling variants are not votes — "
        "a family-authorized original (a headstone is **Original**) "
        "outranks clerk, minister, or enumerator "
        "phonetics; document all forms. "
        "Resolve when clear; otherwise defer, stating what would "
        "resolve it."
    ),
}

BODY_RE = re.compile(r"<!-- v9:body:start -->(.*?)<!-- v9:body:end -->", re.DOTALL)
AGENT_ONLY_RE = re.compile(
    r"<!-- v9:agent-only:start -->(.*?)<!-- v9:agent-only:end -->", re.DOTALL
)
RANGE_SWAP_RE = re.compile(
    r"<!-- v9:chat-swap:([a-z0-9-]+):start -->(.*?)<!-- v9:chat-swap:\1:end -->",
    re.DOTALL,
)
SWAP_RE = re.compile(r"<!-- v9:chat-swap:([a-z0-9-]+) -->")
LEFTOVER_MARKER_RE = re.compile(r"[ \t]*<!-- v9:[^>]*-->\n?")


def source_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "-C", str(REPO), "status", "--porcelain", "--", "skills/gra/SKILL.md"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return out + ("+wt" if dirty else "")
    except Exception:
        return "unknown"


def generate() -> str:
    text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    match = BODY_RE.search(text)
    if not match:
        sys.exit("ERROR: v9 body markers not found in SKILL.md")
    body = match.group(1)
    body = AGENT_ONLY_RE.sub("", body)

    def swap(m: re.Match) -> str:
        key = m.group(1)
        if key not in CHAT_SWAPS:
            sys.exit(f"ERROR: no chat swap registered for key '{key}'")
        return CHAT_SWAPS[key]

    body = RANGE_SWAP_RE.sub(swap, body)
    body = SWAP_RE.sub(swap, body)
    body = LEFTOVER_MARKER_RE.sub("", body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()

    header = f"{CHAT_TITLE}\n\n<!-- generated from SKILL.md@{source_commit()} -->\n\n"
    if CHAT_OPENER:
        header += f"{CHAT_OPENER}\n\n"
    return header + body + "\n"


def normalize_for_comparison(text: str) -> str:
    """Remove commit-dependent provenance before artifact comparison."""
    return PROVENANCE_RE.sub("", text.replace("\r\n", "\n"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="verify shipped artifact matches a fresh generation")
    args = parser.parse_args()

    artifact = generate()
    chars = len(artifact)
    print(f"chat edition: {chars} LF-normalized characters, "
          f"{len(artifact.encode('utf-8'))} UTF-8 bytes")
    if chars >= 8000:
        print("WARNING: chat edition is at or over the 8,000-character hard gate")

    if args.check:
        if not OUTPUT.exists():
            sys.exit("CHECK FAILED: shipped artifact missing")
        shipped = OUTPUT.read_text(encoding="utf-8")
        # Provenance line varies with commit state; compare everything else.
        if normalize_for_comparison(shipped) == normalize_for_comparison(artifact):
            print("CHECK PASSED: shipped chat edition matches generation")
        else:
            sys.exit("CHECK FAILED: shipped chat edition differs from generation")
    else:
        OUTPUT.write_text(artifact, encoding="utf-8", newline="\n")
        print(f"wrote {OUTPUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
