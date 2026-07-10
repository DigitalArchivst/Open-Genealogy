<!-- markdownlint-disable MD013 -->

# Research: Current GRA v9.2.0 And Retained History

This folder preserves the research-prompt history of Open-Genealogy. For a new
research workflow, begin with GRA v9.2.0 below. The earlier v9.0.0, v8.5, v8,
v7, and v6.1 files remain at their existing paths for compatibility and historical
study.

## Safety Before Upload

Hosted AI tools can process the text, images, and files you provide with their
cloud services, even when the files began on your computer. Do not upload a
living person's address, contact information, medical, financial, employment,
or other sensitive details. If a record is too sensitive for the service you
choose, do not send it. AI output is draft analysis: the human genealogist
verifies records, citations, reasoning, and conclusions.

## Current GRA v9.2.0

Choose the edition that matches how you work:

| Choose | Best for | Start here |
| --- | --- | --- |
| **Agent Skill** | An Agent Skills client with local-folder and reference-file support | [GRA v9.2.0 release source](https://github.com/DigitalArchivst/Open-Genealogy/tree/v9.2.0/skills/gra) |
| **Chat Edition** | Custom GPTs, Gems, projects, and ordinary copy-paste chat | Direct [v9.2.0 chat download](https://github.com/DigitalArchivst/Open-Genealogy/releases/download/v9.2.0/research-assistant-v9.2.0-chat.md) and immutable [repository artifact](https://github.com/DigitalArchivst/Open-Genealogy/blob/v9.2.0/research/research-assistant-v9.2.0-chat.md) |

Both editions use the same v9.2.0 methodology. The Agent Skill adds agent-only
features where the client supports them; the Chat Edition is the self-contained
copy-paste form. Installation behavior varies by client; do not assume that an
Agent Skills ZIP installs the same way in every client.

## Compatibility And History

The following files are preserved. They are not the current GRA recommendation.
Their historical language and behavior may differ from v9, including its
current privacy, human-verification, and GPS-alignment boundaries.

### v8.5 Compatibility Files

| Path | Historical content | Status |
| --- | --- | --- |
| [research-assistant-v8.5-compact.md](research-assistant-v8.5-compact.md) | v8.5.2c compact prompt | Canonical compact v8.5 compatibility entry |
| [research-assistant-v8.5-compact-unwrapped.md](research-assistant-v8.5-compact-unwrapped.md) | v8.5.2c compact prompt | Exact byte-for-byte compatibility alias of the canonical compact entry |
| [research-assistant-v8.md](research-assistant-v8.md) | Full v8 prompt | Retained historical full prompt |
| [research-assistant-v8-compact.md](research-assistant-v8-compact.md) | Compact v8 prompt | Retained historical compact prompt |

### v7 And Earlier Files

| Path | Historical content | Status |
| --- | --- | --- |
| [research-with-citations-v7.md](research-with-citations-v7.md) | v7 web-research prompt | Canonical entry for this retained v7 prompt |
| [web-research-v7.md](web-research-v7.md) | v7 web-research prompt | Exact byte-for-byte compatibility alias of `research-with-citations-v7.md` |
| [research-assistant-v7.md](research-assistant-v7.md) | Full v7 prompt | Archive |
| [research-assistant-v7-compressed.md](research-assistant-v7-compressed.md) | Compressed v7 prompt | Archive |
| [research-assistant-v6.1.md](research-assistant-v6.1.md) | Full v6.1 prompt | Archive |
| [research-assistant-v6.1-compressed.md](research-assistant-v6.1-compressed.md) | Compressed v6.1 prompt | Archive |

The two alias pairs are preserved because older links may point to either path:

1. `research-assistant-v8.5-compact.md` and
   `research-assistant-v8.5-compact-unwrapped.md`
2. `research-with-citations-v7.md` and `web-research-v7.md`

No alias is a second current recommendation. Do not rename, delete, or
consolidate these files without first checking inbound links and release
history.

### Other Retained Research Material

- [contract-first-genealogy-v3.1.md](contract-first-genealogy-v3.1.md):
  historical structured-project workflow; use only after reading its own
  limitations and privacy boundary.
- [research-agent-assignment-v2.1.md](research-agent-assignment-v2.1.md):
  retained general research-agent framework, not a current GRA workflow.
- [genealogy-record-analysis-prd.md](genealogy-record-analysis-prd.md): dated
  design reference, not operational instructions.
- [evidence terminology](reference/evidence-terminology.md): reference for the
  Source / Information / Evidence distinction.
- [research archive](archive/): older preserved experiments and prompts.

## Method Boundary

GRA is GPS-aligned and designed to support careful research. It does not
enforce or guarantee the Genealogical Proof Standard. A genealogist must review
the records, evaluate the reasoning, resolve conflicts, and own the conclusion.

## Historical Version Notes

The detailed v8 and v7 history remains in the retained files for readers who
need it. Current lifecycle and release information is maintained in
[CHANGELOG.md](../CHANGELOG.md). For v8.5 package and historical-path detail,
see the [GRA legacy table](../skills/gra/README.md#legacy-v85-continuity).
