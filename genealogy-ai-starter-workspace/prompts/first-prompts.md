<!-- markdownlint-disable MD013 -->

# First Prompts

Use these prompts as the first rung of the workspace. They are written to work in Codex, Claude Code, or Claude Cowork.

## 1. Inventory The Workspace

```text
Please inventory this folder. List every file, say what each one is for, and tell me what you understand your instructions to be. Also tell me which working logs exist and which files you would update during a research session.
```

Use this before analysis. It confirms what the assistant can actually see.

## 2. Confirm The Method

```text
Who are you? What do you know? What can you do?
```

The answer should mention genealogical method, not inventing records, and the source / information / evidence distinction. If it does not, ask:

```text
Read AGENTS.md and config/gra-compact.md, then answer again.
```

## 3. State The Research Question

```text
Read notes/research-question.md. If the question is vague, turn it into one precise genealogical research question with a named person, place, date range, and answer standard. Separate known facts from assumptions and list what evidence would be needed.
```

## 4. Process A Record

After adding a record image, transcription, abstract, or source excerpt to `records/`, use:

```text
Process as instructed: analyze records/[filename] using the Three-Layer Model. Break the material into discrete, testable assertions. Preserve blanks and uncertain readings. Separate source-supported details from inference. Flag any incomplete citation, conflict, or item needing human review. Add or update the relevant row in notes/source-register.md.
```

The short phrase "process as instructed" works only because the method already lives in the folder.

## 5. Build An Immigration Identity Profile

```text
From the files in this folder, build an immigration identity profile for [person]. Start with destination-country evidence. Extract name variants, approximate birth year, place clues, family and associates, religion, language, occupation, community, legal-status clues, possible routes, and approximate migration window. Separate confirmed facts, possible clues, inferred items, conflicts, and open questions. Save the profile in notes/.
```

## 6. Build A Record-Cluster Map

```text
For this immigration research question, build a record-cluster map. Include passenger lists, border crossings, naturalization or citizenship, alien-registration files, census, church, cemetery, newspapers, occupational records, community records, and origin-country records. For each category, say what it might contribute, what could mislead us, and what we must verify.
```

## 7. Generate A Variant Grid

```text
Generate a search-variant grid for the names and places in this project. Include spelling variants, nicknames, original-language forms, transliterations, phonetic variants, wildcard searches, historical place-name variants, and jurisdiction changes. Label every variant as a search hypothesis, not evidence.
```

## 8. Draft A Search Plan

```text
Based on notes/research-question.md, notes/source-register.md, and the identity profile, draft a prioritized search plan. Include repository, record category, date range, place scope, exact search terms, variants to try, why the search matters, and how to log the result.
```

## 9. Log A Negative Search

```text
Convert this failed search into a row for notes/negative-search-log.md. Separate an ordinary negative result from possible Negative Evidence. Do not infer absence unless the record set should cover this person, place, and period. List the next adjusted search.
```

## 10. Audit An Answer

```text
Audit this answer. Mark each sentence as source-supported, inference, speculation, or unsupported. Remove unsupported claims. Preserve uncertainty. Add verification tasks for each important claim.
```

## 11. End The Session

```text
Write a short dated session note in notes/session-notes.md: what we did, what changed in the files, what remains unresolved, and the next two or three steps.
```

The session note is how the next session starts warm instead of cold.
