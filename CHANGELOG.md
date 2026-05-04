# Changelog

## v8.5.3 - 2026-05-04 - Packaging release

No runtime or methodology changes. Refactor of skill packaging only.

- Moved `research-assistant-v8.5-full.md` and `companion-reference.md`
  into `skills/gra/references/` for the Agent Skills progressive-disclosure
  pattern.
- Added `skills/gra/agents/openai.yaml` for Codex metadata.
- Added `skills/gra/LICENSE` so the skill folder is standalone.
- Added `scripts/package_gra_skill.py` for repeatable allow-list packaging.
- Added `scripts/validate_gra_skill_zip.py` to verify extracted runtime ZIPs.
- Removed `tests/run_tests.py` and developer fixtures from the runtime install
  ZIP. Tests still live in the repo for contributors.
- Updated `SKILL.md` frontmatter to the current Codex-validator-compatible
  format. Cross-platform compatibility information moved to the README.
- Updated README install links and version references for v8.5.3.
