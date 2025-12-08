# Prompt & Tool Index (Open-Genealogy)

This is the canonical catalog of scripts and prompts in this repository.  
Browse by category to find what you need. Each entry includes a practical, plain-language description.  

- **Recommended versions:** When a prompt family has multiple versions, prefer the highest version unless you need legacy behavior.
- **Machine-readable index:** A structured XML block is included at the end for tools/agents.

---

## Scripts & Utilities

- `transcribe-4.py`  
  CLI transcription helper using OpenAI Whisper. Prompts for an audio file path and output format (e.g., text or SRT), then submits the file to the API and saves the result. Designed for straightforward “single-file” transcription runs.

- `transcribe_v02.py`  
  Minimal example of OpenAI audio transcription. Useful as a reference starting point or a lightweight fallback when you don’t need chunking or extra options.

- `transcribe-4o-chunk.py`  
  Long-audio workflow. Splits (chunks) large recordings, transcribes each chunk, and merges into a final output. Intended for interviews, lectures, or any file too large for a single pass.

---

## Transcription & HTR Prompts

- `PROMPT Describe Transcribe Analyze Interpret.txt`  
  Compact four-step workflow reminder: first describe the artifact, then transcribe verbatim, analyze its content, and interpret meaning/implications. Useful as a tiny “do this in order” scaffold.

- `PROMPT Steve's Transcription Tool v02.txt` *(legacy)*  
  Early diplomatic transcription protocol for handwritten/archival sources. Emphasizes fidelity to the page, uncertainty notation, and structured output.

- `PROMPT Steve's Transcription Tool v03.txt` *(legacy)*  
  Refinement of v02. Clarifies rules for line breaks, ambiguous characters, and layout features like marginalia.

- `PROMPT Steve's Transcription Tool v04.txt` *(legacy)*  
  Adds more explicit handling for damaged text, insertions, and page-level structure. Good for consistency when working with messy scans.

- `PROMPT Steve's Transcription Tool v06.5.md`  
  Mature diplomatic transcription prompt. Preserves spelling, punctuation, capitalization, and lineation while producing clean transcription plus notes on uncertainty and layout.

- `PROMPT Steve's Transcription Tool v07.txt` **(recommended default)**  
  Latest, most consistent version. Optimized for reliable uncertainty tagging, strict verbatim capture, and stable structured outputs across varied document types.

- `PROMPT Unofficial HTR Transcription (Humphries Method) v1.md`  
  Minimalist HTR method emphasizing low character/word error and strict verbatim transcription. Use when you want a shorter prompt with a tight “just transcribe” focus.

---

## Photo Restoration & Enhancement Prompts

- `PROMPT Steve's Photo Conservator v1.md` *(legacy)*  
  “Do-no-harm” conservation workflow for historical photos. Focus on subtle repairs, tonal recovery, and preserving exact likeness and period details.

- `PROMPT Steve's Photo Conservator v2.md`  
  Updated conservation protocol with clearer damage taxonomy and restoration priorities while keeping strict period authenticity.

- `PROMPT Steve's Historic Photo Reconstructor v3.md`  
  Reconstruction-oriented prompt for heavily damaged photos. Directs the model to restore missing regions using photographic logic and era-appropriate detail.

- `PROMPT Steve's Photo Damage Removal Specialist v3.md`  
  Intensive museum-grade restoration process. Starts with detailed analysis of subjects, context, period, and damage; then removes damage comprehensively while avoiding AI artifacts.

- `PROMPT Historical Photograph Restoration v2.md`  
  Universal high-standard restoration prompt that adapts to any subject count, damage severity, and photographic era. A good default when you want a robust, general solution.

---

## Writing, Summaries & Content Tools

- `PROMPT Summarize Chat v3.txt`  
  Summarizes a conversation into key points, themes, and actionable takeaways. Useful for turning research chats into archival abstracts.

- `PROMPT Lingustic Profiler v3.md`  
  Profiles writing style (tone, lexical habits, rhythm, markers) to characterize voice or compare authorship across texts.

- `PROMPT InfographicGPT v7 Gemini.md`  
  Converts complex source material into infographic-ready content: strong hierarchy, clear labeling, and visual-friendly summarization.

- `PROMPT Steve's Fact Extractor v4.txt`  
  Extracts atomic factual claims from messy text into structured, citation-ready units. Built for genealogy notes and source digestion.

- `PROMPT Steve's Fact Narrator v4.txt`  
  Turns extracted facts into coherent narrative prose while preserving evidentiary boundaries and uncertainty markers.

- `PROMPT Chat Conversation Abstractor v2.md`  
  Produces a formal abstract of a conversation: purpose, claims, evidence, and unresolved questions.

- `PROMPT Steve's Content Decoder v01.txt`  
  Sense-making assistant for dense or ambiguous text: clarifies meaning and returns structured highlights.

