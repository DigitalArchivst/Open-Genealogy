"""
GRA Skill Test Runner

Sends each test fixture's input to Claude with the GRA SKILL.md as
system prompt, then evaluates the response against MUST/MUST NOT
rubrics using string matching and a rubric-guided judge.

Usage:
    py run_tests.py                  # Run all tests
    py run_tests.py t01 t05          # Run specific tests
    py run_tests.py --list           # List available tests
    py run_tests.py --verbose        # Show full responses

Requires:
    ANTHROPIC_API_KEY environment variable set
    pip install anthropic  (if not already installed)

Cost: ~$0.10-0.30 per full run (Sonnet for test, Haiku for judge)
"""

import os
import re
import sys
import glob
import json
import time
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding for Unicode output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
FIXTURES_DIR = SCRIPT_DIR / "fixtures"
RESULTS_DIR = SCRIPT_DIR / "results"

# Models
TEST_MODEL = "claude-sonnet-4-20250514"
JUDGE_MODEL = "claude-haiku-4-5-20251001"

# API key
API_KEY_ENV = "ANTHROPIC_API_KEY"


def load_skill_prompt():
    """Load SKILL.md as the system prompt, stripping YAML frontmatter."""
    skill_path = SKILL_DIR / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    # Strip YAML frontmatter
    if text.startswith("---"):
        end = text.index("---", 3)
        text = text[end + 3:].strip()
    return text


def parse_fixture(path):
    """Parse a test fixture into structured components."""
    text = path.read_text(encoding="utf-8")
    fixture = {"id": path.stem, "path": str(path)}

    # Extract Input section
    input_match = re.search(
        r"## Input\s*\n(.*?)(?=\n## (?:MUST|MUST NOT) Criteria)",
        text, re.DOTALL
    )
    if input_match:
        # Strip blockquote markers and clean up
        raw = input_match.group(1).strip()
        lines = []
        for line in raw.split("\n"):
            line = re.sub(r"^>\s?", "", line)
            lines.append(line)
        fixture["input"] = "\n".join(lines).strip()

    # Extract MUST criteria
    must_match = re.search(
        r"## MUST Criteria\s*\n(.*?)(?=\n## MUST NOT Criteria)",
        text, re.DOTALL
    )
    if must_match:
        fixture["must"] = extract_checklist(must_match.group(1))

    # Extract MUST NOT criteria
    must_not_match = re.search(
        r"## MUST NOT Criteria\s*\n(.*?)(?=\n## Ground Truth)",
        text, re.DOTALL
    )
    if must_not_match:
        fixture["must_not"] = extract_checklist(must_not_match.group(1))

    # Extract Ground Truth
    gt_match = re.search(r"## Ground Truth\s*\n(.*)", text, re.DOTALL)
    if gt_match:
        fixture["ground_truth"] = gt_match.group(1).strip()

    return fixture


def extract_checklist(text):
    """Extract checklist items from markdown checkbox list."""
    items = []
    for line in text.strip().split("\n"):
        match = re.match(r"^-\s*\[.\]\s*(.*)", line.strip())
        if match:
            items.append(match.group(1).strip())
    return items


def call_claude(system, user, model):
    """Make an API call to Claude."""
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ[API_KEY_ENV])
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text


def string_checks(response, fixture):
    """Run string-match checks against the response."""
    results = []
    lower = response.lower()

    # Terminology MUST NOT checks (high confidence, string-based)
    terminology_violations = {
        "primary source": "Used forbidden term 'primary source'",
        "secondary source": "Used forbidden term 'secondary source'",
        "primary evidence": "Used forbidden term 'primary evidence'",
        "secondary evidence": "Used forbidden term 'secondary evidence'",
    }

    for term, message in terminology_violations.items():
        # Allow the term if it's in a correction context
        # (quoting the user or explaining what NOT to say)
        occurrences = [
            m.start() for m in re.finditer(re.escape(term), lower)
        ]
        for pos in occurrences:
            # Check surrounding context (100 chars each side)
            start = max(0, pos - 100)
            end = min(len(lower), pos + len(term) + 100)
            context = lower[start:end]
            # If context suggests correction/quoting, allow it
            correction_signals = [
                "never say", "don't say", "not say", "avoid",
                "instead of", "rather than", "incorrect",
                "library science", "not genealogy", "gps uses",
                "should be", "correct term", "you asked",
                "your question", "you said",
                '"', "'",
            ]
            if not any(signal in context for signal in correction_signals):
                results.append(("FAIL", f"STRING: {message}"))
                break
        else:
            results.append(("PASS", f"STRING: No unqualified '{term}'"))

    # Check for "original source" presence (should appear in most tests)
    if fixture["id"] != "t04-anti-fabrication":
        if "original" in lower and "source" in lower:
            results.append(("PASS", "STRING: Uses 'original source'"))
        else:
            results.append(
                ("WARN", "STRING: 'original source' not found")
            )

    return results


