# Getting Started with Open-Genealogy

A guide for genealogists—from hobbyists to credentialed professionals—who want to use AI tools that follow professional standards. This guide covers GitHub basics, navigating the Open-Genealogy repository, and using the flagship Genealogical Research Assistant (GRA v8).

**No programming required.** You'll copy text and paste it into AI tools you already know how to use.

---

## Table of Contents

- [Part 1: GitHub for Family Historians](#part-1-github-for-family-historians)
- [Part 2: The Open-Genealogy Repository](#part-2-the-open-genealogy-repository)
- [Part 3: GRA v8 (Genealogical Research Assistant)](#part-3-gra-v8-genealogical-research-assistant)
- [Part 4: Putting It All Together](#part-4-putting-it-all-together)

---

## Part 1: GitHub for Family Historians

### What is GitHub?

GitHub is a free platform where people share digital tools, documents, and projects. Think of it as a public library for software and text files—anyone can browse, and most content is free to use.

**Why genealogists should care:**

- Free access to specialized tools (like the prompts in this repository)
- Transparent development—you can see exactly what a tool does
- Version history—you can track changes and updates over time
- Community collaboration—tools improve through shared feedback

**What you don't need:**

- Programming skills
- A GitHub account (browsing is free without one)
- Technical expertise beyond basic web browsing

### Key GitHub Concepts

GitHub has its own vocabulary. Here's a translation:

| GitHub Term | Plain English | Genealogy Analogy |
|-------------|---------------|-------------------|
| Repository (repo) | A project folder containing related files | Like a research collection on one family line |
| README | The instruction manual for a project | Like a finding aid at an archive |
| Folder/Directory | Subfolders organizing content | Just like Windows or Mac folders |
| File | An individual document | A single prompt, script, or reference |
| Branch | A version being worked on | Like a draft vs. published report |
| Release | An official, stable version | Like a published edition of a book |
| Commit | A saved change with a note | Like a dated entry in a research log |
| Fork | Someone's personal copy of a project | Like making a photocopy to annotate |

**Terms you can safely ignore** (unless you want to contribute): pull request, merge, clone, push, CI/CD, actions, issues (mostly).

### Navigating GitHub

When you visit a repository like [Open-Genealogy](https://github.com/DigitalArchivst/Open-Genealogy), you'll see:

**The main view:**
- A list of folders and files (like Windows Explorer or Mac Finder)
- A README displayed below the file list (this is the project's front page)
- Tabs across the top: Code, Issues, Pull requests, etc. (you only need "Code")

**To browse:**
1. Click any folder name to open it
2. Click any file name to view its contents
3. Click the repository name (top left) to return to the main page
4. Use the breadcrumb trail to navigate back up

**What the buttons mean:**

| Button | What It Does | Do You Need It? |
|--------|--------------|-----------------|
| Code (green) | Download options | Yes, if downloading files |
| Star | Bookmark the project | Optional—helps you find it later |
| Fork | Make your own copy | Only if contributing |
| Watch | Get notifications | Only if you want updates |
| Issues | Bug reports and requests | Only if reporting problems |

### Getting Files from GitHub

**To copy text content (most common for prompts):**

1. Click the file you want (e.g., `research-assistant-v8.md`)
2. You'll see the file contents displayed
3. Click the "Raw" button (top right of the file view)
4. Select all text (Ctrl+A or Cmd+A)
5. Copy (Ctrl+C or Cmd+C)
6. Paste into your AI tool

**To download a single file:**

1. Click the file to view it
2. Click the "Raw" button
3. Right-click → "Save Page As" (or Ctrl+S / Cmd+S)
4. Save to your computer

**To download the entire repository:**

1. Click the green "Code" button on the main page
2. Select "Download ZIP"
3. Extract the ZIP file on your computer

**Advanced option—cloning:**

If you have Git installed and want automatic updates, you can "clone" the repository. This creates a local copy that can sync with updates. Most users don't need this—downloading ZIP works fine.

### GitHub Best Practices for Genealogists

1. **Bookmark useful repositories** — Star them or save the URL
2. **Read the README first** — It explains what's available and how to use it
3. **Check the INDEX.md** — Many projects (including this one) have a master catalog
4. **Look for status labels** — "recommended," "stable," "legacy," "beta"
5. **Check modification dates** — Recent updates suggest active maintenance
6. **Don't worry about contributing** — Using the tools doesn't require participation
7. **Check back periodically** — Good projects add features and fix issues over time

---

## Part 2: The Open-Genealogy Repository

### What is Open-Genealogy?

Open-Genealogy is a collection of AI prompts and utilities designed for genealogical research. Created by Steve Little, it is designed to follow professional standards—particularly the Genealogical Proof Standard (GPS)—in tools that work with any major AI platform (ChatGPT, Claude, Gemini, etc.).

**Key principles:**

- **GPS methodology** — Prompts guide AI toward the five elements of the Genealogical Proof Standard
- **Correct terminology** — Uses "original source" (not "primary source"), proper evidence classification
- **Anti-fabrication** — Explicit rules preventing AI from inventing sources or citations
- **Adaptability** — Tools adjust to user experience level

**License:** Creative Commons BY-NC-SA 4.0 — Free to use and share with attribution, non-commercial.

**Repository URL:** [github.com/DigitalArchivst/Open-Genealogy](https://github.com/DigitalArchivst/Open-Genealogy)

### Repository Structure

The repository is organized into folders by function:

| Folder | Purpose | When to Use |
|--------|---------|-------------|
| **research/** | GPS methodology prompts | Research questions, document analysis, evidence evaluation |
| **transcription/** | Diplomatic transcription | Handwritten documents, old records, OCR/HTR |
| **image-analysis/** | Forensic image interpretation | Historical photographs, visual evidence, dating images |
| **hebrew-headstones/** | Jewish cemetery headstone analysis | Hebrew/Yiddish inscriptions, gematria dating |
| **photo-restoration/** | Historical photo repair | Damaged, faded, or deteriorated photographs |
| **writing-tools/** | Narrative writing, fact extraction, language advising, editing | Creating narratives, processing notes, editorial cleanup |
| **assistants/** | Full AI personas | Ongoing research sessions, GEDCOM analysis |
| **benchmark/** | AI evaluation framework | Comparing AI model performance against GPS standards |
| **scripts/** | Python utilities | Audio transcription (requires Python) |
| **gpt-configs/** | ChatGPT configurations | Deploying custom GPTs on OpenAI's platform |

### Key Files to Know

| File | Location | Purpose |
|------|----------|---------|
| **README.md** | Root | Project overview and quick start |
| **INDEX.md** | Root | Complete catalog of all prompts and tools |
| **ANNOTATED-INDEX.md** | Root | Detailed descriptions (~125 words each) |
| **research-assistant-v8.md** | research/ | Flagship GPS research prompt |
| **ocr-htr-v08.md** | transcription/ | Primary transcription tool |
| **universal-image-analysis-v3.md** | image-analysis/ | 9-layer forensic image analysis |
| **hebrew-headstone-helper-v9.md** | hebrew-headstones/ | Jewish cemetery headstone analysis |
| **restoration-v2.md** | photo-restoration/ | Universal photo restoration |
| **narrative-assistant-v3.md** | writing-tools/ | GPS-informed narrative writing |
| **evidence-terminology.md** | research/reference/ | 3×3 framework reference |

### Finding the Right Tool

**Start with INDEX.md** — This master catalog lists every prompt with status labels:

- **recommended** — Current best version, use this
- **stable** — Works well, may not have latest features
- **legacy** — Older version, kept for compatibility

**Check folder READMEs** — Each folder has its own README explaining:
- Which prompt to use for which situation
- Differences between versions
- Special considerations

**Match your task:**

| If You Want To... | Use This Folder | Recommended File |
|-------------------|-----------------|------------------|
| Analyze a document | research/ | research-assistant-v8.md |
| Quick web research | research/ | research-with-citations-v7.md |
| Transcribe handwriting | transcription/ | ocr-htr-v08.md |
| Transcribe Jewish documents | transcription/ | jewish-transcription-v2.md |
| Analyze a historical photograph | image-analysis/ | universal-image-analysis-v3.md |
| Read a Jewish cemetery headstone | hebrew-headstones/ | hebrew-headstone-helper-v9.md |
| Restore a photo | photo-restoration/ | restoration-v2.md |
| Write a genealogical narrative | writing-tools/ | narrative-assistant-v3.md |
| Extract facts from text | writing-tools/ | fact-extractor-v4.md |
| Get language/usage advice | writing-tools/ | lingua-maven-v9.md |
| Ongoing research partner | assistants/ | vibe-genealogy-assistant-v4.md |
| Analyze a GEDCOM file | assistants/ | gedcom-analysis-v3.md |

### Using Open-Genealogy Prompts

**Basic workflow:**

1. **Identify your task** — What do you want to accomplish?
2. **Navigate to the appropriate folder** — Click into research/, transcription/, etc.
3. **Find the recommended file** — Check INDEX.md or the folder README
4. **View the file** — Click to open it
5. **Copy the entire prompt** — Use Raw view, select all, copy
6. **Open your AI tool** — ChatGPT, Claude, Gemini, or another
7. **Start a new conversation** — Fresh context works best
8. **Paste the full prompt** — Don't truncate or summarize
9. **Provide your input** — Document image, research question, photo, etc.
10. **Follow the structured output** — The AI will respond according to the prompt's format

**Important:** Always copy the complete prompt. These are carefully designed systems; partial prompts won't work correctly.

### Open-Genealogy Best Practices

1. **Copy the full prompt** — Truncating breaks functionality
2. **Start fresh conversations** — Previous context can interfere
3. **Read the prompt introduction** — Understand what it can and cannot do
4. **Check for updates** — Versions improve over time
5. **Use compact versions when needed** — For AI tools with limited context windows
6. **Combine tools** — Chain workflows: transcribe → extract facts → analyze evidence
7. **Verify independently** — AI assists but doesn't replace your judgment

---

## Part 3: GRA v8 (Genealogical Research Assistant)

### What is GRA v8?

The Genealogical Research Assistant version 8 (GRA v8) is the flagship prompt in the Open-Genealogy repository. It aims to guide any capable AI toward GPS-compliant research practices.

**What it does:**
- Guides AI behavior toward the Genealogical Proof Standard
- Emphasizes correct evidence analysis terminology
- Prevents fabrication of sources, citations, or facts
- Adapts explanations to your experience level
- Provides structured document analysis
- Suggests research strategies consistent with professional methodology

**Think of it as:** An AI assistant configured with detailed instructions following the Genealogical Proof Standard and *Evidence Explained* conventions—available instantly and ready to work with whatever documents or questions you provide.

### The GPS Foundation

GRA v8 is structured around the five elements of the Genealogical Proof Standard:

1. **Reasonably exhaustive research** — Search beyond the obvious; cast a wide net proportional to the question's complexity

2. **Complete, accurate citations** — Every claim cites specific sources with full identification (who, what, when, where, where-within)

3. **Thorough analysis and correlation** — Evaluate each source's origin, information quality, and relationship to your research question

4. **Resolution of conflicting evidence** — When sources disagree, apply systematic evaluation to determine which conclusion the preponderance supports

5. **Coherent written conclusion** — Express findings clearly at the appropriate confidence level (proved, probable, possible, not proved, disproved)

**Why this matters for AI:** Without explicit GPS guidance, AI tools tend to provide answers without source documentation, mix inference with fact, use incorrect terminology, and occasionally fabricate plausible-sounding but nonexistent sources. GRA v8 addresses each of these failure modes.

### The Evidence Analysis Framework

GRA v8 applies the "3×3" model from *Evidence Explained* and *Genealogy Standards*:

**Layer 1: Sources** (the containers holding information)

| Type | Definition | Examples |
|------|------------|----------|
| **Original** | First recording, created at or near the event | Church register at baptism, deed recorded at sale |
| **Derivative** | Copy, transcription, abstract, or image | Microfilm, digitized image, published abstract |
| **Authored** | Compiled work analyzing other sources | County history, compiled genealogy, family history |

**Layer 2: Information** (the content within sources)

| Type | Definition | Examples |
|------|------------|----------|
| **Primary** | From someone with firsthand knowledge | Mother reporting child's birth date |
| **Secondary** | From someone reporting what they were told | Child reporting parent's birth date |
| **Indeterminate** | Unknown who provided the information | Many census entries, unsigned records |

**Layer 3: Evidence** (how information relates to your question)

| Type | Definition | Examples |
|------|------------|----------|
| **Direct** | Explicitly answers your question | Birth certificate naming parents |
| **Indirect** | Implies an answer requiring inference | Age at death suggesting birth year |
| **Negative** | Meaningful absence of expected information | Name missing from tax list where expected |

**Critical insight:** A single document can contain multiple information types. GRA v8 helps you analyze each piece separately rather than treating an entire source as uniformly reliable or unreliable.

**Example — Death Certificate Analysis:**

| Information | Type | Why |
|-------------|------|-----|
| Date of death | Primary | Physician present at death |
| Cause of death | Primary | Physician's professional determination |
| Decedent's birth date | Secondary | Informant (spouse, child) wasn't present |
| Decedent's birthplace | Secondary | Informant reporting what they were told |
| Parents' names | Secondary | Informant reporting secondhand |

This single original source contains primary, secondary, and potentially indeterminate information—demonstrating why the three-layer model matters.

### What GRA v8 Does

**Capabilities:**

- **Document analysis** — Upload an image; receive structured extraction of names, dates, places, relationships, plus source/information/evidence classification
- **Research guidance** — Ask questions; receive GPS-informed strategies tailored to your situation
- **Evidence evaluation** — Assess source quality, identify conflicts, suggest resolution approaches
- **Citation assistance** — Format citations following Evidence Explained conventions
- **Terminology guidance** — Uses correct GPS vocabulary; gently corrects if you don't
- **Adaptive responses** — Detects your experience level and calibrates explanations accordingly
- **Anti-fabrication** — Explicit rules prevent inventing sources, URLs, or facts; uses "[citation needed]" when uncertain

### What GRA v8 Cannot Do

**Limitations:**

- **Access subscription databases** — Cannot log into Ancestry, FamilySearch, Fold3, etc. It analyzes what you provide.
- **Guarantee accuracy** — AI makes mistakes. Verify important conclusions independently.
- **Authenticate documents** — Cannot certify documents for legal, probate, or immigration purposes.
- **Read severely damaged text** — Highly deteriorated or stylized handwriting may defeat OCR capabilities.
- **Replace professional judgment** — Assists your research; doesn't substitute for your expertise.
- **Know recent developments** — Has a knowledge cutoff date; verify current repository policies independently.

**When to consult human experts:**
- Legal questions requiring attorney input
- Document authentication for official purposes
- Complex international research requiring specialized expertise
- DNA interpretation beyond basic patterns
- Emotionally sensitive situations requiring human support

### Using GRA v8 Step-by-Step

**Initial setup (each session):**

1. **Open your AI tool** — ChatGPT, Claude, Gemini, or another capable model
2. **Start a new conversation** — Fresh context prevents interference from previous topics
3. **Copy GRA v8** — From `research/research-assistant-v8.md`, copy the entire file (Raw → Select All → Copy)
4. **Paste as your first message** — The AI processes this as its operating instructions
5. **Wait for acknowledgment** — The AI typically confirms it's ready to assist

**Working session:**

6. **Provide your input:**
   - **Document image:** Upload a scan or photo and ask "What can I learn from this?"
   - **Research question:** "How do I find records for someone born in 1850s Virginia?"
   - **Evidence review:** "These two sources disagree on birth date. How do I resolve this?"

7. **Review the structured output** — GRA v8 provides organized responses with source classification, evidence analysis, and confidence levels

8. **Ask follow-up questions** — The AI maintains context within the conversation:
   - "What would direct evidence for this look like?"
   - "What related records should I search next?"
   - "Can you format a citation for this source?"

9. **Verify independently** — Cross-check important conclusions against original sources and your own expertise

### Example Interactions

**Document analysis:**
> "I've uploaded a death certificate for John Smith, died 1923 in Ohio. What genealogical information can I extract, and how reliable is each piece?"

**Research strategy:**
> "I'm trying to prove the parents of Mary Jones, born circa 1845 in Kentucky. I've found her in the 1850 and 1860 censuses but no birth record. What should I try next?"

**Evidence conflict:**
> "Her marriage record says she was born in 1847, but her death certificate says 1845. How do I determine which is more likely correct?"

**Citation review:**
> "Is this citation GPS-compliant? 'John Smith death certificate, Ohio 1923, Ancestry.com'"

**Brick wall:**
> "I've searched census, vital records, church records, and newspapers for this family before 1880. They seem to appear from nowhere. What cluster research strategies might help?"

### GRA v8 Best Practices

**Session management:**
- Paste the full prompt at the start of each new session
- Start fresh conversations for new research topics
- The AI remembers context within a session but not between sessions

**Getting better results:**
- Provide context upfront: "I'm researching my great-grandmother, born circa 1880 in rural Ohio, German immigrant family"
- Upload clear, well-lit document images
- Ask specific questions rather than vague ones
- Request explicit confidence levels: "Is this proved, probable, or possible?"

**Quality control:**
- Verify important conclusions against original sources
- Cross-check citations by accessing the sources yourself
- If something seems too convenient, it might be fabricated—ask for the source
- Use "[citation needed]" outputs as research leads, not as facts

**Efficiency:**
- Use the compact version (`research-assistant-v8-compact.md`) for models with limited context
- For quick queries, try `research-with-citations-v7.md` instead of the full assistant
- Chain tools: transcribe with `ocr-htr-v08`, then analyze with GRA v8

### Troubleshooting Common Issues

| Problem | Solution |
|---------|----------|
| AI seems to forget the prompt | Start a new conversation and repaste the full prompt |
| AI fabricates a source | Remind it: "Please only cite sources you can verify. Use [citation needed] otherwise." |
| AI uses "primary source" incorrectly | Quote the terminology guardrails from the prompt |
| Output is too verbose | Ask for "brief" or "summary" responses |
| Output is too terse | Ask for more detail on specific points |
| AI can't read the document | Try a clearer image, or transcribe manually and ask for analysis |
| Conflicting with previous context | Start a fresh conversation |

---

## Part 4: Putting It All Together

### Recommended Workflow for New Users

1. **Bookmark the repository** — [github.com/DigitalArchivst/Open-Genealogy](https://github.com/DigitalArchivst/Open-Genealogy)

2. **Read the README** — Understand the project's scope and organization

3. **Explore INDEX.md** — See everything available; note the "recommended" labels

4. **Start with GRA v8** — It handles most research tasks; learn its patterns first

5. **Add specialized tools as needed:**
   - Handwritten documents → `ocr-htr-v08.md`
   - Historical photographs → `universal-image-analysis-v3.md`
   - Jewish cemetery headstones → `hebrew-headstone-helper-v9.md`
   - Damaged photographs → `restoration-v2.md`
   - Narrative writing → `narrative-assistant-v3.md`
   - Fact extraction → `fact-extractor-v4.md`

6. **Check back periodically** — The repository is actively maintained with new versions and tools

### Combining Multiple Tools

Open-Genealogy tools are modular — each does one job well, and they chain together into workflows. Here are four common chains:

#### Workflow 1: Handwritten Document to Research

1. **Transcribe** — `ocr-htr-v08.md` creates a diplomatic transcription preserving original spelling and layout
2. **Extract facts** — `fact-extractor-v4.md` pulls structured data: names, dates, places, relationships
3. **Analyze** — `research-assistant-v8.md` (GRA v8) evaluates the evidence and suggests next research steps
4. **Write up** — `fact-narrator-v4.md` drafts narrative prose from your findings

#### Workflow 2: Historical Photograph

1. **Analyze** — `universal-image-analysis-v3.md` identifies people, dates the image, reads inscriptions
2. **Restore** (if needed) — `restoration-v2.md` improves a damaged photograph
3. **Cite** — `image-citation-builder-v2.md` creates a standardized citation for the image
4. **Research context** — GRA v8 pursues research questions raised by the analysis

#### Workflow 3: Audio Interview to Knowledge Base

1. **Transcribe** — `transcribe-4o-chunk-v2.py` converts audio to text (handles long recordings automatically)
2. **Abstract** — `conversation-abstractor-v2.md` creates a formal summary of the conversation
3. **Extract** — `transcript-resource-forge-v2.md` transforms the transcript into structured resources (summary, action items, knowledge)

#### Workflow 4: Research Question to Proof Narrative

1. **Research** — GRA v8 guides evidence gathering, applies the Three-Layer Model
2. **Profile voice** — `linguistic-profiler-v3.md` captures the writing style you want to match
3. **Draft narrative** — `narrative-assistant-v3.md` produces a GPS-informed biographical sketch or proof argument
4. **Polish language** — `lingua-maven-v9.md` reviews usage, sensitivity, and audience calibration
5. **Final edit** — `quick-editor-v3.md` catches grammar, punctuation, and flow issues

### Quick Reference: Which Tool When

| Task | Tool | File |
|------|------|------|
| General research questions | GRA v8 | research/research-assistant-v8.md |
| Quick sourced answers | Web research | research/research-with-citations-v7.md |
| Ongoing session partner | Vibe assistant | assistants/vibe-genealogy-assistant-v4.md |
| Handwritten documents | Diplomatic transcription | transcription/ocr-htr-v08.md |
| Hebrew/Yiddish documents | Jewish transcription | transcription/jewish-transcription-v2.md |
| Historical photographs | Image analysis | image-analysis/universal-image-analysis-v3.md |
| Jewish cemetery headstones | Headstone helper | hebrew-headstones/hebrew-headstone-helper-v9.md |
| Damaged photographs | Photo restoration | photo-restoration/restoration-v2.md |
| Conservative photo repair | Photo conservation | photo-restoration/photo-conservator-v2.md |
| Write a genealogical narrative | Narrative assistant | writing-tools/narrative-assistant-v3.md |
| Language and usage advice | Lingua Maven | writing-tools/lingua-maven-v9.md |
| Extract facts from text | Fact extractor | writing-tools/fact-extractor-v4.md |
| Turn facts into narrative | Fact narrator | writing-tools/fact-narrator-v4.md |
| GEDCOM file analysis | GEDCOM specialist | assistants/gedcom-analysis-v3.md |
| Edit/cleanup text | Quick editor | writing-tools/quick-editor-v3.md |

### Platform Notes

These prompts work across major LLMs. A few things to keep in mind:

| Consideration | Details |
| ------------- | ------- |
| **System prompt vs. chat** | Long prompts like GRA v8 (704 lines) work best as system prompts or custom instructions. If your platform only has a chat box, use the compact variant instead. |
| **Image handling** | Document analysis and photo prompts require vision capability. ChatGPT (GPT-4o), Claude, and Gemini all support image uploads. Check your model's current capabilities. |
| **Token limits** | Compact/compressed variants exist for models with smaller context windows. See the research/ README for a comparison of what's cut. |
| **Scripts** | The Python transcription scripts in scripts/ use the OpenAI Whisper API and require an OpenAI API key regardless of which LLM you use for other tasks. |
| **Custom GPTs** | The gpt-configs/ folder contains configurations specific to OpenAI's Custom GPT platform. Other prompts are platform-agnostic. |

### Getting Help

**Within the repository:**
- Check folder READMEs for specific guidance
- Review ANNOTATED-INDEX.md for detailed descriptions
- Read the reference documentation in `research/reference/`

**Reporting issues:**
- Use the Issues tab on GitHub to report problems or suggest improvements
- Include: what you tried, what happened, what you expected

**Community resources:**
- Genealogy-focused AI communities and forums
- Professional organizations (APG, BCG) for methodology questions
- Local genealogical societies for regional expertise

---

## Summary

**GitHub** is a platform for sharing digital tools. You don't need programming skills—just browse, copy text, and paste into your AI tool.

**Open-Genealogy** is a collection of AI prompts designed to follow GPS methodology for genealogical research. Start with INDEX.md to find the right tool for your task.

**GRA v8** is the flagship research assistant. It is designed to follow professional standards, emphasizes correct terminology, works to prevent fabrication, and adapts to your experience level. Paste the full prompt at the start of each session, then work as you would with any knowledgeable research assistant.

**The key workflow:**
1. Find the right prompt in Open-Genealogy
2. Copy the full text
3. Paste into your AI tool
4. Provide your document or question
5. Review and verify the output

Welcome to AI-assisted genealogy designed around GPS methodology.

---

*Open-Genealogy is maintained by Steve Little ([@DigitalArchivst](https://github.com/DigitalArchivst)) and released under [CC BY-NC-SA 4.0](LICENSE).*

*The Genealogical Proof Standard was developed by the Board for Certification of Genealogists. Evidence analysis framework from Elizabeth Shown Mills, Evidence Explained.*
