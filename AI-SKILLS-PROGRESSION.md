# AI Skills Progression

A structured path from first chatbot conversation to autonomous AI agents. Forty skills organized into seven tiers, each building on the last. Designed for genealogists, but applicable to anyone learning to work with AI.

**No programming required through Tier 5.** Tiers 6 and 7 introduce command-line tools and light configuration.

---

## How to Use This List

- **Start where you are.** If you already use ChatGPT daily, skip to the tier where the skills feel new.
- **Each skill is a checkpoint**, not a course. Some take ten minutes; others take a few sessions to internalize.
- **Platform-agnostic where possible.** Most skills work across ChatGPT, Claude, Gemini, and other capable models. Platform-specific skills are labeled.
- **Genealogy examples included**, but every skill applies broadly.

---

## Tier 1: Chatbot Foundations

The basics. If you can do all six of these comfortably, you're ready to move on.

| # | Skill | What It Looks Like |
|---|-------|--------------------|
| 1 | **Have a conversation with an AI chatbot** | Open ChatGPT, Claude, or Gemini. Ask a question. Read the answer. Ask a follow-up. You now understand multi-turn conversation. |
| 2 | **Upload an image for analysis** | Drag a photo into the chat. Ask "What do you see?" Understand that vision-capable models can read documents, describe photographs, and interpret visual evidence. |
| 3 | **Upload a document for analysis** | Attach a PDF, spreadsheet, or text file. Ask the AI to summarize it, extract key points, or answer questions about it. |
| 4 | **Recognize when the AI is wrong** | Ask about something you know well. Notice when it fabricates a source, invents a date, or states something plausible but false. This is the most important skill on the list. |
| 5 | **Ask the AI to show its reasoning** | Instead of accepting an answer, ask "How did you arrive at that?" or "What's your source for that claim?" Learn to distinguish inference from fact in AI output. |
| 6 | **Compare outputs across models** | Ask the same question to two or three different models. Notice how answers differ. Develop intuition for model strengths and blind spots. |

---

## Tier 2: Prompt Craft

Moving from "asking questions" to "giving effective instructions."

| # | Skill | What It Looks Like |
|---|-------|--------------------|
| 7 | **Write a specific, structured prompt** | Instead of "Tell me about census records," write "List the information fields on the 1940 U.S. Federal Census and explain what each one tells a genealogist." Specificity transforms output quality. |
| 8 | **Provide context before asking** | Open with "I'm researching a German immigrant family in 1880s Ohio. The surname may have been anglicized." Context steers the AI toward relevant, calibrated responses. |
| 9 | **Use role assignment** | "You are an experienced genealogist specializing in Eastern European Jewish records." Role framing changes tone, vocabulary, and depth. |
| 10 | **Chain prompts across a session** | Transcribe a document in one message, extract facts in the next, then ask for research leads. Each step builds on the last within a single conversation. |
| 11 | **Paste a full system prompt into chat** | Copy an Open-Genealogy prompt (like GRA v8) into a new conversation. Understand that long, detailed instructions shape the entire session. This is the copy-paste workflow described in [GETTING-STARTED.md](GETTING-STARTED.md). |
| 12 | **Understand context windows and token limits** | Know that AI has a finite memory within each conversation. Recognize when a session is "forgetting" early instructions. Learn when to start fresh vs. continue. |
| 13 | **Use compact vs. full prompts strategically** | Choose the 147-line compact version when context is limited; use the full 704-line version when the model can handle it. Understand the tradeoff between thoroughness and token budget. |

---

## Tier 3: Custom GPTs & Assistants

Building your own persistent AI configurations rather than pasting prompts every session.

