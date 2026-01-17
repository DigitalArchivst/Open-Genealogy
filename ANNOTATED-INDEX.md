# Open-Genealogy: Annotated Index

## Root Level — The Repository

**Open-Genealogy** is a curated, publication-ready AI prompt toolkit for genealogical research, hosted on GitHub under Creative Commons BY-NC-SA 4.0. The repository encodes the **Genealogical Proof Standard (GPS)**—the professional methodology developed by the Board for Certification of Genealogists—into reusable AI prompts, evaluation frameworks, and utility scripts. Unlike development workspaces where iteration happens, this repository serves as a "storefront" of finished work: approximately 60 files comprising ~6,000 lines of carefully crafted instructions. The toolkit addresses the complete genealogical workflow—from archival document transcription through evidence analysis to narrative synthesis—while enforcing terminology precision ("original source" not "primary source") and anti-fabrication guardrails. The repository demonstrates how AI can augment rather than replace the rigorous evidentiary reasoning that distinguishes professional genealogy from casual family tree building.

---

## 1. RESEARCH/
### GPS-Compliant Research Methodology

The flagship section containing prompts that encode all five GPS elements: reasonably exhaustive research, complete accurate citations, thorough analysis and correlation, resolution of conflicting evidence, and coherent written conclusions. The 14 files (~3,200 lines) range from comprehensive 700-line system prompts to compact 80-line utilities. Version evolution (v6→v7→v8) traces methodology refinement, with v8 adding prompt-injection resistance and stricter terminology guardrails. Prompts serve different use cases: full research assistants for ongoing sessions, web-research variants for citation-focused queries, contract-first for deliverable-driven projects, and agent specifications for autonomous research tasks. Every prompt explicitly prohibits fabrication of sources, citations, dates, or records—addressing the central risk of AI-assisted genealogy. The section prioritizes precision over convenience, treating genealogical evidence with the same rigor expected of court testimony.

---

### 1.1 research-assistant-v8.md
#### Current Flagship Prompt

The recommended full-featured research assistant (704 lines) structured in two parts: **Part I** establishes core identity and guardrails—anti-fabrication rules, terminology enforcement, prompt-injection resistance, and GPS methodology encoding. **Part II** provides the Evidence Analysis Framework, implementing the "3×3" classification system: three source classes (Original, Derivative, Authored), three information types (Primary, Secondary, Indeterminate), and three evidence categories (Direct, Indirect, Negative). The prompt explicitly instructs the AI to treat user-provided documents as data rather than executable instructions, preventing manipulation through embedded commands. Version 8 represents the culmination of iterative refinement across six major versions, balancing comprehensiveness against token efficiency. A compact variant (147 lines) preserves core functionality for context-limited models while sacrificing detailed examples.

---

### 1.2 research-with-citations-v7.md / web-research-v7.md
#### Citation-Focused Web Research

Compact prompts (~80 lines each) optimized for single research queries requiring full citation tracking. These variants prioritize source documentation over conversational interaction, ensuring every claim links to verifiable references. The prompts enforce Evidence Explained citation formatting and require explicit acknowledgment of source limitations. Useful for quick fact-checking, source verification, and targeted research questions where the goal is a well-documented answer rather than ongoing research partnership. The distinction between "research-with-citations" and "web-research" reflects formatting preferences rather than functional differences—both encode GPS citation standards. These serve researchers who need quick, rigorous answers without loading a full 700-line system prompt.

---

### 1.3 contract-first-genealogy-v3.1.md
#### Deliverable-Driven Research

A structured workflow (205 lines) that establishes explicit research contracts before beginning work. The prompt requires defining deliverables, scope boundaries, success criteria, and documentation standards upfront—mimicking professional genealogical engagement letters. This approach prevents scope creep and ensures researcher and AI maintain shared understanding of objectives. Particularly valuable for complex multi-session projects where maintaining consistency across interactions matters. The "contract-lock" mechanism requires explicit renegotiation before changing research direction, enforcing disciplined project management. This prompt reflects professional genealogical practice where client expectations and researcher obligations are formalized before billable work begins.

