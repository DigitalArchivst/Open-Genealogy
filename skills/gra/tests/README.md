# GRA Skill — Test Suite

Automated behavioral tests for the Genealogical Research
Assistant skill. Validates GPS alignment, anti-fabrication,
terminology, and ethical behavior.

## How It Works

1. Loads `SKILL.md` as the system prompt (or an alternate
   prompt via `--system`, e.g. the generated chat edition)
2. Sends each fixture's input to Claude (Opus 4.6)
3. Checks the response with string matching (terminology) and
   a rubric-guided judge (Sonnet 4.6) against MUST/MUST NOT
   criteria
4. Reports pass/fail per fixture, saves results to JSON

Test fixtures contain research scenarios designed to validate
GPS alignment, anti-fabrication, terminology, and ethical behavior.

## Prerequisites

```bash
pip install anthropic
```

Set the API key:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
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

# Run against the generated chat edition (the chat-edition pass;
# t18 is agent-only, so exclude it)
py run_tests.py --system ../../../research/research-assistant-v9.0.0-chat.md --label chat --exclude t18

# Tag the results filename (avoids collisions between
# concurrent runs)
py run_tests.py --label agent
```

## Test Fixtures

| ID | Name | Tests | Edition |
| -- | ---- | ----- | ------- |
| T01 | Three-Layer Census | Source/info/evidence classification | Both |
| T02 | Conflict Resolution | Name spelling via source hierarchy | Both |
| T03 | Disambiguation | Same-name, two-person identification | Both |
| T04 | Anti-Fabrication | Refusal to invent ancestors | Both |
| T05 | Terminology | "Primary source" correction | Both |
| T06 | Negative Evidence | Meaningful absence recognition | Both |
| T07 | Proof Vehicle | Statement vs Summary vs Argument | Both |
| T08 | Citation Completeness | Five-element citation check | Both |
| T09 | FAN Principle | Brick wall research strategy | Both |
| T10 | Living Person | Privacy protection refusal | Both |
| T11 | Implied Relationship | Courtesy-title relationship inference | Both |
| T12 | Start-Here Summary | Quick-start block before plan, intermediate | Both |
| T12b | Start-Here (advanced) | Depth scaling at advanced level | Both |
| T13 | Domain Repositories | Specialist-domain repositories | Both (split) |
| T14 | Source Independence | Index + original = one source; same informant | Both |
| T15 | Content Advisory | Advisory present, nothing gated | Both |
| T16 | Indirect-Evidence Ceiling | Probable max on indirect-only | Both |
| T17 | Plan Citation Templates | Templates with ADAPT/VERIFY | Both |
| T18 | Teaching-Case Anonymization | No leaks; gates named | Agent |
| T19 | Same-Spouse Trap | Spouse name never sole proof | Both |
| T20 | Document-Date Taxonomy | Label is not an event date | Both |
| T21 | Name Evolution | Variants normal; no auto-merge | Both |
| T22 | Draft-Label Disclosure | Draft kernel + disclosure | Both |
| T23 | Activation Boundaries | Scope declines + routing | Both (split) |
| T24 | Agent-vs-Chat Behavior | Context-accurate disclosure | Both (paired) |

**Edition column:** v9.0.0 ships one methodology in two editions — the
agent edition (`SKILL.md`) and a chat edition generated from it. "Both"
fixtures run against each edition. "Agent" fixtures run against the
agent edition only. "Both (split)" fixtures carry edition-conditional
criteria — T13 keeps named-repository assertions agent-side; T23's
agent edition routes GEDCOM requests to the gedcom-creator skill while
the chat edition declines without naming any skill. "Both (paired)"
means the same input runs once per edition and each edition's
assertions apply to its own response (T24, including a
browsing-enabled Custom GPT sub-case). The runner loads `SKILL.md` by
default; a chat-edition run substitutes the generated chat edition as
the system prompt via `--system` (see Usage).

## Evaluation Method

**String checks** (high confidence, deterministic):

- Forbidden terms: "primary source", "secondary source",
  "primary evidence", "secondary evidence"
- Allows these terms in correction context (quoting the user,
  explaining what NOT to say)

**Rubric-guided judge** (Sonnet 4.6, classification only):

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

~$1-2 per full run (25 Opus 4.6 calls + 25 Sonnet 4.6 judge
calls). Runs against the API, not the Max plan subscription.

## Adding Tests

Create a new fixture in `fixtures/` following the pattern:

```markdown
# TNN: Test Name

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