| # | Skill | What It Looks Like |
|---|-------|--------------------|
| 14 | **Create a Custom GPT** | In ChatGPT, build a Custom GPT with instructions, a name, and a description. It remembers its role across sessions without re-pasting. *(OpenAI platform)* |
| 15 | **Add knowledge files to a Custom GPT** | Upload reference documents — evidence-terminology.md, a family group sheet, a county history PDF — so the GPT can draw on them in every conversation. *(OpenAI platform)* |
| 16 | **Configure guardrails and behavior** | Write instructions that prevent fabrication, enforce terminology, and define what the assistant should refuse to do. The gpt-configs/ folder in this repository shows working examples. |
| 17 | **Build a Gem** | Create a persistent assistant in Google Gemini with custom instructions and reference material. Same concept as Custom GPTs, different platform. *(Google platform)* |
| 18 | **Share and publish an assistant** | Make your Custom GPT or Gem available to others. Understand visibility settings, usage limits, and how to maintain a published tool. |
| 19 | **Evaluate and iterate on assistant performance** | Test your assistant against known questions. Compare its output to the benchmark rubric in this repository. Revise instructions based on failure patterns. |

---

## Tier 4: NotebookLM & Source-Grounded Research

Working with AI that's anchored to your specific sources rather than general knowledge.

| # | Skill | What It Looks Like |
|---|-------|--------------------|
| 20 | **Add sources to a NotebookLM notebook** | Upload PDFs, paste URLs, or add Google Docs. NotebookLM reads them and answers questions grounded in your material — not its training data. *(Google platform)* |
| 21 | **Ask questions across multiple sources** | "What do these three documents say about where the family lived in 1890?" NotebookLM cross-references your uploaded sources and cites which document supports each claim. |
| 22 | **Generate an Audio Overview** | Have NotebookLM create a podcast-style conversation about your sources. Useful for absorbing research during a commute or hearing connections you missed while reading. |
| 23 | **Build a genealogical document collection** | Create a notebook for a specific research question. Upload census images, vital records, newspaper clippings, and correspondence. Use it as an AI-searchable case file. |
| 24 | **Create structured outputs from sources** | Generate timelines, family group summaries, or source-by-source evidence tables — all grounded in the documents you uploaded, with inline citations. |
| 25 | **Understand grounded vs. ungrounded AI** | Recognize the difference between a chatbot drawing on general training data and a tool like NotebookLM drawing on your specific sources. Know when each approach is appropriate. |

---

## Tier 5: Projects & Persistent Workspaces

Long-running research with persistent context, knowledge, and conversation history.

| # | Skill | What It Looks Like |
|---|-------|--------------------|
| 26 | **Set up a Claude Project** | Create a project in Claude with a custom system prompt and uploaded knowledge files. Every conversation within the project inherits that context automatically. *(Anthropic platform)* |
| 27 | **Set up a ChatGPT Project** | Create a project workspace in ChatGPT where files, instructions, and conversations are grouped together. *(OpenAI platform)* |
| 28 | **Organize project knowledge files** | Curate what the AI knows: upload your research log, key transcriptions, the evidence-terminology reference, and your current proof argument. Remove outdated files as research evolves. |
| 29 | **Conduct multi-session research** | Maintain a coherent research thread across days or weeks. Use project context to avoid re-explaining your research question every session. Pick up where you left off. |
| 30 | **Combine tools within a project workflow** | In a single project, chain the workflows from [GETTING-STARTED.md](GETTING-STARTED.md): transcribe → extract facts → analyze evidence → draft narrative. Each step feeds the next. |
| 31 | **Use artifacts and structured outputs** | Work with Claude's artifacts (documents, code, diagrams) or ChatGPT's canvas to produce and refine deliverables inside the conversation — not just in the chat stream. |

---

## Tier 6: Claude Code & Developer-Adjacent Tools

The command line and IDE. No prior programming experience required, but comfort with a terminal helps.