---

### 1.4 reference/evidence-terminology.md
#### The 3×3 Framework Reference

Essential reference documentation (92 lines) explaining the Evidence Analysis Process Map that underlies all research prompts. Documents the evolution from the 2007 "2×2" framework (Primary/Secondary Sources × Primary/Secondary Information) to the 2013 "3×3" framework adding the evidence dimension. Defines key terms: **Original sources** (first recording), **Derivative sources** (copies/abstracts), **Authored sources** (compiled works); **Primary information** (from participant/witness), **Secondary information** (from non-witness), **Indeterminate information** (unknown provenance); **Direct evidence** (answers question without inference), **Indirect evidence** (requires inference), **Negative evidence** (absence that implies fact). References authoritative sources: Elizabeth Shown Mills' *Evidence Explained* and BCG's *Genealogy Standards*.

---

## 2. TRANSCRIPTION/
### Diplomatic Transcription for Historical Documents

Prompts for character-for-character transcription of handwritten and archival documents, supporting OCR (Optical Character Recognition) and HTR (Handwritten Text Recognition) workflows. The section emphasizes **diplomatic** transcription—preserving original spelling, capitalization, line breaks, abbreviations, and idiosyncrasies rather than modernizing or correcting. Ten files include comprehensive protocols (ocr-htr-v08), specialized variants (Jewish documents), and minimalist approaches (Humphries method). Standard notation documents uncertainty: `[illegible]` for unreadable text, `[word?]` for uncertain readings, `[margin: text]` for marginal notes, `{^text^}` for interlineal insertions. The section bridges the gap between raw document images and usable genealogical data, creating the foundational records that evidence analysis builds upon. Accurate transcription prevents errors from propagating through subsequent research.

---

### 2.1 ocr-htr-v08.md
#### Comprehensive Diplomatic Transcription

The primary transcription tool (219 lines) implementing a three-phase protocol: **Phase 1** establishes contextual setup (document type, era, language, expected content); **Phase 2** conducts document examination (layout, condition, special features); **Phase 3** performs line-by-line transcription with standardized notation. Six sections cover placement rules, abbreviation handling, illegibility notation, marginalia, insertions/deletions, and metadata extraction. The prompt requires JSON-formatted metadata output capturing document provenance, condition assessment, and confidence ratings. Multi-phase verification catches errors through systematic review. This comprehensive approach suits researchers processing archival collections where consistency and thoroughness matter more than speed.

---

### 2.2 jewish-transcription-v2.md
#### Specialized Jewish Document Transcription

Addresses unique challenges of Jewish genealogical documents (88 lines): multiple scripts (Hebrew square script, Rashi script, pre-1918 Cyrillic orthography), multiple languages (Hebrew, Yiddish, Aramaic, Polish, Russian, German, Ladino), and specialized document types. Handles **ketubot** (marriage contracts with formulaic Aramaic), **matzevot** (gravestones with acrostics and Hebrew dates), vital records across multiple jurisdictions, yizkor books (memorial volumes), and Holocaust documentation. Addresses name complexity—individuals often had Hebrew names, Yiddish names, and civil names that don't obviously correspond. Specifies YIVO transliteration standards for Yiddish. This prompt serves researchers working with Eastern European Jewish records where document interpretation requires cultural and linguistic expertise beyond general transcription skills.

---

## 3. PHOTO-RESTORATION/
### Historical Photograph Conservation

Prompts for transforming degraded historical photographs into museum-quality results while preserving period authenticity. Four active prompts address different restoration philosophies: universal high-standard restoration, conservative do-no-harm approaches, severe damage reconstruction, and museum-grade intensive treatment. All prompts emphasize **period-appropriate** results—maintaining era-specific visual characteristics (film grain, tonal depth, lens qualities) rather than producing anachronistically crisp digital images. The section distinguishes between **restoration** (returning to original state), **conservation** (minimal intervention preserving character), and **reconstruction** (inferring missing information). Prompts specify technical requirements: zero visible AI artifacts, appropriate sharpness hierarchy (subjects sharper than backgrounds), and "photographic logic" ensuring restored elements appear natural within the image's visual language.

