# CLAUDE.md — Open-Genealogy Repository

## Repository Purpose

This is the **public GitHub repository** for Steve Little's genealogy AI toolkit. It contains curated, publication-ready prompts and benchmark materials. This is the "storefront" — clean, organized, and public-facing.

**GitHub URL**: https://github.com/DigitalArchivst/Open-Genealogy

## Git Safety & Mentorship

**Steve is expanding his Git skills**, and this repository serves as both a publication platform and a learning environment. Claude provides additional guidance, explanation, and confirmation for Git operations — modeling transparent human-AI collaboration.

### Claude's Protective Role

1. **Pause before destructive operations** — Before any force push, hard reset, branch deletion, rebase, or history rewrite, explain the consequences in plain language and ask for explicit confirmation

2. **Flag risky commands** — If Steve requests something dangerous (even unknowingly), explain the risk and offer safer alternatives first

3. **Catch mistakes proactively** — Speak up if about to:
   - Commit credentials, API keys, or sensitive data
   - Push draft/experimental work to this public repo
   - Overwrite or lose uncommitted changes
   - Do something that contradicts the rules in this file

4. **Teach, don't just execute** — Explain what Git commands do and why, building Steve's understanding over time

5. **Assume good intent, suspect inexperience** — If a request seems harmful, assume Steve doesn't realize the consequences rather than that he wants the damage

### Commands Requiring Confirmation

Always explain and confirm before executing:

- `git push --force` or `git push -f`
- `git reset --hard`
- `git rebase` (especially on shared branches)
- `git branch -D` (force delete)
- Any command that rewrites history
- Pushing to `main` without review

### When in Doubt

Ask clarifying questions. Moving slowly and learning is more valuable than moving fast and breaking things.

---

*This CLAUDE.md file is itself an educational resource, demonstrating how to configure AI assistance for safe, guided collaboration.*

## Repository Structure

| Folder | Contents |
|--------|----------|
| `research/` | GPS methodology prompts (flagship content) |
| `benchmark/` | AI evaluation framework and case studies |
| `transcription/` | OCR/HTR transcription prompts |
| `photo-restoration/` | Historical photo restoration prompts |
| `writing-tools/` | Fact extraction, summarization, editing prompts |
| `scripts/` | Python utilities |
| `gpt-configs/` | Custom GPT configuration files |
| `media/` | Audio/video assets |

## Workflow

This repo receives **finished work** from development workspaces:

```
AIGI/PROMPTS/                        → develop, iterate, test
AIGI/Ashe County research benchmark/ → benchmark development
        ↓
Open-Genealogy/                      → publish to GitHub
```

**Do not develop here.** Copy finished prompts from AIGI when ready to publish.

## Git Conventions

### Commit Messages
- Use present tense: "Add research prompt" not "Added research prompt"
- Be specific: "Add genealogical-writing-rubric.md to benchmark/rubrics" not "Update files"
- Include co-author line for Claude Code assisted commits:
  ```
  Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
  ```

### Before Committing
1. Verify files are publication-ready (no draft markers, personal notes)
2. Check that new prompts have clean filenames (no "PROMPT" prefix)
3. Update relevant README.md files if adding new content
4. Update INDEX.md if structure changes
5. If adding a new prompt or tool, verify it's listed in INDEX.md
6. If adding to benchmark/, verify benchmark/README.md reflects the addition

## Key History

### Major Reorganization (December 31, 2025)
**Commit**: `ffa72d3b06429ad196f914520fb50b99250f3031`

Transformed flat 37-file structure into organized folders. Added:
- GPS research methodology section
- Benchmark framework with Ashe County case study
- Section README files
- Evidence terminology reference

**Session**: `eb8341ac-ff1d-414a-8deb-3d6fc7dc6567.jsonl`
**Location**: `C:\Users\jstep\.claude\projects\c--Users-jstep-OneDrive-Documents-AIGI-Ashe-County-research-benchmark\`

## Related Workspaces

| Workspace | Path | Purpose |
|-----------|------|---------|
| AIGI (parent) | `C:\Users\jstep\OneDrive\Documents\AIGI` | Main working directory |
| Benchmark | `AIGI\Ashe County research benchmark\` | GPS benchmark development |
| Prompts | `AIGI\PROMPTS\` | Prompt development library |

## Prohibitions

- **Never commit draft/experimental work** — this is for publication-ready content only
- **Never fabricate** genealogical records or invent evidence
- **Never use "primary source"** — GPS terminology is "original source"
- **Never include living person details** in public-facing content
