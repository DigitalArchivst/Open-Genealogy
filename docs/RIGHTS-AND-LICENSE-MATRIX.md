# Rights and License Matrix

Use this page to decide when the repository's root [LICENSE](../LICENSE) is enough and when you need to check a file's own rights notice first. The license does not automatically cover third-party, historical, or limited-permission media merely because it appears in this repository.

The controlling path-by-path policy is [RIGHTS.md](../RIGHTS.md). This guide highlights the most common cases; it does not add a license or change a local rights notice.

## Quick Guide

| Material | What to do before reuse | Where to check |
| --- | --- | --- |
| Steve-authored prompt, guide, or other repository content with no narrower notice | Follow the root `CC-BY-NC-SA-4.0` terms and provide attribution. | [Root LICENSE](../LICENSE) and [RIGHTS.md](../RIGHTS.md) |
| A file with its own license or permission statement | Follow that local statement; do not assume the root license adds terms. | The file and the matching row in [RIGHTS.md](../RIGHTS.md) |
| Historical image, quotation, logo, trademark, captured model output, or source excerpt | Treat it as excluded unless the item has a documented rights notice or permission. | [RIGHTS.md](../RIGHTS.md) and the item's local `RIGHTS.md`, if present |
| Sample record image, audio file, or mixed PDF | Check the item-level provenance and reuse statement before sharing or adapting it. | [RIGHTS.md](../RIGHTS.md), `genealogy-ai-starter-workspace/records/RIGHTS.md`, or `media/RIGHTS.md` |
| A status marked unresolved | Do not infer a Creative Commons version or grant. Seek the rights holder's permission or choose different material. | [RIGHTS.md](../RIGHTS.md) |

## Common Path Categories

| Path or material | Rights status | Reuse reminder |
| --- | --- | --- |
| Most Steve-authored repository content | `CC-BY-NC-SA-4.0` baseline | Attribution, noncommercial use, and compatible ShareAlike terms apply where Steve owns the copyrightable content. |
| `gpt-configs/open-geneagpt-v0.4.txt`; `gpt-configs/website-frontend-v3.txt` | Local `CC-BY-4.0` exception | Follow the local exception rather than the repository baseline. |
| Selected older transcription and photo-conservator files | Local `CC-BY-NC-4.0` exception | ShareAlike is not added by this matrix. |
| `image-analysis/deep-look-v2.md`; selected restored GRA files; `writing-tools/narrative-assistant-v3.md` | Unresolved or informal local statement | Do not convert shorthand or informal permission into a guessed Creative Commons grant. |
| Sample record images, audio, historical images, and captured model outputs | Excluded or authorship uncertain | Repository access does not grant reuse permission. |
| `skills/gedcom-creator/scripts/gedcom_builder.py` | MIT code exception | The MIT grant applies only to that script; accompanying prose remains under the applicable authored-content terms. |

## Machine-Readable Data

[LICENSE-MATRIX.json](../LICENSE-MATRIX.json) records the same policy in a machine-readable form. A `null` SPDX expression deliberately means that the repository does not establish a reuse license for that material.
