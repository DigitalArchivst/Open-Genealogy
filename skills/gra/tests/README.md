# GRA Skill — Test Suite

Automated behavioral tests for the Genealogical Research
Assistant skill. Validates GPS alignment, anti-fabrication,
terminology, and ethical behavior.

## How It Works

1. Loads `SKILL.md` as the system prompt
2. Sends each fixture's input to Claude (Sonnet)
3. Checks the response with string matching (terminology) and
   a rubric-guided judge (Haiku) against MUST/MUST NOT criteria
4. Reports pass/fail per fixture, saves results to JSON

**Ground truth** comes from the 52 Ancestors project — 81 record
notes, 30+ documented decisions, and a full GPS alignment audit.
These are real analyses Steve validated during active research,
not synthetic examples.

## Prerequisites

```bash
pip install anthropic
```

Set the API key:

```bash
export ANTHROPIC_AI_KEY_AI_NEWS_TODAY=sk-ant-...
```

## Usage

```bash
# Run all tests
py run_tests.py

# Run specific tests
py run_tests.py t01 t05

# Run with full response output
py run_tests.py --verbose

# List available tests
py run_tests.py --list
```

## Test Fixtures

| ID | Name | Tests |
| -- | ---- | ----- |
| T01 | Three-Layer Census | Source/info/evidence classification |
| T02 | Conflict Resolution | Name spelling via source hierarchy |
| T03 | Disambiguation | Same-name, two-person identification |
| T04 | Anti-Fabrication | Refusal to invent ancestors |
| T05 | Terminology | "Primary source" correction |
| T06 | Negative Evidence | Meaningful absence recognition |
| T07 | Proof Vehicle | Statement vs Summary vs Argument |
| T08 | Citation Completeness | Five-element citation check |
| T09 | FAN Principle | Brick wall research strategy |
| T10 | Living Person | Privacy protection refusal |

## Evaluation Method

**String checks** (high confidence, deterministic):

- Forbidden terms: "primary source", "secondary source",
  "primary evidence", "secondary evidence"
- Allows these terms in correction context (quoting the user,
  explaining what NOT to say)

**Rubric-guided judge** (Haiku, classification only):

- Each MUST/MUST NOT criterion evaluated independently
- Judge sees the ground truth for reference
- Judge outputs PASS or FAIL per criterion — no open-ended
  reasoning about GPS

This avoids the circularity problem: the judge classifies
against a rubric, it doesn't need to understand GPS.

## Results

Results are saved to `results/run-YYYY-MM-DD_HHMM.json` with
full responses and per-criterion verdicts.

## Cost

~$0.10-0.30 per full run (10 Sonnet calls + 10 Haiku judge
calls). Runs against the API, not the Max plan subscription.

## Adding Tests

Create a new fixture in `fixtures/` following the pattern:

```markdown
# TNN: Test Name

## Source
Where the ground truth comes from.

## Input
> The prompt to send to the GRA.

## MUST Criteria
- [ ] What the response must do

## MUST NOT Criteria
- [ ] What the response must not do

## Ground Truth
What correct behavior looks like.
```

The test runner auto-discovers any `t*.md` file in `fixtures/`.
