# Deep Look v2 Four-Model Methodology Note

> [!CAUTION]
> **Current interpretation of the preserved companion PDF:** it is not a controlled model comparison. The overall winner, controlled-comparison, and categorical no-fabrication conclusions are withdrawn pending comparable reruns and a claim-level ground-truth record.

This note applies to [Deep-Look-v2-Four-Models-Full-Results.pdf](Deep-Look-v2-Four-Models-Full-Results.pdf). The PDF and its captured outputs are preserved as a historical teaching artifact. This note records the current editorial assessment without altering that evidence.

## Context Contradiction

Page 1 says, "No model received any context about the family, the location, or the date." Page 5 later says Claude had genealogical context in the interactive session and that an API blind run would not have identified Ashe County.

Those statements cannot both describe the same controlled condition. The retained report also does not disclose enough per-model detail to reconstruct the actual context, interface, tools, settings, and retrieval state for every run. The exercise therefore cannot isolate model behavior from differences in supplied context or execution conditions.

## Context-Tainted Scoring Margin

The scoring matrix gives Claude `71/84` and GPT-5.4 `68/84`, a three-point overall margin. In the Geography category, where the report itself discloses Claude's context advantage, Claude receives `5/5` and GPT-5.4 receives `3/5`. Those two points account for two of the three points in the reported overall winning margin.

Because a materially unequal category supplies most of the margin, the statement that Claude "wins overall" is not supported as a controlled comparative conclusion. The numeric matrix may still be studied as a record of the evaluator's historical scoring, but it should not be generalized to current models or used for model selection.

## No-Fabrication Claim

Page 9 says that no model fabricated data. The packet does not retain a claim-level ground-truth table showing every output assertion, its image anchor or external support, the evaluator's verification result, and any adjudication.

The categorical no-fabrication conclusion is therefore withdrawn. At most, the report records that the evaluator did not identify an obvious fabrication during that exercise. That bounded observation is not proof that every claim was accurate or image-grounded.

## What Remains Useful

The PDF preserves four substantial outputs, a common analysis prompt, an evaluator's scoring approach, and examples of uncertainty language. It can support:

- Close reading of how models organize visual analysis
- Discussion of observation, inference, and speculation
- Identification of claims that need image anchors or external verification
- Critique of scoring categories and evaluator assumptions
- Design of a stronger controlled comparison

It cannot currently support a model winner, a claim that context was controlled, or a categorical claim that no model fabricated data.

## Requirements for a Comparable Rerun

A future comparison should retain and publish:

- The exact image bytes, prompt, task, and any system or project instructions
- A dated manifest with exact model/version identifiers and settings
- The interface or API used for each run
- All family, location, date, and genealogical context supplied to each model
- Browsing, vision, code, retrieval, and other tool state for each run
- Unedited outputs and tool or retrieval logs
- A claim-level ground-truth log with image regions or external sources
- A scoring guide, criterion-level score sheets, scorer calibration, and adjudication notes
- Separate results for observational accuracy, writing quality, completeness, uncertainty calibration, and reproducibility

Only comparable reruns with that record can support a controlled model comparison. A no-fabrication conclusion additionally requires complete claim-level verification against the image and any external facts used.
