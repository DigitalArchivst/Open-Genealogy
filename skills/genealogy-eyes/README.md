# Genealogy Eyes

Steve Little’s family-history image interpreter. Version 0.1.1.

## Use the skill

Extract the ZIP. It contains one folder named `genealogy-eyes`. In a trusted project, copy the whole folder into `.agents/skills/` for Codex or `.claude/skills/` for Claude Code. Start a fresh session in that project. In Codex invoke `$genealogy-eyes`. In Claude Code invoke `/genealogy-eyes`. Attach an image or supply a path the client can read.

## Try the example

Open [the fictional picnic notice](examples/picnic-notice.png). Attach it, then ask:

> A relative remembers a musician named Clara Bell. What does this notice tell me about her? Quote the relevant words and suggest one local record I could check for evidence that she played that day.

A good reading quotes “Music by Clara Bell and the hall band.” The small footer identifies the notice as fictional. Within the exercise, Clara was advertised to play. A newspaper report written after the event that names the performers could help establish whether she actually played.

The skill uses the image and tools available in your client. It can suggest archival searches. Specific archives, image creation, or historical newspaper access depend on your own accounts and tools.

## Credit and rights

Adapted for the Open-Genealogy collection from Steve Little’s Genealogy Eyes Custom GPT. The example notice was made for this project and depicts a fictional event. The [Open-Genealogy rights policy](https://github.com/DigitalArchivst/Open-Genealogy/blob/main/RIGHTS.md) applies [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) to Steve-authored copyrightable material within its scope. See the included LICENSE for the legal code. Uploaded reader records retain their own rights.
