<!-- markdownlint-disable MD013 -->

# Genealogical Research Assistant v9.2 Agent Skill

GRA v9.2 is a GPS-aligned research assistant for source-bounded genealogical
analysis. It is instructed not to invent records, citations, people, dates,
places, or events, but AI can still err. Verify every record, citation,
inference, and conclusion before relying on or publishing it.

## Release Status

v9.2.0 is the current release. Its [Agent Edition](SKILL.md), generated
[Chat Edition](https://github.com/DigitalArchivst/Open-Genealogy/releases/download/v9.2.0/research-assistant-v9.2.0-chat.md), references,
fixtures, and packaging checks are maintained together. The
[v9.0.0 release](https://github.com/DigitalArchivst/Open-Genealogy/releases/tag/v9.0.0)
and all retained v8.5 links and historical artifacts remain unchanged.

## Choose An Edition

| Choose | Use it when | v9.2.0 release artifact |
| --- | --- | --- |
| **Agent Skill** | Your client supports a local Agent Skills folder and you want the compact skill plus reference files | Download [gra-skill-v9.2.0.zip](https://github.com/DigitalArchivst/Open-Genealogy/releases/download/v9.2.0/gra-skill-v9.2.0.zip) or inspect the [release source](https://github.com/DigitalArchivst/Open-Genealogy/tree/v9.2.0/skills/gra) |
| **Chat Edition** | You want a self-contained prompt for chat, a Custom GPT, a Gem, or a project | Download [research-assistant-v9.2.0-chat.md](https://github.com/DigitalArchivst/Open-Genealogy/releases/download/v9.2.0/research-assistant-v9.2.0-chat.md) |

The two editions share one methodology. The Agent Skill can use file access,
references, structured output, and verification offers only when the client
and permissions allow. The Chat Edition omits those agent-only surfaces.

## Safety Before Uploading Records

Using a local folder does not make a hosted AI model local. Standard Codex,
Claude Code, Claude Cowork, ChatGPT, and Gemini workflows may process the text
or files they read with a cloud model. Do not upload or grant access to
living-person addresses, contact information, employment, medical, financial,
or other sensitive details. If material is too sensitive for the chosen
service, keep it out of that service. A human genealogist remains responsible
for the research conclusion.

## Platform And Installation Matrix

The v9.2 ZIP was built from an explicit six-file allowlist, extracted, and
structurally validated. Interactive installation was not rerun in every named
client. The matrix deliberately separates
native support documented by a platform from expected standards-based
compatibility.

| Platform | Support status | What was verified | Install or use path |
| --- | --- | --- | --- |
| Claude Desktop / Cowork | Native skill workflow | The v9.2 package passed structural validation; no fresh interactive install was recorded | Download the v9.2 ZIP, then use **Customize > Skills** to upload and enable it |
| Claude Code | Native directory skill workflow | The v9.2 package structure was validated locally; no fresh interactive CLI install was recorded | Build and extract the ZIP so its `gra` folder is inside your Claude skills directory, then restart Claude Code |
| OpenAI Codex | Native skill-directory support | Current Codex documentation was checked; the v9.2 ZIP includes `agents/openai.yaml`; no interactive Codex install was rerun | Build and extract the ZIP so its `gra` folder is inside `$HOME/.agents/skills/` for your user or `.agents/skills/` in the repository, then start or reload Codex in that scope |
| Other Agent Skills clients | Expected compatibility, not verified client support | The v9.2 package follows the Agent Skills layout, but the specification does not define a universal installer | Consult that client's skill-install documentation; do not assume it accepts this ZIP directly |
| ChatGPT, Gemini, and ordinary chat | Chat Edition use, not Agent Skill installation | The generated 7,968-character v9.2 artifact passed the size and provenance checks; no fresh platform-specific configuration test was recorded | Use the released Chat Edition as instructions or copy-paste content, subject to the platform's current file and instruction limits |

### Windows Extraction Examples

These source-build examples must be run from the repository root. They create
the v9.2 package locally and place the unpacked `gra` folder in the
documented skill location. They do not send genealogy records anywhere; the
processing boundary begins only when a client reads your files.

#### Codex

```powershell
$zip = Join-Path $env:TEMP 'gra-skill-v9.2.0.zip'
python scripts/package_gra_skill.py --output $zip
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills" | Out-Null
Expand-Archive -LiteralPath $zip -DestinationPath "$HOME\.agents\skills" -Force
```

For repository-only use, replace `"$HOME\.agents\skills"` with
`".agents\skills"` while your current directory is the repository root. Codex
then sees `.agents\skills\gra\SKILL.md` in that repository.

#### Claude Code

```powershell
$zip = Join-Path $env:TEMP 'gra-skill-v9.2.0.zip'
python scripts/package_gra_skill.py --output $zip
New-Item -ItemType Directory -Force -Path "$HOME\.claude\skills" | Out-Null
Expand-Archive -LiteralPath $zip -DestinationPath "$HOME\.claude\skills" -Force
```

Restart the client after installing. On macOS or Linux, extract the same ZIP so
that the resulting `gra` directory is in the client-specific skills directory.

## Legacy v8.5 Continuity

The paths below remain available because earlier articles and readers may refer
to them. They are historical compatibility material, not v9 substitutes. The
content version is taken from each file's own header; a filename or release tag
does not override that header.

| Retained path | Content version in file | Package or release relationship | Why preserved |
| --- | --- | --- | --- |
| [research/research-assistant-v8.5-compact.md](https://github.com/DigitalArchivst/Open-Genealogy/blob/main/research/research-assistant-v8.5-compact.md) | v8.5.2c | Tracked compatibility prompt; not established as identical to a named release ZIP | Existing compact-prompt links |
| [research/research-assistant-v8.5-compact-unwrapped.md](https://github.com/DigitalArchivst/Open-Genealogy/blob/main/research/research-assistant-v8.5-compact-unwrapped.md) | v8.5.2c | Exact byte-for-byte alias of the preceding path | Existing copy/paste links |
| [skills/gra/research-assistant-v8.5-full.md](https://github.com/DigitalArchivst/Open-Genealogy/blob/main/skills/gra/research-assistant-v8.5-full.md) | v8.5 Draft (Phase 1) | Restored article-linked v8.5.1c-era path; header does not establish equivalence to a release ZIP | Known article URL |
| [skills/gra/companion-reference.md](https://github.com/DigitalArchivst/Open-Genealogy/blob/main/skills/gra/companion-reference.md) | v8.5c Reference | Restored historical companion path; no exact release-package equivalence is established by the audit | Known article URL |
| [skills/gra/references/research-assistant-v8.5-full.md](https://github.com/DigitalArchivst/Open-Genealogy/blob/main/skills/gra/references/research-assistant-v8.5-full.md) | v8.5.2 | Runtime reference included in the v8.5.3 packaging release | v8.5.3 package continuity |

Two repository-wide prompt alias pairs are exact byte-for-byte duplicates:

1. `research/research-assistant-v8.5-compact.md` and `research/research-assistant-v8.5-compact-unwrapped.md`
2. `research/research-with-citations-v7.md` and `research/web-research-v7.md`

The canonical navigation entries are `research-assistant-v8.5-compact.md` and
`research-with-citations-v7.md`; their aliases remain in place for compatibility.
Do not rename, delete, or consolidate either alias without an inbound-link and
release-history review.

Historical release pages remain available: [v8.5.1c](https://github.com/DigitalArchivst/Open-Genealogy/releases/tag/v8.5.1c), [v8.5.2](https://github.com/DigitalArchivst/Open-Genealogy/releases/tag/v8.5.2), [v8.5.3](https://github.com/DigitalArchivst/Open-Genealogy/releases/tag/v8.5.3), and [v9.0.0](https://github.com/DigitalArchivst/Open-Genealogy/releases/tag/v9.0.0). Release ZIPs are historical assets; corrected packages belong in a new reviewed release, not as replacements for an old asset.

## Known v9.2 Limitations

Testing identified two model behaviors that compact instructions did not
eliminate consistently:

- When a record does not name its informant, the model may still suggest a
  likely parent or attending physician and classify the information as Primary.
  Treat an unnamed informant as Indeterminate unless the record itself supports
  a qualified eyewitness classification.
- In name conflicts, the Chat Edition may prefer a fuller form because it
  appears in an Original Source. A source label or fuller spelling does not
  establish authority; any provisional display form needs a fact-specific
  provenance rationale.

These are documented limits, not approved shortcuts. Human review remains
responsible for correcting them. The release fixtures preserve both expectations
for continued improvement.

## What GRA Is And Is Not

GRA analyzes the records, transcriptions, and questions you provide. It is not
a record database, an authenticator for legal purposes, legal advice, or a
guarantee of accuracy. It is GPS-aligned and designed to support careful
research; it does not enforce or certify the Genealogical Proof Standard.

The full v9.2 methodology and supporting templates are bundled in the Agent Skill
under `references/`. Chat users can use the Chat Edition directly and may add
supporting reference files only where their platform allows it.

## Disclosing AI Assistance

When publishing work produced with GRA's help, identify the tool and retain
human responsibility. A starting form is:

> Portions of this work were prepared with the assistance of the Genealogical
> Research Assistant (GRA) v9.2.0 Skill Edition, an AI research aid. All
> sources, citations, and conclusions were independently verified by [author's
> full name] on [date]. The author takes professional responsibility for every
> conclusion.

## License

[Creative Commons BY-NC-SA 4.0](LICENSE)

## Author

**Steve Little** ([@DigitalArchivst](https://github.com/DigitalArchivst))
AI Program Director, National Genealogical Society