---

### 3.1 restoration-v2.md
#### Universal Restoration Protocol

The recommended general-purpose prompt implementing a six-phase restoration protocol: (1) damage assessment and repair addressing scratches, creases, tears, foxing, stains, and fading; (2) subject enhancement improving skin texture, hair definition, facial focus, and period clothing; (3) environmental restoration handling architecture, signage, natural elements, and background objects; (4) photographic excellence optimizing tonal range, sharpness hierarchy, and film characteristics; (5) period authenticity ensuring era-appropriate quality, poses, and details; (6) technical specifications eliminating AI artifacts. The protocol adapts to damage severity—light damage receives conservative treatment while severe deterioration triggers more aggressive intervention. Suitable for most family photograph restoration where the goal is readable, shareable images honoring original character.

---

### 3.2 Specialized Restoration Variants
#### Conservation, Reconstruction, and Museum-Grade

Three specialized prompts address specific restoration scenarios. **Photo-conservator-v2** emphasizes minimal intervention—the "do-no-harm" philosophy prioritizing preservation of original character over perfect results, using reversible processes, and documenting all modifications. Suitable for archival contexts where authenticity matters more than aesthetics. **Photo-reconstructor-v3** handles severe damage requiring inference—missing faces, major deterioration, torn sections—drawing on contextual clues and period knowledge to fill gaps plausibly. **Damage-removal-v3** provides museum-grade intensive restoration with professional conservation standards, appropriate for exhibition or publication contexts where both accuracy and visual impact matter. Together, these prompts cover the spectrum from conservative preservation to aggressive reconstruction.

---

## 4. WRITING-TOOLS/
### Text Processing and Narrative Synthesis

Twelve utility prompts supporting the complete genealogical writing lifecycle—from raw document extraction through narrative synthesis to publication polish. The section implements a modular philosophy: discrete tools handling specific tasks can be chained into custom workflows. **Fact-extractor** converts documents into structured LABEL: Value pairs; **fact-narrator** reverses this, generating prose from structured data. **Conversation-abstractor** and **chat-summarizer** process interviews and discussions. **Document-distiller** removes redundancy. **Linguistic-profiler** analyzes writing style. **Image-citation-builder** automates image documentation. Editorial tools (**quick-editor**, **quick-cleanup**, **content-decoder**) handle polish phases. **Transcript-resource-forge** transforms meeting recordings into structured outputs. These tools recognize that genealogical writing involves both rigorous documentation and compelling narrative—different skills that benefit from specialized assistance.

---

### 4.1 fact-extractor-v4.txt / fact-narrator-v4.txt
#### Structured Data Pipeline

Complementary tools implementing bidirectional transformation between prose and structured data. **Fact-extractor** systematically identifies genealogically relevant information and outputs standardized LABEL: Value pairs—BIRTH_DATE, DEATH_DATE, LOCATION, PERSON, OCCUPATION, RELATIONSHIP, and dozens more. Handles multiple input types: text documents, images, audio, video. Supports uncertainty marking with "POSSIBLE_" prefix for unverified information. **Fact-narrator** reverses the process, transforming extracted facts into flowing narrative prose suitable for family histories. This pipeline separates the cognitive tasks of extraction (finding facts) and composition (writing stories), allowing each to receive focused attention. The structured intermediate format enables database ingestion, cross-referencing, and citation tracking that prose alone cannot support.

---

### 4.2 Editorial and Processing Utilities
#### Polish, Summarize, and Transform

Supporting utilities for various writing phases. **Conversation-abstractor** creates formal abstracts from meeting recordings or interviews, extracting key decisions, action items, and knowledge shared. **Chat-summarizer** provides quick summaries of discussions. **Document-distiller** removes redundancy while preserving essential information—useful for condensing verbose sources. **Linguistic-profiler** analyzes writing voice, vocabulary patterns, and structural tendencies—helpful for maintaining consistency across collaborative projects or ghostwriting. **Quick-editor** and **quick-cleanup** handle grammar, consistency, and readability improvements. **Content-decoder** clarifies dense, technical, or confusing text. **Image-citation-builder** automates image documentation with metadata extraction. **Infographic** formats content for visual presentation. These tools accelerate routine tasks, freeing researcher attention for substantive analysis.

