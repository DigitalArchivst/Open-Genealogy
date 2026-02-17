# Open-Genealogy: A Tour-Guide Script for First-Time GitHub Explorers

> **What is this?** An alternative onboarding format for those who prefer learning through dialogue. A fictional guide walks three students through the repository, explaining each section in plain language. For a traditional walkthrough, see [GETTING-STARTED.md](GETTING-STARTED.md). For a catalog, see [INDEX.md](INDEX.md).

---

**Guide:** Welcome aboard, team! Today we’re visiting a GitHub repository called **Open-Genealogy**. Think of a repo like a big, well-organized backpack full of useful tools. We’ll walk through each pocket together and see what’s inside. You can ask questions as we go!

**Student 1:** Is this like a Python project?

**Guide:** Great question! It’s not full of Python code like a game or an app. Instead, it’s a **toolkit of prompts and workflows** for genealogy—finding and telling family history stories. There *are* a few Python scripts, but most of the repo is well-crafted text files and instructions.

---

## Stop 1: The Front Desk (Root Folder)

**Guide:** We’re standing at the root of the repo—the main entrance. Here’s what you see first:

- **README.md**: This is the welcome sign. It tells you what the repo is and where to start.
- **INDEX.md**: A catalog—like a table of contents for everything inside.
- **ANNOTATED-INDEX.md**: A bigger tour guide, with descriptions of each section.
- **LICENSE**: The rules for sharing and using the content.

**Student 2:** Why so many guides?

**Guide:** Imagine a library. Some people want a quick map, others want the full tour. This repo gives both!

---

## Stop 2: Research Wing (`research/`)

**Guide:** This area is all about **research methodology**—how to do careful, evidence-based genealogy. The files are named like versions of a game: `v6`, `v7`, `v8`. That means they’ve been improved over time.

- **Flagship prompts** help a researcher gather and analyze sources.
- **Reference files** explain the rules of good evidence.

**Student 3:** So these are like instructions for an AI assistant?

**Guide:** Exactly! They’re scripts that help AI stay accurate and not make things up.

---

## Stop 3: Transcription Lab (`transcription/`)

**Guide:** Here we find prompts for **transcribing old documents**—that means typing old handwriting exactly as it appears.

- There’s a big all-purpose prompt for OCR/HTR work.
- There’s also a special prompt for **Jewish documents** with different languages and scripts.

**Student 1:** OCR is like when your phone reads text from a photo?

**Guide:** Yep! And HTR is similar, but for handwriting.

---

## Stop 4: Photo Restoration Studio (`photo-restoration/`)

**Guide:** This section helps AI restore old photos—fixing scratches, fading, or tears while keeping things historically accurate.

- There’s a general restoration prompt.
- Others focus on **conservation** (light touch) or **reconstruction** (heavy damage).

**Student 2:** So it’s like Photoshop instructions for AI?

**Guide:** That’s a good way to think about it!

---

## Stop 5: Writing Tools Workshop (`writing-tools/`)

**Guide:** Here’s where writing happens. These prompts help with:

- Extracting facts from documents
- Turning facts into a story
- Summarizing interviews
- Cleaning up grammar

**Student 3:** That sounds like tools for writing a history report.

**Guide:** Exactly. It helps turn raw records into a readable narrative.

---

## Stop 6: AI Assistants (`assistants/`)

**Guide:** These are “personas” for AI assistants. Think of them like custom chatbots:

- One is a friendly storytelling genealogy helper.
- Another specializes in **GEDCOM files** (family tree data).

**Student 1:** GEDCOM sounds like a Pokémon.

**Guide:** It does! But it’s actually a file format for family trees.

---

## Stop 7: GPT Configs (`gpt-configs/`)

**Guide:** These files configure how the AI assistant would behave if deployed on platforms like ChatGPT.

**Student 2:** So these are like settings files?

**Guide:** Exactly—like a config for how the assistant acts and responds.

---

## Stop 8: Scripts Drawer (`scripts/`)

**Guide:** Finally, some real Python! These scripts handle **audio transcription**—turning spoken interviews into text.

- One handles single files.
- Another splits long audio into chunks.

**Student 3:** So we *do* get to see Python!

**Guide:** Just a bit—but it’s practical and useful.

---

## Stop 9: Benchmark Zone (`benchmark/`)

**Guide:** This is where the project checks how well different AI models follow the research rules.

- It includes **case studies** and a detailed **rubric** for scoring outputs.

**Student 1:** Like grading homework, but for AI?

**Guide:** Perfect analogy!

---

## Stop 10: Media Shelf (`media/`)

**Guide:** Here’s a small media area with audio explaining how the prompts work. It’s like a recorded mini-lecture.

---

## Final Wrap-Up

**Guide:** And that’s the whole tour! This repo isn’t a typical Python codebase—it’s more like a toolkit for teaching AI to do careful historical research. But even as new Python students, you can recognize how a repo is organized: a welcome guide, a catalog, themed folders, and specialized tools.

**Student 2:** So the big lesson is… organization and clear instructions?

**Guide:** Exactly! Whether you’re writing Python or building prompts, **clarity and structure** make the project usable.

**Student 3:** Can we come back later?

**Guide:** Absolutely. GitHub is open 24/7—just bring your curiosity.

