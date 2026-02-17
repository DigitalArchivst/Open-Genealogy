# GPS Evaluation Framework

A framework for evaluating AI-generated historical research against GPS methodology. The rubric is the centerpiece; case studies demonstrate its application.

## Rubric

| Resource | Purpose |
| -------- | ------- |
| [genealogical-writing-rubric.md](rubrics/genealogical-writing-rubric.md) | 60-point GPS-derived rubric for evaluating published genealogical writing |

The rubric evaluates published genealogical writing (blog posts, articles, family histories, compiled genealogies) across two layers: **Evidentiary Foundation** (GPS-derived criteria) and **Writing Quality** (narrative effectiveness). Each criterion is scored 1-5.

## Case Studies

### [Ashe County, NC (1492-1799)](case-studies/ashe-county-nc/)

Four models tested on the same research question using [research-with-citations-v7.md](../research/research-with-citations-v7.md):

| Model | Output |
| ----- | ------ |
| Claude | [claude.md](case-studies/ashe-county-nc/claude.md) |
| ChatGPT | [chatgpt.md](case-studies/ashe-county-nc/chatgpt.md) |
| Gemini | [gemini.md](case-studies/ashe-county-nc/gemini.md) |
| Grok | [grok.md](case-studies/ashe-county-nc/grok.md) |

**Key findings:**
- ChatGPT scored highest overall (88.75%) — best methodology compliance
- Gemini provided most genealogical leads
- All models struggled with evidence classification (Direct/Indirect/Negative)

## Contributing Case Studies

Additional case studies strengthen the evaluation framework. If you've run the research prompts on a different topic and want to share results, see the repository's contribution guidelines or open an issue.

Topics that would diversify the benchmark:

- Immigrant research (multi-language records, identity across jurisdictions)
- African American genealogy (enslaved ancestors, indirect evidence)
- Colonial-era records (limited documentation, cluster research)

## Methodology

Each case study uses the same prompt across all tested models, then evaluates outputs using the rubric. This controls for prompt quality and isolates model behavior.
