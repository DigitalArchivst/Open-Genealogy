# Historical AI Research Specimens and Writing Evaluation

> [!CAUTION]
> **Historical specimen set, not a reproducible model benchmark.** The four preserved Ashe County outputs remain useful for teaching evaluation and failure analysis, but the retained packet does not support a precise aggregate score, model ranking, or claim that differences were isolated to model behavior. The previously published `88.75%` ranking is withdrawn from current guidance pending recovery or creation of a complete run and scoring record.

This section contains a rubric for evaluating published genealogical writing and a preserved set of AI-generated historical-research outputs. Read the [Ashe County methodology and annotations](case-studies/ashe-county-nc/README.md) before using the specimens.

## Rubric

| Resource | Purpose |
| --- | --- |
| [Genealogical Writing Evaluation Rubric](rubrics/genealogical-writing-rubric.md) | 60-point rubric for evaluating observable qualities of published genealogical writing |

The rubric evaluates evidentiary presentation, narrative writing, and genealogical utility. Its score is a **published-writing evaluation**, not a measure of factual accuracy, research exhaustiveness, GPS alignment, model quality, or run reproducibility.

## Historical Case Study

### [Ashe County, North Carolina (1492-1799)](case-studies/ashe-county-nc/README.md)

The packet preserves four outputs that were presented as responses to a common research prompt based on [research-with-citations-v7.md](../research/research-with-citations-v7.md). The repository does not retain enough evidence to establish the exact task or comparable run conditions.

| Historical model label | Preserved output | Current annotation |
| --- | --- | --- |
| Claude | [Raw specimen](case-studies/ashe-county-nc/claude.md) | [Missing run and retrieval provenance; only citation `[1]` carries a 2024 access date](case-studies/ashe-county-nc/README.md#claude) |
| ChatGPT | [Raw specimen](case-studies/ashe-county-nc/chatgpt.md) | [Not independently fact-checked or reproducibly scored](case-studies/ashe-county-nc/README.md#chatgpt) |
| Gemini | [Raw specimen](case-studies/ashe-county-nc/gemini.md) | [Not independently fact-checked or reproducibly scored](case-studies/ashe-county-nc/README.md#gemini) |
| Grok | [Raw specimen](case-studies/ashe-county-nc/grok.md) | [Uncited narrative claims, bibliography gaps, and misuse of Direct Evidence](case-studies/ashe-county-nc/README.md#grok) |

No current model ranking is asserted from these files.

## Evidence Required for Future Comparisons

Any future benchmark claim should retain and publish:

- A dated run manifest and the exact task and prompt supplied to every model
- The source corpus or retrieval scope available to each run
- Model and version identifiers, settings, interface, and run date
- Browsing, search, tool, and retrieval state for each model
- Unedited raw outputs and retrieval logs
- Criterion-level score sheets and calculation details
- Scorer identity or role, calibration procedure, and inter-rater record when applicable
- Claim-level fact checks, conflict notes, and adjudication decisions

Results should report writing quality, factual accuracy, research exhaustiveness, GPS alignment, and reproducibility as separate dimensions. A score in one dimension cannot stand in for the others.

## Contributing Case Studies

Additional case studies can strengthen the framework when they include the evidence package above. Useful topics include:

- Immigrant research involving multiple languages and identity across jurisdictions
- African American genealogy involving enslavement and indirect evidence
- Colonial-era research involving limited documentation and cluster research

## Methodology Status

The preserved Ashe County files can support close reading, rubric practice, error spotting, and discussion of source use. They cannot support a controlled comparison of model behavior until comparable runs and complete evaluation evidence are available.
