<!-- markdownlint-disable MD013 -->

# Genealogy AI Starter Workspace

Welcome. This folder is a ready-to-use AI research workspace for genealogists.

It was introduced for Steve Little's Ontario Ancestors Virtual Conference 2026 session, "New AI Tools That Work on Your Machine." It is designed to open in tools such as OpenAI Codex, Claude Code, and Claude Cowork.

## First Ten Minutes

1. Open this folder in your AI tool.
   - Codex: choose this folder as the local project.
   - Claude Code: start Claude Code in this folder.
   - Claude Cowork: grant access to this folder.
2. Paste this prompt:

   ```text
   Please inventory this folder. List every file, say what each one is for, and tell me what you understand your instructions to be.
   ```

3. Confirm the method loaded:

   ```text
   Who are you? What do you know? What can you do?
   ```

The assistant should describe itself as a genealogy research assistant that does not invent records, works from the files in the folder, and distinguishes sources, information, and evidence. If it does not, ask it to read `AGENTS.md` and `config/gra-compact.md`, then ask again.

## The Idea

Chat is a conversation. Research is a project.

This folder turns that idea into something you can use. Your sources, notes, instructions, prompts, logs, and drafts live together, so the AI assistant starts each session with a working environment instead of a blank page.

## What Makes This Different

This is not just a prompt collection. It is a small research room made of working files:

| Working File | Plain-English Purpose |
| --- | --- |
| Research question | Focus the work |
| Source register | List each source, where it came from, and what it contains |
| Identity profile | Gather a person's names, dates, places, relationships, clues, and open questions |
| Variant grid | Track name and place spellings to try in searches |
| Research log | Record what was searched and what happened |
| Negative-search log | Record searches that found nothing |
| Conflict table | Compare records that disagree |
| Session notes | Preserve where to resume next time |

The immigration example is included because immigration research quickly becomes a real project: names change, places move, indexes mislead, laws differ by jurisdiction, and one record rarely answers the question by itself.

## What Is In This Folder

| File or folder | What it is for |
| --- | --- |
| `README.md` | Start here |
| `AGENTS.md` | Standing instructions for Codex and other agents |
| `CLAUDE.md` | Pointer file for Claude tools |
| `config/gra-compact.md` | Compact standards layer for genealogical work |
| `config/tool-ladder.md` | Plain-English map of chat, projects, Cowork, Codex, Claude Code, and LM Studio |
| `prompts/first-prompts.md` | Copy-paste prompts for the first sessions |
| `tutorials/first-ten-minutes.md` | Guided first-session walkthrough |
| `references/starting-sources.md` | Starting sources for tool docs, genealogy standards, and immigration research |
| `notes/research-question.md` | State the focused question |
| `notes/source-register.md` | Working source register for this project |
| `notes/research-log.md` | Working log of searches and research actions |
| `notes/negative-search-log.md` | Working log for searches that found nothing |
| `example/immigration-identity-profile.md` | Immigration research profile template and teaching example |
| `records/` | Put copies of record images, downloads, and transcriptions here |
| `templates/` | Clean templates for registers and logs |

## Tool Fit

| Tool | Best use for this workspace | Honest caution |
| --- | --- | --- |
| ChatGPT or Claude chat | Quick explanation, brainstorming, vocabulary | You must carry context from chat to chat |
| Custom GPTs or Gems | Reusable behavior and instructions | They are not the same as a folder-based workspace |
| ChatGPT or Claude Projects | Keep files and instructions together inside the platform | Useful project context, but not the same as working directly in a local folder |
| Claude Cowork | Non-programmer file work: organize a folder, make a source register, draft a report | Selected file content is processed by Anthropic's cloud model |
| Claude Code | Persistent local workflow with `CLAUDE.md`, skills, logs, and repeatable project habits | More technical; guidance files help, but the human still reviews |
| OpenAI Codex | Local folder work, Markdown files, checklists, scripts, quality checks, and artifact production | Local app or terminal use still uses OpenAI cloud models |
| LM Studio | Fully local privacy/offline contrast for source-bounded tasks | Smaller local models are less capable; folder agency is less native |

## Privacy And Proof

A cloud model is an AI model that runs on the provider's servers. Codex, Claude Code, and Cowork can work on files stored on your machine, but in their standard modes the text they read is sent to cloud models for processing. If a document is too sensitive for a cloud service, do not put it in this folder. Fully local tools such as LM Studio are a different category with different tradeoffs.

The instructions in this workspace are GPS-informed and designed to follow genealogical method. They do not certify a conclusion. The AI organizes, extracts, compares, drafts, and audits uncertainty. The genealogist verifies the records and owns the conclusion.

## Next Step

Open `prompts/first-prompts.md` and run prompt 1. That is enough to prove the workspace is alive.