| # | Skill | What It Looks Like |
|---|-------|--------------------|
| 32 | **Use Claude Code on the web** | Access Claude Code through claude.ai's agentic coding interface. Give it tasks like "read this folder of transcriptions and create a summary table." It reads files, writes files, and runs commands — all in a browser. |
| 33 | **Install and run Claude Code CLI** | Install the command-line tool on your computer. Run `claude` in a terminal. Interact with an AI that can see your files, run scripts, and make changes to your local projects. |
| 34 | **Use Claude Code in an IDE** | Install the Claude Code extension in VS Code or another supported editor. Get AI assistance that understands your full project context — files, structure, dependencies. |
| 35 | **Work with a GitHub repository** | Use Claude Code to explore, understand, and contribute to repositories like Open-Genealogy. Clone a repo, ask Claude Code to explain the structure, make edits, create commits. |
| 36 | **Automate a repeatable workflow** | Write a script (with Claude Code's help) that processes a batch of files — e.g., transcribe all audio files in a folder, rename images by date, or extract facts from a stack of PDFs. |
| 37 | **Use CLAUDE.md for project memory** | Create a CLAUDE.md file in your project root with conventions, preferences, and instructions that Claude Code reads automatically at every session start. Persistent context without re-explaining. |
| 38 | **Chain AI tools via the command line** | Pipe outputs between tools: use Whisper for transcription, Claude Code for analysis, and a Python script for formatting — all orchestrated from the terminal. |

---

## Tier 7: OpenClaw & Autonomous Agents

AI that acts on your behalf across platforms — with all the power and responsibility that implies.

| # | Skill | What It Looks Like |
|---|-------|--------------------|
| 39 | **Install and configure OpenClaw** | Set up the open-source autonomous agent on your machine. Connect it to an LLM provider (Claude, GPT, DeepSeek). Understand the difference between sandbox and full system access. |
| 40 | **Connect OpenClaw to a messaging platform** | Link OpenClaw to Signal, Telegram, Discord, or WhatsApp. Interact with your AI agent through the messaging app you already use — not a special interface. |
| 41 | **Install skills from ClawHub** | Browse the skill registry (10,000+ skills as of early 2026). Install skills that extend what your agent can do — file management, web research, calendar integration, document processing. |
| 42 | **Create a custom OpenClaw skill** | Build a reusable skill package: define tools, prompts, and behaviors. Publish to ClawHub or keep private. This is where your prompt-writing experience from Tiers 2–3 pays off. |
| 43 | **Manage permissions and security** | Understand what your agent can and cannot access. Configure sandboxing. Review audit logs. Know the security landscape — OpenClaw's rapid growth has attracted both innovation and risk. |
| 44 | **Design a multi-step autonomous workflow** | Set up an agent that monitors a folder of new document scans, transcribes each one, extracts facts, and adds entries to a research log — all without manual intervention for each file. |

---

## The Progression at a Glance

| Tier | Theme | Skills | Key Milestone |
|------|-------|--------|---------------|
| 1 | Chatbot Foundations | 1–6 | You can hold a productive AI conversation and spot errors |
| 2 | Prompt Craft | 7–13 | You can write effective prompts and use Open-Genealogy tools |
| 3 | Custom GPTs & Assistants | 14–19 | You can build and share persistent AI assistants |
| 4 | NotebookLM & Source-Grounded Research | 20–25 | You can do AI research anchored to your specific sources |
| 5 | Projects & Persistent Workspaces | 26–31 | You can run long research projects with persistent AI context |
| 6 | Claude Code & Developer Tools | 32–38 | You can use AI to work with files, code, and repositories |
| 7 | OpenClaw & Autonomous Agents | 39–44 | You can deploy AI agents that act on your behalf |

---

## Notes

- **This is a learning path, not a gatekeeping exercise.** You don't need to master every skill before moving to the next tier. Some people will skip tiers entirely based on their needs.
- **The tools will change.** Platform names, features, and interfaces evolve. The underlying skills — clear instructions, source awareness, critical evaluation, workflow design — transfer across whatever comes next.
- **Security scales with capability.** The more autonomy you give an AI, the more carefully you should configure permissions, review outputs, and understand what it's doing. This is especially true at Tiers 6 and 7.
- **Start where it's useful.** A genealogist who just wants better document transcription doesn't need autonomous agents. A researcher managing hundreds of source files might jump straight to projects and Claude Code.

---

*Open-Genealogy is maintained by Steve Little ([@DigitalArchivst](https://github.com/DigitalArchivst)) and released under [CC BY-NC-SA 4.0](LICENSE).*
