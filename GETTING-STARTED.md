<!-- markdownlint-disable MD013 -->

# Getting Started with Open-Genealogy

Open-Genealogy is a public collection of AI-assisted genealogy workflows,
prompts, and supporting files. The current research route is GRA v9.2.0,
available as a v9.2.1 Agent ZIP or a v9.2.0 Chat text file. Both use v9.2.0 research instructions.

## Before You Upload Or Share Records

Standard Codex, Claude, ChatGPT, Gemini, and other hosted AI workflows process
the content they read with a cloud model. A local folder is not the same thing
as a local model. Do not upload or grant access to a living person's address,
contact information, employment, medical, financial, or other sensitive
details. If a record is too sensitive for the chosen service, keep it out of
that service.

Before sharing a draft, read it as someone who knows the family. In tests,
GRA sometimes suggested including a living person's line of work or town.
Those two clues together can identify someone. Remove identifying details
from the copy you share. If a reply includes a private list of real names
and their substitutes, keep that list in your private notes.

AI can help organize, extract, compare, plan, and draft. It does not certify a
genealogical conclusion. Verify every record, citation, inference, and final
conclusion yourself.

## Start With GRA v9.2.0

Choose one route. A first-time reader reaches either current edition directly
from this page.

| Choose | When it fits | Start here |
| --- | --- | --- |
| **GRA Agent ZIP v9.2.1** | Your app supports installing a skill from a ZIP or local folder | [Download the v9.2.1 Agent ZIP](https://github.com/DigitalArchivst/Open-Genealogy/releases/download/gra-agent-packager-v9.2.1/gra-skill-v9.2.1.zip) |
| **GRA v9.2.0 Chat Edition** | You want a self-contained prompt for ordinary chat, a Custom GPT, a Gem, or a project | [Direct v9.2.0 chat download](https://github.com/DigitalArchivst/Open-Genealogy/releases/download/v9.2.0/research-assistant-v9.2.0-chat.md) |

The Agent Skill and Chat Edition share one GPS-aligned methodology. The Agent
Skill adds client-dependent file and reference features. The Chat Edition is the
copy-paste form. The [GRA page](skills/gra/README.md) contains direct immutable
source links, installation guidance, and a platform matrix that separates
documented native support from expected compatibility.

## Current Setup Paths

### Chat Edition

1. Open the [v9.2.0 Chat Edition](https://github.com/DigitalArchivst/Open-Genealogy/releases/download/v9.2.0/research-assistant-v9.2.0-chat.md).
2. Copy the complete prompt into the instruction or system-prompt field your
   chat platform provides, or paste it at the beginning of a new conversation.
3. Provide only the research question, transcription, or record material you
   are comfortable processing in that platform.
4. Ask for a source-bounded analysis and verify the response against the record.

### Agent Skill

1. [Download the Agent ZIP v9.2.1](https://github.com/DigitalArchivst/Open-Genealogy/releases/download/gra-agent-packager-v9.2.1/gra-skill-v9.2.1.zip). Your browser saves `gra-skill-v9.2.1.zip`.
2. Use the row for your app. For the two folder-based options, extract the ZIP in your file manager and copy the whole `gra` folder. Its `SKILL.md` file identifies the runtime as v9.2.0.
3. Open a new session in the project and ask it to use the Genealogical Research Assistant on the public records below. The [packager release notes](https://github.com/DigitalArchivst/Open-Genealogy/releases/tag/gra-agent-packager-v9.2.1) give the archive checksum.

| App | Where the skill goes |
| --- | --- |
| Claude with skill uploads enabled | Open **Customize → Skills**, upload the downloaded ZIP, and enable the skill. [Claude help](https://support.claude.com/en/articles/12512180-use-skills-in-claude) |
| Claude Code | Inside your project folder, place the skill at `.claude/skills/gra/SKILL.md`, with its supporting files alongside it. [Claude Code skill locations](https://code.claude.com/docs/en/skills) |
| Codex | Inside your project folder, place the skill at `.agents/skills/gra/SKILL.md`, with its supporting files alongside it. [Codex skill locations](https://developers.openai.com/codex/skills) |

Do not assume that an Agent Skills-compatible ZIP has a universal installer.
The package was release-validated, but interactive installation was not
rechecked for every named client.

## Trace the Adams family backward

John Adams Morgan, the Olympic sailor, died on January 23, 2025. His family memorial names his mother, Catherine Lovering Adams Morgan. In the Pierpont genealogy, the couple Henry Sturgis Morgan and Catherine Adams appear above the entry for their son John, born September 17, 1930. Open the two sources and compare the names and birth date. [Morgan memorial](https://everloved.com/life-of/john-adams-morgan/obituary/) · [Pierpont genealogy, entries 162323124 and 1623231244](https://ccat.sas.upenn.edu/rak/gen/pier/piergenn.htm)

Paste this question into either edition:

> John Adams Morgan’s memorial names Catherine Lovering Adams Morgan as his mother. A separately published family genealogy places John Adams Morgan, born September 17, 1930, among the children of Henry Sturgis Morgan and Catherine Adams. These are my abstracts. Who is the first parent on the Adams line? What details connect the two accounts, and which information would you still want to verify?

Then follow the worked case through six parent-child relationships. It shows how the maternal surname changes, how dates distinguish two men named John Quincy Adams, and which record identifies the father of the Navy secretary Charles Francis Adams III. [Work backward from Morgan to President John Adams](research/adams-family-case.md)

## Starter Workspace

The [Genealogy AI Starter Workspace](genealogy-ai-starter-workspace/README.md)
is a ready-to-use local project folder with logs, templates, sample records,
and instructions for a cautious first research session. Its README gives exact
whole-repository download, extraction, and client folder-selection instructions.

## Find Other Tools

Use [INDEX.md](INDEX.md) as the current catalog for transcription, image
analysis, writing, GEDCOM, and other topics. Read each tool's privacy and
capability boundaries before sending it a document, photo, audio file, or GEDCOM
file.

## Legacy Compatibility Walkthrough

The earlier long GRA v8 walkthrough has been replaced by this v9.2.0-first
guide. Its v8 and v7 action steps are no longer current recommendations. The
frozen historical walkthrough remains available for article links, prior
teaching materials, and comparison:

- [Frozen GRA v8 legacy guide](GETTING-STARTED-v8-legacy.md)

- [v8.5 compatibility files](research/README.md#v85-compatibility-files)
- [v7 and earlier files](research/README.md#v7-and-earlier-files)
- [GRA v8.5 legacy table](skills/gra/README.md#legacy-v85-continuity)

If an earlier article directs you to v8.5, you may use that preserved artifact
for context or continuity, but begin a new workflow with GRA v9. The
[research history page](research/README.md) identifies the exact alias pairs
and the canonical navigation entry for each pair.

## Downloading the Repository

For the starter workspace or several related tools, download the whole
repository rather than trying to download a single GitHub folder:

1. Visit [Open-Genealogy on GitHub](https://github.com/DigitalArchivst/Open-Genealogy), select **Code**, then **Download ZIP**; or use the direct [whole-repository ZIP](https://github.com/DigitalArchivst/Open-Genealogy/archive/refs/heads/main.zip).
2. Download the ZIP archive.
3. Extract the downloaded archive.
4. Open the needed subfolder inside the extracted `Open-Genealogy-main` folder,
   such as `genealogy-ai-starter-workspace`.

The audited releases include GRA runtime packages, not a separately verified
starter-workspace ZIP. The whole-repository download is the documented path for
the starter workspace.

## Method Boundary

Open-Genealogy tools are GPS-aligned or designed to follow genealogical method.
They do not enforce, guarantee, or certify the Genealogical Proof Standard. The
genealogist, not the AI, owns the conclusion.

## More Help

- [Current catalog](INDEX.md)
- [Current GRA v9.2.0 Agent Skill and Chat Edition](https://github.com/DigitalArchivst/Open-Genealogy/tree/v9.2.0/skills/gra)
- [Historical annotated index](ANNOTATED-INDEX.md)
- [Historical tour](TOUR-REPORT.md)

## License

[Creative Commons BY-NC-SA 4.0](LICENSE) covers Steve-authored content within
its stated scope. It does not automatically cover third-party, historical, or
limited-permission media. Consult [RIGHTS.md](RIGHTS.md) and the [Rights and
License Matrix](docs/RIGHTS-AND-LICENSE-MATRIX.md) before reusing material with
separate rights.