- `PROMPT Steve's Quick Editor v03.txt`  
  Fast editorial pass focused on clarity and flow, with a brief change summary.

- `PROMPT Quick Writing Cleanup v3.md`  
  Lightweight cleanup for grammar, verbosity, and readability without altering meaning.

- `PROMPT Image Citation Builder v2.md`  
  Generates consistent citations for images (especially archival photos) using standardized fields.

---

## Research & Analysis Agents

- `PROMPT Research Assignment v0.md` *(legacy template)*  
  Deep-research assignment framework with best practices, output schemas, comparative matrices, timelines, and confidence handling.

- `PROMPT Research Agent Assignment v2.1.md`  
  Reusable research-agent spec: subject classification, adaptive methodology, verification rules, structured deliverables, and quality gates.

- `PROMPT Contract-First Genealogy System Prompt v3.1.md`  
  System-level prompt for a GPS-compliant genealogy assistant. Enforces a contract-lock workflow, structured logs, and ethics-first research behavior.

---

## GPT Shells & Configs

- `GPT Website Frontend GPT v3.txt`  
  Template for custom GPTs tied to a blog/site domain. Instructs domain-first search, summary generation, and menu-style follow-ups.

- `GPT - Open GeneaGPT Beta 0.4 (2024-01-22b).txt`  
  Full identity and operating spec for Open GeneaGPT: role, tone, standards, citation posture, and response structure.

---

## License

- `LICENSE`  
  Creative Commons BY-NC-SA 4.0 license text.

---

