# Open-Genealogy

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![GitHub last commit](https://img.shields.io/github/last-commit/DigitalArchivst/Open-Genealogy)](https://github.com/DigitalArchivst/Open-Genealogy/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/DigitalArchivst/Open-Genealogy)](https://github.com/DigitalArchivst/Open-Genealogy)

A toolkit of **AI prompts and utilities for genealogical research**, designed to
follow the Genealogical Proof Standard (GPS). For genealogists at every level — from
hobbyists exploring their first census record to credentialed professionals
managing client work.

## Get started with the Genealogical Research Assistant

Before copying, pasting, or uploading a record: standard Codex, Claude, and
other hosted AI workflows process the material with a cloud model. Do not send
living-person details or any record that is too sensitive for the service you
choose. Treat every AI response as draft analysis; verify records, citations,
and conclusions yourself.

**[Download the GRA Agent ZIP v9.2.1](https://github.com/DigitalArchivst/Open-Genealogy/releases/download/gra-agent-packager-v9.2.1/gra-skill-v9.2.1.zip)** if your app supports Agent Skills. The package contains the v9.2.0 research instructions. Seeing v9.2.0 inside the ZIP is expected. [Installation steps](GETTING-STARTED.md#agent-skill) · [Release notes and checksum](https://github.com/DigitalArchivst/Open-Genealogy/releases/tag/gra-agent-packager-v9.2.1)

### Start With GRA v9.2.0

**Using a regular chat window?** [Read and copy the Chat Edition](https://github.com/DigitalArchivst/Open-Genealogy/blob/v9.2.0/research/research-assistant-v9.2.0-chat.md) or [download the text file](https://github.com/DigitalArchivst/Open-Genealogy/releases/download/v9.2.0/research-assistant-v9.2.0-chat.md). Paste the instructions into a new conversation. The [Agent download above](#get-started-with-the-genealogical-research-assistant) uses the same research methodology. [Try your first research question](GETTING-STARTED.md#trace-the-adams-family-backward)

GRA v8.5, v8, and v7 remain available under the documented
[compatibility and history route](research/README.md#compatibility-and-history).

## What's Here

- **[Trifecta Complete Reference](reference/trifecta/)**
  - Description: Full guide to one genealogist, two AI assistants, one folder, and GRA v9.2
  - Start Here: [Reference guide and chatbot-accessible Markdown](reference/trifecta/README.md)
- **[Genealogy AI Starter Workspace](genealogy-ai-starter-workspace/)**
  - Description: Project-folder starter kit for Codex, Claude Code, and Cowork
  - Start Here: [README.md](genealogy-ai-starter-workspace/README.md)
- **[Research](research/)**
  - Description: Current GRA v9.2.0 Chat Edition plus retained research history
  - Start Here: [v9.2.0 Chat Edition](https://github.com/DigitalArchivst/Open-Genealogy/releases/download/v9.2.0/research-assistant-v9.2.0-chat.md)
- **[GRA Agent Skill](GETTING-STARTED.md#agent-skill)**
  - Description: GRA v9.2.1 Agent ZIP with the v9.2.0 research instructions and supporting references
  - Start Here: [Install the Agent Skill](GETTING-STARTED.md#agent-skill)
- **[Transcription](transcription/)**
  - Description: Diplomatic transcription for handwritten documents
  - Start Here: [ocr-htr-v08.md](transcription/ocr-htr-v08.md)
- **[Image Analysis](image-analysis/)**
  - Description: Forensic image interpretation for historical photographs
  - Start Here: [deep-look-v2.md](image-analysis/deep-look-v2.md)
- **[Hebrew Headstones](hebrew-headstones/)**
  - Description: Jewish cemetery headstone analysis with gematria dating
  - Start Here:
    [hebrew-headstone-helper-v9.md](hebrew-headstones/hebrew-headstone-helper-v9.md)
- **[Photo Restoration](photo-restoration/)**
  - Description: Historical photograph restoration
  - Start Here: [restoration-v2.md](photo-restoration/restoration-v2.md)
- **[Writing Tools](writing-tools/)**
  - Description: Narrative writing, web briefing, fact extraction, language
    advising, editing
  - Start Here:
    [narrative-assistant-v3.md](writing-tools/narrative-assistant-v3.md)
- **[Assistants](assistants/)**
  - Description: AI personas, GEDCOM creation and analysis
  - Start Here: [gedcom-builder-v1.md](assistants/gedcom-builder-v1.md)
- **[GPT Configs](gpt-configs/)**
  - Description: Custom GPT system prompts for OpenAI deployments
  - Start Here: [README.md](gpt-configs/README.md)
- **[Skills](skills/)**
  - Description: Agent Skills for compatible clients, with supporting files
  - Start Here: [skills/](skills/)
- **[Scripts](scripts/)**
  - Description: Privacy-aware batch and long-audio transcription utilities
  - Start Here: [batch_transcribe_v2.py](scripts/batch_transcribe_v2.py)
- **[Media](media/)**
  - Description: Audio explainers and supporting media
  - Start Here: [README.md](media/README.md)
- **[Benchmark](benchmark/)**
  - Description: AI research evaluation framework
  - Start Here: [README.md](benchmark/README.md)

**Full catalog:** [INDEX.md](INDEX.md) | **Detailed guide:**
[GETTING-STARTED.md](GETTING-STARTED.md) | **Historical v8 guide:**
[GETTING-STARTED-v8-legacy.md](GETTING-STARTED-v8-legacy.md) | **Guided tour:**
[TOUR-REPORT.md](TOUR-REPORT.md)

## Quick Start

1. Read the privacy and living-person boundary above.
2. Choose the Agent ZIP or the Chat Edition above.
3. Follow the [Getting Started guide](GETTING-STARTED.md) for your edition.
4. Provide only material you are comfortable processing with the selected tool.
5. Verify the resulting analysis against the records.

New here? The [Getting Started guide](GETTING-STARTED.md) walks through setup,
first use, and common workflows.

## Featured: GPS Research Methodology

The **research/** folder contains prompts designed to follow the
[Genealogical Proof Standard](https://bcgcertification.org/ethics-standards)—the
professional methodology for evidence-based genealogical conclusions.

Key features:

- **Evidence Analysis Process Map**: Classifies sources
  (Original/Derivative/Authored), information (Primary/Secondary), and evidence
  (Direct/Indirect/Negative)
- **Epistemic transparency**: Separates what sources state from inference from
  uncertainty
- **Conflict resolution**: Explicit protocols for handling contradictory
  evidence

Aligned with the methodology described in:

- Mills, _Evidence Explained_, 4th ed. (2024)
- BCG, _Genealogy Standards_, 2nd ed. revised (2021)

## Benchmark

The **benchmark/** folder preserves four historical model outputs and a teaching
rubric for close reading. The retained evidence does not support a reproducible
model ranking; read the benchmark's current methodology notice before using it.

## Notice

This toolkit applies widely recognized genealogical research principles. It is
not published by, endorsed by, or affiliated with Elizabeth Shown Mills, the
Board for Certification of Genealogists, or any certifying body. References to
published standards indicate methodological alignment, not authorization or
derivation.

## License

[Creative Commons BY-NC-SA 4.0](LICENSE) covers Steve-authored content within
its stated scope. It does not automatically cover third-party, historical, or
limited-permission media included in the repository. Read [RIGHTS.md](RIGHTS.md)
and the [Rights and License Matrix](docs/RIGHTS-AND-LICENSE-MATRIX.md) before
reusing an image, audio file, captured model output, quotation, or other
material that may have separate rights.

## Help and feedback

For an installation problem, [open an issue](https://github.com/DigitalArchivst/Open-Genealogy/issues/new/choose) with your app, edition, and the step that failed. Describe the problem without including private family details. For a security or data-exposure concern, use the [private reporting route](SECURITY.md).

## Author

**Steve Little** ([@DigitalArchivst](https://github.com/DigitalArchivst))
