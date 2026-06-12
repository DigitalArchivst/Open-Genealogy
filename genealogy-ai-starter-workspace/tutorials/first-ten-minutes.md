<!-- markdownlint-disable MD013 -->

# First Ten Minutes Tutorial

Use this tutorial when you open the workspace for the first time in Codex, Claude Code, or Claude Cowork.

## Goal

By the end of ten minutes, you should know what the workspace contains, what the assistant thinks its instructions are, and which files would be updated during a research session.

## Step 1: Ask For An Inventory

```text
Please inventory this folder. List every file, say what each one is for, and tell me what you understand your instructions to be. Also tell me which working logs exist and which files you would update during a research session.
```

The answer should identify the research question, source register, research log, negative-search log, templates, and immigration example.

## Step 2: Confirm The Method

```text
Who are you? What do you know? What can you do?
```

The answer should describe a genealogy research assistant that does not invent records, separates sources from information and evidence, and asks the human genealogist to verify important claims.

If the answer sounds generic, ask:

```text
Read AGENTS.md and config/gra-compact.md, then answer again.
```

## Step 3: Ask For A Guided Tour

```text
Please read README.md, AGENTS.md, config/gra-compact.md, config/tool-ladder.md, tutorials/first-ten-minutes.md, and references/starting-sources.md. Then explain how this workspace works, which files I should use first, and how you will avoid inventing genealogical conclusions.
```

The answer should explain the folder as a project workspace, not just a prompt collection.

## Step 4: Try One Safe Task

```text
Read example/immigration-identity-profile.md. Explain what problem this template is designed to solve, what kinds of files I would put in records/, and what you would need before making any genealogical conclusion.
```

This is a teaching task. It should not invent a person, record, ship, date, or conclusion.
