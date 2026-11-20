# Deep Look

Separate visible image details from interpretation.

## Use the skill

Extract the folder into the skills directory supported by your client. In a project, use .agents/skills/deep-look/ for Codex or .claude/skills/deep-look/ for Claude Code. Start a fresh session in that project. Select the skill by name and enter the example below. When the task uses an image, attach the source image in a client that supports it.

## Worked example

Inspect the fictional picnic notice. Which design features can be observed, and which claims need evidence?

Illustrative result: The notice advertises music by Clara Bell and the hall band at Willow Hall. It provides evidence of a planned performance. A later newspaper report could help establish whether the band appeared.

## Origin and reuse

Deep Look v2 is Steve Little’s image analysis prompt. The portable edition adds skill discovery metadata, source-handling guidance, this guide and a fictional practice example. Steve licensed his prompt under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Read LICENSE.txt and RIGHTS.md for scope. The fictional picnic notice is included at examples/picnic-notice.png.

In portable edition 2.0.0-portable.2, descriptions of people distinguish visible details from names, relationships and demographic information documented in a caption or record. The analysis attributes these claims to their source and retains its uncertainty.