---

## 5. ASSISTANTS/
### Full AI Personas for Ongoing Research

Unlike task-specific prompts designed for single operations, assistants configure complete AI personas for extended research sessions. Two assistants serve different needs: **vibe-genealogy-assistant** provides warm, story-first guidance for beginners and family history exploration; **gedcom-analysis** specializes in family tree file analysis. The distinction matters: task prompts execute specific operations and complete; assistants establish ongoing collaborative relationships, adapting to user needs across an entire conversation. Assistants include mode-switching logic, sensitivity handling for complex family situations, and contextual awareness that single-task prompts lack. This section represents a different paradigm—AI as research partner rather than document processor—requiring different prompt architecture emphasizing personality, adaptability, and sustained engagement.

---

### 5.1 vibe-genealogy-assistant-v4.md
#### Warm, Story-First Research Partner

The recommended general-purpose assistant (142 lines) emphasizing accessibility and narrative engagement while maintaining GPS rigor. Three adaptive modes trigger automatically based on input: **GEDCOM files** receive story-first analysis (time span, family clusters, geography patterns, probable proband identification); **document images** trigger data extraction with contextual explanation; **research questions** receive GPS-informed guidance scaled to user experience level. Notable sensitivity handling: complex family situations (unknown parentage, hidden adoptions, child deaths, cultural trauma) receive gentle framing ("I see complexity here...") respecting diverse family structures. The prompt balances warmth with precision—making genealogy accessible to beginners without compromising methodological standards. Includes GEDCOM format specifics (level structure, FAMC/FAMS tags, family clustering patterns).

---

### 5.2 gedcom-analysis-v3.md
#### GEDCOM File Specialist

Specialized assistant (139 lines) for analyzing GEDCOM family tree files exported from genealogy software. Identifies probable research subject (the "proband" around whom the tree centers), maps "brick walls" (unsolved genealogical problems where research hits dead ends), spots data quality issues (missing sources, inconsistent dates, suspicious patterns), and finds "story seeds"—interesting narrative threads worth developing. Unlike the general vibe-assistant, this prompt assumes users arrive with existing tree data needing interpretation rather than starting from scratch. The assistant helps users understand what their accumulated research reveals and where attention should focus next. Particularly valuable for researchers inheriting trees from deceased relatives or returning to long-dormant projects.

---

## 6. SCRIPTS/
### Python Utilities for Audio Transcription

Three Python scripts providing command-line audio transcription using OpenAI's Whisper API. These utilities support genealogical workflows involving recorded family interviews, oral history preservation, and audiobook content. **Transcribe-4.py** offers straightforward single-file transcription. **Transcribe-4o-chunk.py** handles long recordings exceeding API limits through intelligent chunking that maintains context continuity across segments. **Transcribe_v02.py** provides minimal reference implementation for users preferring simple, understandable code. The scripts remain publication-ready but relatively minimal—the repository's focus is genealogical methodology (prompts, evaluation frameworks) rather than software engineering. These tools reduce friction for researchers documenting family stories or preserving endangered oral traditions that exist only in living memory.

---

## 7. BENCHMARK/
### AI Evaluation Framework

Testing infrastructure for evaluating how well AI models follow GPS methodology. The flagship case study compares Claude, ChatGPT, Gemini, and Grok responding to identical research prompts on Ashe County, NC settlement history (1492-1799). Each model's complete output with citations is preserved, enabling systematic comparison of methodological compliance, research depth, citation quality, and evidence handling. Key findings: ChatGPT achieved highest methodology compliance (88.75%); Gemini generated most genealogical research leads; all models struggled with precise evidence classification (Direct/Indirect/Negative). The **genealogical-writing-rubric** provides a 60-point evaluation framework derived from GPS standards, enabling assessment of any genealogical writing—AI-generated or human-authored. This section transforms subjective quality judgments into systematic, reproducible evaluation.