def judge_rubric(response, fixture):
    """Use a rubric-guided judge to evaluate MUST/MUST NOT criteria."""
    must_text = "\n".join(
        f"  MUST {i+1}: {item}"
        for i, item in enumerate(fixture.get("must", []))
    )
    must_not_text = "\n".join(
        f"  MUST_NOT {i+1}: {item}"
        for i, item in enumerate(fixture.get("must_not", []))
    )

    judge_prompt = f"""You are a GPS methodology alignment judge.
Evaluate the RESPONSE against each criterion below.

For each criterion, respond with exactly one line:
PASS|criterion_id|brief reason
or
FAIL|criterion_id|brief reason

Do not explain further. Do not add commentary. Just the verdicts.

CRITERIA:
{must_text}
{must_not_text}

GROUND TRUTH (for reference):
{fixture.get('ground_truth', 'N/A')}

RESPONSE TO EVALUATE:
{response}
"""

    judge_response = call_claude(
        system="You are a strict rubric evaluator. Output only "
               "PASS|id|reason or FAIL|id|reason lines.",
        user=judge_prompt,
        model=JUDGE_MODEL,
    )

    results = []
    for line in judge_response.strip().split("\n"):
        line = line.strip()
        if line.startswith("PASS") or line.startswith("FAIL"):
            parts = line.split("|", 2)
            if len(parts) >= 3:
                status = parts[0].strip()
                crit_id = parts[1].strip()
                reason = parts[2].strip()
                results.append((status, f"JUDGE {crit_id}: {reason}"))
            elif len(parts) == 2:
                status = parts[0].strip()
                rest = parts[1].strip()
                results.append((status, f"JUDGE: {rest}"))
    return results


def run_test(fixture, system_prompt, verbose=False):
    """Run a single test fixture."""
    print(f"\n{'=' * 60}")
    print(f"  {fixture['id']}")
    print(f"{'=' * 60}")

    # Send the test input
    response = call_claude(
        system=system_prompt,
        user=fixture["input"],
        model=TEST_MODEL,
    )

    if verbose:
        print(f"\n--- Response ---\n{response}\n--- End ---\n")

    # String checks
    string_results = string_checks(response, fixture)

    # Judge checks
    judge_results = judge_rubric(response, fixture)

    # Combine
    all_results = string_results + judge_results

    passes = sum(1 for s, _ in all_results if s == "PASS")
    fails = sum(1 for s, _ in all_results if s == "FAIL")
    warns = sum(1 for s, _ in all_results if s == "WARN")

    for status, msg in all_results:
        icon = {"PASS": "+", "FAIL": "X", "WARN": "?"}[status]
        print(f"  [{icon}] {msg}")

    print(f"\n  Result: {passes} pass, {fails} fail, {warns} warn")

    return {
        "id": fixture["id"],
        "response": response,
        "results": all_results,
        "passes": passes,
        "fails": fails,
        "warns": warns,
    }


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    list_only = "--list" in sys.argv

    # Find fixtures
    fixture_paths = sorted(FIXTURES_DIR.glob("t*.md"))

    if list_only:
        print("Available test fixtures:")
        for p in fixture_paths:
            print(f"  {p.stem}")
        return

    # Filter to specific tests if named
    named = [a for a in sys.argv[1:] if not a.startswith("-")]
    if named:
        fixture_paths = [
            p for p in fixture_paths
            if any(n in p.stem for n in named)
        ]

    if not fixture_paths:
        print("No fixtures found.")
        return

    # Check API key
    if API_KEY_ENV not in os.environ:
        print(f"Error: {API_KEY_ENV} not set.")
        sys.exit(1)

    # Load skill prompt
    system_prompt = load_skill_prompt()
    print(f"Loaded SKILL.md ({len(system_prompt)} chars)")
    print(f"Running {len(fixture_paths)} tests with {TEST_MODEL}")
    print(f"Judge model: {JUDGE_MODEL}")

    # Run tests
    all_test_results = []
    start = time.time()

    for path in fixture_paths:
        fixture = parse_fixture(path)
        result = run_test(fixture, system_prompt, verbose=verbose)
        all_test_results.append(result)

    elapsed = time.time() - start

    # Summary
    total_pass = sum(r["passes"] for r in all_test_results)
    total_fail = sum(r["fails"] for r in all_test_results)
    total_warn = sum(r["warns"] for r in all_test_results)
    tests_clean = sum(
        1 for r in all_test_results if r["fails"] == 0
    )

    print(f"\n{'=' * 60}")
    print(f"  SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Tests run: {len(all_test_results)}")
    print(f"  Tests clean (0 fails): {tests_clean}"
          f"/{len(all_test_results)}")
    print(f"  Total checks: {total_pass} pass, {total_fail} fail,"
          f" {total_warn} warn")
    print(f"  Time: {elapsed:.1f}s")
    print(f"  Model: {TEST_MODEL}")

    # Save results
    RESULTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    report_path = RESULTS_DIR / f"run-{timestamp}.json"

    report = {
        "timestamp": timestamp,
        "test_model": TEST_MODEL,
        "judge_model": JUDGE_MODEL,
        "skill_chars": len(system_prompt),
        "summary": {
            "tests_run": len(all_test_results),
            "tests_clean": tests_clean,
            "total_pass": total_pass,
            "total_fail": total_fail,
            "total_warn": total_warn,
            "elapsed_seconds": round(elapsed, 1),
        },
        "tests": [
            {
                "id": r["id"],
                "passes": r["passes"],
                "fails": r["fails"],
                "warns": r["warns"],
                "results": [
                    {"status": s, "message": m}
                    for s, m in r["results"]
                ],
                "response": r["response"],
            }
            for r in all_test_results
        ],
    }

    report_path.write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(f"  Report: {report_path}")

    # Exit code
    sys.exit(1 if total_fail > 0 else 0)


if __name__ == "__main__":
    main()
