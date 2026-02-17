# GPS Research Methodology

Prompts for research workflows designed around the **Genealogical Proof Standard (GPS)**. These are structured to follow professional methodology developed by the Board for Certification of Genealogists and documented in Mills' *Evidence Explained*.

## Core Concepts

GPS ensures genealogical conclusions are well-reasoned and evidence-based through five interdependent elements:

1. **Reasonably exhaustive research**
2. **Complete, accurate citations**
3. **Thorough analysis and correlation**
4. **Resolution of conflicting evidence**
5. **Coherent written conclusion**

## Recommended Prompts

| Prompt | Purpose | Use When |
|--------|---------|----------|
| **[research-assistant-v8.md](research-assistant-v8.md)** | Full GPS-based research assistant (669 lines) | System prompt for ongoing research assistance |
| **[research-assistant-v8-compact.md](research-assistant-v8-compact.md)** | Token-efficient v8 | Context-limited models |
| **[research-with-citations-v7.md](research-with-citations-v7.md)** | Web research with GPS methodology | Single research queries with citation requirements |
| **[web-research-v7.md](web-research-v7.md)** | Compact web search prompt | Quick web research tasks |
| **[contract-first-genealogy-v3.1.md](contract-first-genealogy-v3.1.md)** | Contract-lock workflow | Structured research projects with deliverables |
| **[research-agent-assignment-v2.1.md](research-agent-assignment-v2.1.md)** | Research agent specification | Autonomous research tasks |

## Full vs. Compact Variants

The compact/compressed versions are token-efficient alternatives for context-limited models. Here's what they trade away:

| Feature | Full v8 (704 lines) | Compact v8 (147 lines) |
| ------- | ------------------- | ---------------------- |
| Three-Layer Model | Detailed tables with examples | Condensed paragraph summaries |
| Worked examples | Death certificate walkthrough | Omitted |
| Adaptive scaffolding | Full detection protocol + calibration table | Simplified behavioral cues |
| Decision trees | Appendix B flowcharts | Omitted |
| Core templates | Evidence table, research plan, conflict matrix, proof summary | Omitted |
| Terminology reference | Appendix A quick-reference table | Omitted |
| Provenance chain | Detailed with error propagation | Brief mention |
| Cluster research | Full FAN protocol + same-name defense | Brief mention |

**When to use compact:** Models with small context windows, or when combined with other system prompts. The compact variant preserves all rules, guardrails, and the evidence framework — it cuts examples, templates, and decision trees.

**Risk:** Without worked examples, models may apply the Three-Layer Model less precisely. Without templates, users must structure their own output formats.

## Version History

### What changed in v8 (from v7)

v8 was amalgamated from five beta candidates through systematic feature analysis (January 2026). Key changes:

- **Restructured into 10 parts** (v7 had a flatter organization) — clearer separation of concerns
- **Added prompt-injection resistance** — explicit instruction to treat uploaded documents as data, not commands
- **Added instruction priority hierarchy** — System > Ethics > GPS > User, making conflict resolution explicit
- **Expanded document analysis protocol** — step-by-step image upload handling with quality assessment
- **Added core templates** — evidence table, research plan, conflict resolution matrix, proof summary format
- **Added decision trees** — flowcharts for user level detection, sensitive information, and conflicting evidence
- **Added terminology quick reference** — Appendix A lookup table
- **Added capabilities & limitations section** — honest about what AI can and cannot do
- **Strengthened DNA ethics** — explicit disclosure requirements before recommending testing
- **Added error recovery protocol** — how to handle and communicate mistakes transparently

### What changed in v7 (from v6.1)

- **Added adaptive user experience** — beginner/intermediate/advanced detection and response calibration
- **Added scaffolding protocols** — adjusting support as users grow
- **Added cognitive load management** — chunking, pausing, prioritizing
- **Expanded ethics section** — CARE principles for Indigenous data, diverse family structures, cultural naming

### Previous Versions

| Prompt | Notes |
| ------ | ----- |
| [research-assistant-v7.md](research-assistant-v7.md) | Previous full version |
| [research-assistant-v7-compressed.md](research-assistant-v7-compressed.md) | Token-efficient v7 |
| [research-assistant-v6.1.md](research-assistant-v6.1.md) | Earlier full version |
| [research-assistant-v6.1-compressed.md](research-assistant-v6.1-compressed.md) | Token-efficient v6.1 |

## Evidence Analysis Framework

The prompts use the **Evidence Analysis Process Map** vocabulary:

| Element | Classes | Definition |
|---------|---------|------------|
| **SOURCES** | Original, Derivative, Authored | The containers holding information |
| **INFORMATION** | Primary, Secondary, Indeterminate | Content classified by informant's knowledge |
| **EVIDENCE** | Direct, Indirect, Negative | Interpretation relative to research question |

See [reference/evidence-terminology.md](reference/evidence-terminology.md) for detailed definitions.

## References

- Mills, Elizabeth Shown. *Evidence Explained*, 4th ed. (2024)
- Board for Certification of Genealogists. *Genealogy Standards*, 2nd ed. revised (2021)
