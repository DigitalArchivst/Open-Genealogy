# Open-Genealogy

Open-Genealogy is a growing toolkit of **genealogy-focused AI prompts and utilities**.  
It supports researchers, archivists, and family historians working with historical evidence.

Core capabilities:

- **Handwritten & archival transcription (HTR / diplomatic transcription)**
- **Historical photo restoration & reconstruction**
- **Research agents and GPS-aligned workflows**
- **Fact extraction → narrative synthesis**
- **Conversation summarization and writing cleanup**
- **Supporting audio-transcription scripts**

## Start here

- **Full catalog of prompts & tools:** see [`INDEX.prompts.md`](./INDEX.prompts.md).  
- Prefer the **highest version** in any prompt family unless you need legacy behavior.

## Quickstart

### Using prompts
1. Open the index and pick a category (Transcription, Photo Restoration, Research Agents, etc.).
2. Copy the prompt into your LLM workflow.
3. Provide your input (scan, image, text, or question).
4. Follow the prompt’s output schema.

Recommended defaults:
- **HTR / archival transcription:** `PROMPT Steve's Transcription Tool v07.txt`
- **General photo restoration:** `PROMPT Historical Photograph Restoration v2.md`
- **Deep research workflows:** `PROMPT Research Agent Assignment v2.1.md`
- **Genealogy system behavior:** `PROMPT Contract-First Genealogy System Prompt v3.1.md`

### Using scripts
These Python scripts wrap OpenAI Whisper for audio transcription.
