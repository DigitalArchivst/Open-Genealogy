# Changelog

## v9.0.0 Skill Edition - 2026-07-09 - Two editions, presentation discipline, folded methodology patches

The first major release since v8: one methodology, two editions. Built to the
approved v9.0.0 PRD; supersedes the v8.5.x line.

- **Two editions**: the agent edition (`skills/gra/SKILL.md`, Agent Skills
  clients) and a chat edition (`research/research-assistant-v9.0.0-chat.md`,
  under 8,000 characters for Custom GPTs, Gems, and copy-paste), generated
  from the agent edition by `scripts/generate_chat_edition.py` — never
  hand-edited.
- **Presentation discipline**: "Start Here" quick-start blocks on multi-step
  research plans (universal, depth-scaled, cost-and-channel labeled, hedged
  costs); plan-time content advisories for hard records (preparation-framed,
  never gating); two-direction confidence calibration (anti-hedging paired
  with an indirect-evidence ceiling); citation templates in research plans;
  explicit draft self-labeling on analytical output.
- **Methodology guardrails**: operational two-prong source-independence test
  (provenance + informant); same-spouse coincidence trap; document-date
  taxonomy (six date types); life-stage name evolution; specialist-domain
  repository hooks with three worked domains (military/POW, immigration,
  religious).
- **Registered workflow markers**: `[citation needed]`, `[VERIFY]`, `[ADAPT]`.
- **Tests**: fixture suite grows from 11 to 25 (t12-t24 plus a paired
  advanced-persona fixture), with per-edition coverage mapping.
- Skill metadata, activation boundaries, and context-accurate capability
  disclosure are first-class; `scripts/measure_gra_compact.py` added for
  size-gate enforcement.
- **Legacy continuity**: the article-linked v8.5.1c full prompt and companion
  paths remain available, along with the versioned v8.5.3 reference.

## v8.5.3 - 2026-05-04 - Packaging release

No runtime or methodology changes. Refactor of skill packaging only.

- Moved `research-assistant-v8.5-full.md` and `companion-reference.md` into
  `skills/gra/references/` for the Agent Skills progressive-disclosure pattern.
- Added `skills/gra/agents/openai.yaml` for Codex metadata.
- Added `skills/gra/LICENSE` so the skill folder is standalone.
- Added `scripts/package_gra_skill.py` for repeatable allow-list packaging.
- Added `scripts/validate_gra_skill_zip.py` to verify extracted runtime ZIPs.
- Removed `tests/run_tests.py` and developer fixtures from the runtime install
  ZIP. Tests still live in the repo for contributors.
- Updated `SKILL.md` frontmatter to the current Codex-validator-compatible
  format. Cross-platform compatibility information moved to the README.
- Updated README install links and version references for v8.5.3.

## v8.5.2 - 2026-04-23 - Implied-Relationship Guardrail

Added guidance for records that imply, but do not prove, relationships through
shared surnames, courtesy titles, co-residence, or similar clues. The assistant
is instructed to name the inference explicitly and identify evidence that could
confirm or refute it.

- Added the Warren Dean Lawrence draft-card scenario as a regression fixture.
- Preserved public filenames and paths from the previous GRA release.
- Release verification reported the full GRA suite at 11/11 fixtures clean.

See full notes at
<https://github.com/DigitalArchivst/Open-Genealogy/releases/tag/v8.5.2>.

## v8.5.1c - 2026-04-05 - Genealogical Research Assistant

Published the compact GRA prompt and Agent Skill package for genealogical
research. The release is designed to follow GPS methodology, the Three-Layer
Evidence Model, and strict anti-fabrication principles.

- Included Claude Desktop/Cowork and Claude Code installation paths.
- Linked related ChatGPT Custom GPT, Gemini Gem, copy-paste prompt, and blog
  post resources.
- Released under CC-BY-NC-SA-4.0.

See full notes at
<https://github.com/DigitalArchivst/Open-Genealogy/releases/tag/v8.5.1c>.