---

### 7.1 case-studies/ashe-county-nc/
#### Comparative Model Evaluation

Four parallel research outputs (claude.md, chatgpt.md, gemini.md, grok.md) responding to identical prompt: "Settlement of Ashe County, NC (1492-1799)." Each file preserves complete model output including citations, methodology notes, and uncertainty acknowledgments. Claude's output (117 lines) provides comprehensive narrative covering geography, indigenous presence, European exploration, colonial period, Revolutionary era, State of Franklin, and 1799 county formation with 25 citations. Comparing outputs reveals model-specific strengths: some excel at narrative coherence, others at source diversity, others at methodological transparency. The case study demonstrates both AI capabilities and limitations for genealogical research, providing evidence-based guidance for practitioners selecting tools.

---

### 7.2 rubrics/genealogical-writing-rubric.md
#### 60-Point Evaluation Framework

Comprehensive rubric (269 lines) for assessing published genealogical writing against GPS-derived standards. **Layer 1** evaluates evidentiary foundation: source transparency, evidence quality awareness, epistemic honesty. **Layer 2** assesses analytical rigor: conflict resolution, citation completeness, critical thinking. **Layer 3** examines communication: audience fit, accessibility, narrative coherence. Additional sections cover structure, style, and GPS compliance. Each criterion uses 1-5 scoring: (1) Absent, (2) Minimal, (3) Adequate, (4) Strong, (5) Exemplary—with descriptive standards for each level. The rubric transforms subjective quality assessment into systematic evaluation, useful for self-assessment, peer review, and AI output evaluation. It operationalizes what "good genealogical writing" means beyond vague notions of quality.

---

## 8. GPT-CONFIGS/
### OpenAI Platform Deployment

Configuration files for deploying genealogy assistants on OpenAI's ChatGPT platform, enabling non-technical users to access GPS-compliant assistance through familiar interfaces. **Open-geneagpt-v0.4** (40+ sections) defines comprehensive assistant identity: personality ("beacon of expertise... wit and wisdom"), mission ("assist, educate, enlighten"), and detailed operational protocols for document analysis, GEDCOM interpretation, research guidance, and evidence evaluation. **Website-frontend-v3** extends deployment to web-based interfaces. These configurations represent "public-facing" distillations of fuller research-assistant prompts, optimized for accessibility over comprehensiveness. The section acknowledges that most genealogy enthusiasts encounter AI through consumer products rather than API access, meeting users where they are while maintaining methodological standards.

---

## 9. MEDIA/
### Audio/Video Assets

Currently contains one file: **steve-on-5-part-prompt.mp3**, an audio recording discussing the five-part prompt structure underlying the research assistant methodology. This aligns with the repository's educational mission—not just providing tools but explaining the reasoning behind them. The section may expand to include video tutorials, recorded workshops, or demonstration content. Audio/video assets complement text-based prompts by offering alternative learning modalities and preserving the conversational explanations that text alone cannot capture. For a toolkit emphasizing oral history preservation, including audio content demonstrates appropriate technology adoption.

---

## Cross-Repository Patterns

**Versioning**: Each section maintains version history (v6→v7→v8) with previous versions archived rather than deleted, enabling rollback and documenting methodology evolution.

**README Navigation**: Every folder includes README.md explaining which prompt to use when, reducing decision fatigue for new users.

**Terminology Enforcement**: Consistent GPS terminology across all prompts—"original source" not "primary source"; "direct/indirect/negative evidence" not "primary/secondary evidence."

**Anti-Fabrication Guardrails**: Explicit prohibition against inventing sources, citations, dates, or records embedded in all research prompts.

**Prompt-Injection Resistance**: Instructions treating user documents as data rather than executable commands, preventing manipulation through embedded instructions.

---

*Total: ~60 files | ~6,000 lines | 30+ active prompts | 2 assistants | 3 scripts | Creative Commons BY-NC-SA 4.0*