```xml
<repository_index>
  <file name="transcribe-4.py">
    <category>scripts_and_utilities</category>
    <summary>CLI wrapper around OpenAI Whisper for single-file audio transcription with selectable output formats (e.g., text, SRT).</summary>
    <status>stable</status>
  </file>
  <file name="transcribe_v02.py">
    <category>scripts_and_utilities</category>
    <summary>Minimal reference implementation of OpenAI audio transcription for lightweight use or as a starting template.</summary>
    <status>stable</status>
  </file>
  <file name="transcribe-4o-chunk.py">
    <category>scripts_and_utilities</category>
    <summary>Long-audio transcription pipeline that chunks recordings, transcribes segments, and merges results into a final output.</summary>
    <status>stable</status>
  </file>

  <file name="PROMPT Describe Transcribe Analyze Interpret.txt">
    <category>transcription_and_htr_prompts</category>
    <summary>Four-step workflow scaffold: describe artifact, transcribe verbatim, analyze content, interpret meaning/implications.</summary>
    <status>stable</status>
  </file>
  <file name="PROMPT Steve's Transcription Tool v02.txt">
    <category>transcription_and_htr_prompts</category>
    <summary>Early diplomatic transcription protocol emphasizing page fidelity and uncertainty notation.</summary>
    <status>legacy</status>
  </file>
  <file name="PROMPT Steve's Transcription Tool v03.txt">
    <category>transcription_and_htr_prompts</category>
    <summary>Refines v02 with clearer rules for lineation, ambiguity, and layout features.</summary>
    <status>legacy</status>
  </file>
  <file name="PROMPT Steve's Transcription Tool v04.txt">
    <category>transcription_and_htr_prompts</category>
    <summary>Further refinement including explicit guidance for damaged text and archival insertions.</summary>
    <status>legacy</status>
  </file>
  <file name="PROMPT Steve's Transcription Tool v06.5.md">
    <category>transcription_and_htr_prompts</category>
    <summary>Mature diplomatic transcription prompt preserving spelling, punctuation, and line breaks with structured notes.</summary>
    <status>stable</status>
  </file>
  <file name="PROMPT Steve's Transcription Tool v07.txt">
    <category>transcription_and_htr_prompts</category>
    <summary>Latest recommended transcription prompt emphasizing consistent uncertainty tagging and dependable structured outputs.</summary>
    <status>recommended</status>
  </file>
  <file name="PROMPT Unofficial HTR Transcription (Humphries Method) v1.md">
    <category>transcription_and_htr_prompts</category>
    <summary>Minimalist HTR method focused on strict verbatim capture and error minimization.</summary>
    <status>stable</status>
  </file>

  <file name="PROMPT Steve's Photo Conservator v1.md">
    <category>photo_restoration_and_enhancement</category>
    <summary>Legacy “do-no-harm” conservation workflow for subtle repair and strict historical fidelity.</summary>
    <status>legacy</status>
  </file>
  <file name="PROMPT Steve's Photo Conservator v2.md">
    <category>photo_restoration_and_enhancement</category>
    <summary>Updated conservation protocol with clearer damage taxonomy and restoration priorities.</summary>
    <status>stable</status>
  </file>
  <file name="PROMPT Steve's Historic Photo Reconstructor v3.md">
    <category>photo_restoration_and_enhancement</category>
    <summary>Reconstruction-oriented restoration prompt for severely damaged historical images.</summary>
    <status>stable</status>
  </file>
  <file name="PROMPT Steve's Photo Damage Removal Specialist v3.md">
    <category>photo_restoration_and_enhancement</category>
    <summary>Intensive museum-grade restoration: analyze subjects/period/damage, then remove damage while avoiding AI artifacts.</summary>
    <status>stable</status>
  </file>
  <file name="PROMPT Historical Photograph Restoration v2.md">
    <category>photo_restoration_and_enhancement</category>
    <summary>Universal high-standard historical photo restoration protocol that adapts to era, subject count, and damage severity.</summary>
    <status>recommended</status>
  </file>

  <file name="PROMPT Summarize Chat v3.txt">
    <category>writing_summaries_and_content_tools</category>
    <summary>Conversation summarizer producing key points, themes, and actionable takeaways.</summary>
    <status>stable</status>
  </file>
  <file name="PROMPT Lingustic Profiler v3.md">
    <category>writing_summaries_and_content_tools</category>
    <summary>Linguistic fingerprinting prompt to profile tone, habits, and stylistic markers.</summary>
    <status>stable</status>
  </file>
  <file name="PROMPT InfographicGPT v7 Gemini.md">
    <category>writing_summaries_and_content_tools</category>
    <summary>Transforms sources into infographic-ready content with strong hierarchy and visual logic.</summary>
    <status>stable</status>
  </file>
  <file name="PROMPT Steve's Fact Extractor v4.txt">
    <category>writing_summaries_and_content_tools</category>
    <summary>Extracts atomic factual claims into structured, citation-ready units for research workflows.</summary>
    <status>stable</status>
  </file>
  <file name="PROMPT Steve's Fact Narrator v4.txt">
    <category>writing_summaries_and_content_tools</category>
    <summary>Turns extracted facts into coherent narrative prose while preserving evidence boundaries.</summary>
    <status>stable</status>
  </file>
  <file name="PROMPT Chat Conversation Abstractor v2.md">
    <category>writing_summaries_and_content_tools</category>
    <summary>Produces a formal abstract of conversations with claims, evidence, and open questions.</summary>
    <status>stable</status>
  </file>
  <file name="PROMPT Steve's Content Decoder v01.txt">
    <category>writing_summaries_and_content_tools</category>
    <summary>Clarifies dense/ambiguous content and returns structured highlights.</summary>
    <status>stable</status>
  </file>
  <file name="PROMPT Steve's Quick Editor v03.txt">
    <category>writing_summaries_and_content_tools</category>
    <summary>Fast editorial cleanup focusing on clarity and flow with brief change notes.</summary>
    <status>stable</status>
  </file>
  <file name="PROMPT Quick Writing Cleanup v3.md">
    <category>writing_summaries_and_content_tools</category>
    <summary>Lightweight grammar/verbosity/readability cleanup without meaning drift.</summary>
    <status>stable</status>
  </file>
  <file name="PROMPT Image Citation Builder v2.md">
    <category>writing_summaries_and_content_tools</category>
    <summary>Builds standardized, traceable citations for images, especially archival photographs.</summary>
    <status>stable</status>
  </file>

  <file name="PROMPT Research Assignment v0.md">
    <category>research_and_analysis_agents</category>
    <summary>Legacy deep-research assignment template defining best practices and output schemas.</summary>
    <status>legacy</status>
  </file>
  <file name="PROMPT Research Agent Assignment v2.1.md">
    <category>research_and_analysis_agents</category>
    <summary>Reusable research-agent operating spec with classification, verification, and structured deliverables.</summary>
    <status>recommended</status>
  </file>
  <file name="PROMPT Contract-First Genealogy System Prompt v3.1.md">
    <category>research_and_analysis_agents</category>
    <summary>GPS-anchored contract-first genealogy assistant system prompt with staged workflow and JSON schemas.</summary>
    <status>recommended</status>
  </file>

  <file name="GPT Website Frontend GPT v3.txt">
    <category>gpt_shells_and_configs</category>
    <summary>Template for domain-fronted GPTs that search a specific site before answering and end with a topic menu.</summary>
    <status>stable</status>
  </file>
  <file name="GPT - Open GeneaGPT Beta 0.4 (2024-01-22b).txt">
    <category>gpt_shells_and_configs</category>
    <summary>Identity and operating spec for Open GeneaGPT, including tone, standards, and response structure.</summary>
    <status>stable</status>
  </file>

  <file name="LICENSE">
    <category>license</category>
    <summary>Creative Commons BY-NC-SA 4.0 license text for repository contents.</summary>
    <status>stable</status>
  </file>
</repository_index>
