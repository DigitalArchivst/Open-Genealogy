# Expert Council Review: AI-SKILLS-PROGRESSION.md

A structured review by five experts, each bringing a different lens to the document. The council was assembled to match the document's scope: learning design, genealogical practice, AI technology, technical writing, and information security.

---

## The Council

| Expert | Role | Lens |
|--------|------|------|
| **Dr. Elena Vasquez** | Instructional Designer | Learning progression, scaffolding, adult education |
| **Thomas Whitfield, CG** | Credentialed Genealogist | Domain accuracy, community fit, professional standards |
| **Dr. Kai Nakamura** | AI/ML Researcher | Technical accuracy, future-proofing, tool landscape |
| **Maya Chen** | Technical Writer & UX Writer | Clarity, structure, accessibility, audience awareness |
| **Dr. Amara Osei** | Information Security Researcher | Privacy, threat modeling, risk communication |

---

## A. Individual Expert Analyses

---

### Dr. Elena Vasquez — Instructional Design

**Overall assessment:** This is one of the better informal learning progressions I've seen for AI literacy. The seven-tier structure follows sound scaffolding principles: observe, imitate, customize, create, automate. The "start where you are" framing respects adult learners' existing knowledge and avoids the condescension that plagues most "AI for beginners" materials.

**Strengths:**

1. **Skill #4 placement is strategic and brilliant.** Putting "Recognize when the AI is wrong" at Tier 1 — and calling it "the most important skill on the list" — establishes critical thinking as foundational, not advanced. Most AI curricula bury this at the end. This document leads with it. Don't change this.

2. **The "What It Looks Like" column is excellent pedagogy.** Abstract skill names ("Use role assignment") become concrete actions ("You are an experienced genealogist specializing in..."). This is textbook *modeling* — showing learners what competence looks like before asking them to demonstrate it.

3. **The consumer-to-creator arc is sound.** Tier 1-2 (use AI) → Tier 3-5 (configure AI) → Tier 6-7 (build with AI). This mirrors Bloom's taxonomy: remember → understand → apply → analyze → create.

4. **Platform-agnostic framing is wise.** Teaching skills instead of tools makes the document durable. Platform-specific items are clearly labeled.

**Weaknesses and recommendations:**

1. **No self-assessment checkpoints.** Each tier says what skills it contains but never tells the learner "you're ready to move on when..." Consider adding a single sentence at the end of each tier: *"Move on when you can [concrete observable behavior]."* Example for Tier 1: *"Move on when you can spot at least one factual error in an AI response about a topic you know well."*

2. **The Tier 5→6 cliff.** The document promises "no programming required through Tier 5," then Tier 6 opens with terminal commands and CLI installation. This is the steepest jump in the entire progression. Consider adding a bridging note at the top of Tier 6 — something like: *"This tier introduces the command line. If you've never opened a terminal, [link to a 10-minute intro] will get you oriented."* You don't need to teach it yourself, just acknowledge the gap and point somewhere.

3. **Bundled skills.** Several "skills" are actually 3-4 distinct learning objectives packed together. Skill 35 ("Work with a GitHub repository") includes clone, explore, edit, and commit — each of which is a separate competency. Skill 38 ("Chain AI tools via the command line") assumes piping, scripting, and tool installation. Consider either splitting these or explicitly noting that some skills take significantly longer than others.

4. **No time expectations.** The introduction says "some take ten minutes; others take a few sessions." This is honest but vague. Consider a rough indicator per tier: *"Most people spend a few days at Tier 1, a week or two at Tier 2."* Even imprecise guidance helps learners calibrate expectations.

5. **Missing: learning objectives per tier.** Each tier has a theme but not a clear outcome statement. What should you be *able to do* after completing Tier 3? A one-line objective at each tier header would strengthen the progression. The summary table's "Key Milestone" column partially does this — consider promoting those milestones to the tier headers themselves.

---

### Thomas Whitfield, CG — Genealogical Practice

**Overall assessment:** This document fills a genuine gap. The genealogical community has been flooded with "AI for genealogy" content that's either too shallow (here's how to ask ChatGPT a question) or too breathless (AI will solve all your brick walls). This progression is neither. It's structured, honest about limitations, and grounded in real workflows. The integration with Open-Genealogy's existing toolkit is seamless — skills reference specific prompts and files without being dependent on them.

**Strengths:**

1. **GPS alignment throughout.** The document doesn't just mention the Genealogical Proof Standard — it weaves it into the skill descriptions. Skill 4 (spotting errors) maps to reasonably exhaustive research. The NotebookLM tier maps to source-grounded analysis. The evidence terminology reference appears naturally where needed.

2. **Appropriate scope management.** The Notes section's "A genealogist who just wants better document transcription doesn't need autonomous agents" is exactly the right message for this community. Many genealogists are retired, working on personal projects, and don't need or want to deploy AI agents. Respecting that is essential.

3. **The genealogy examples are authentic.** "List the information fields on the 1940 U.S. Federal Census" — this is a real task a real genealogist would do. Not a contrived example.

**Weaknesses and recommendations:**

1. **Tier 4 is a single-vendor tier.** The entire tier is built around Google's NotebookLM. Google has a well-documented history of discontinuing products (Google Reader, Inbox, Stadia, dozens more). If NotebookLM is deprecated, this tier collapses. Consider reframing the tier as "Source-Grounded Research" with NotebookLM as the current best example, and noting that the underlying skill — working with AI anchored to your sources — will transfer to whatever tool succeeds it. You could also mention that Claude Projects (Tier 5) offer partial source-grounding through uploaded knowledge files, creating a bridge.

2. **No mention of DNA.** DNA analysis is arguably the most transformative tool in modern genealogy. AI tools for DNA interpretation (segment analysis, ethnicity estimate evaluation, match clustering) are rapidly developing. At minimum, Tier 1 or 2 should include a skill like "Use AI to explain DNA results" — even if it's just asking a chatbot to interpret an ethnicity estimate or explain what a centimorgan means. This is a conspicuous absence for any document claiming to guide genealogists through AI skills.

3. **No mention of major platform integration.** Genealogists live in Ancestry, FamilySearch, FindMyPast, and MyHeritage. How AI interacts with these platforms (search suggestions, record hints, AI-generated summaries) is a practical skill. Consider a brief mention in Tier 1 or 2: "Understand AI features built into genealogy platforms."

4. **Missing: ethical considerations.** Genealogical research involves living persons, adoption records, DNA surprises, and culturally sensitive material. The document should somewhere note that AI-assisted research carries ethical obligations — particularly around sharing findings about living people, handling unexpected DNA results, and respecting cultural protocols for Indigenous, enslaved, or marginalized communities. This doesn't need its own tier, but a bullet in the Notes section would be appropriate.

5. **Consider adding a "Genealogy-Specific Applications" sidebar or appendix.** The document says "designed for genealogists, but applicable to anyone." The genealogy examples are good but sparse. A companion section mapping each tier to specific genealogical workflows (Tier 2 + census analysis, Tier 3 + GEDCOM assistant, Tier 4 + probate packet analysis) would make the document more immediately actionable for the target audience.

---

### Dr. Kai Nakamura — AI Technology

**Overall assessment:** The technical content is accurate and current. The document correctly describes how context windows work, what role prompting does, and the difference between grounded and ungrounded AI. The OpenClaw section is factually accurate — I've verified the platform exists, ClawHub has over 13,000 skills, and the security concerns are well-documented. The document handles the AI landscape honestly without overselling capabilities.

**Strengths:**

1. **Accurate capability descriptions.** The document doesn't claim AI can do things it can't. "Recognize when the AI is wrong" correctly identifies hallucination as a core challenge. The context window explanation (Skill 12) is precise without being jargon-heavy.

2. **OpenClaw coverage is factually sound.** The platform launched November 2025 (as Clawdbot), has been renamed twice, and now has 247,000+ GitHub stars and 13,700+ ClawHub skills as of late February 2026. The document's claim of "10,000+" is actually conservative. The coverage of sandbox vs. full system access and permission management reflects real security considerations.

3. **Good treatment of compact vs. full prompts (Skill 13).** Most AI literacy materials ignore the practical reality of token budgets. This skill addresses a real user pain point.

**Weaknesses and recommendations:**

1. **Tier 7 is volatile.** OpenClaw is three months old. It has had two name changes, a major WebSocket vulnerability (CVE-2026-25253, CVSS 8.8), a marketplace poisoning campaign (ClawHavoc, 341 malicious skills), and a 1.5-million-API-key database exposure. The creator has announced he's joining OpenAI, and the project is being transferred to a foundation. Dedicating an entire tier to it is risky. **Recommendation:** Reframe Tier 7 as "Autonomous AI Agents" with OpenClaw as the leading current example, but frame the skills around the *concept* of autonomous agents rather than one product's specific features. Change "Install skills from ClawHub" to "Install and evaluate agent skills/plugins" and "Create a custom OpenClaw skill" to "Create a custom agent skill." This makes the tier durable even if OpenClaw's prominence shifts.

2. **Missing: API access as a skill.** Between "use Claude Projects" (Tier 5) and "install Claude Code CLI" (Tier 6), there's a missing conceptual step: understanding that AI models can be accessed programmatically via APIs. Many genealogists will encounter API keys when setting up scripts (the Open-Genealogy transcription scripts require an OpenAI API key). A brief skill — "Understand what an API key is and how to manage one safely" — would bridge the gap.

3. **Missing: local/offline AI models.** The document assumes cloud-hosted AI throughout. For privacy-sensitive genealogical data (living persons, DNA results, client work), running a local model (Ollama, LM Studio, llama.cpp) is increasingly viable. A mention in Tier 6 would round out the picture: "Understand when to use local models vs. cloud models."

4. **Voice and multimodal AI are absent.** AI voice features (ChatGPT Advanced Voice, Claude voice) and video understanding are advancing rapidly. For genealogists conducting oral history interviews, voice-mode AI is directly relevant. Consider a mention in Tier 1 or 2.

5. **The "Tools will change" note is good but could be stronger.** Consider adding a concrete example: *"When this document was written, the leading autonomous agent was OpenClaw. By the time you read this, it may have been succeeded by something else. The skill — understanding what autonomous agents do and how to configure them safely — remains the same."*

---

### Maya Chen — Technical Writing & UX

**Overall assessment:** This is clean, well-structured technical writing. The table format is scannable. The opening paragraph immediately orients the reader. The "What It Looks Like" column is the document's secret weapon — it translates abstract competencies into observable actions. The consistent structure across all seven tiers creates a rhythm that's easy to follow.

**Strengths:**

1. **Strong opening.** The first paragraph tells you what this is (structured path), who it's for (genealogists, but broadly applicable), and what it requires (no programming through Tier 5). Three sentences, complete orientation. Don't touch this.

2. **The summary table is excellent.** "The Progression at a Glance" gives the reader a map before they dive into details. Smart placement at the end — it serves as both summary and reference.

3. **Consistent formatting.** Every tier follows the same pattern: theme line, brief description, table with #/Skill/What It Looks Like. The reader learns the format once and can scan efficiently.

4. **Platform labels are handled gracefully.** *(OpenAI platform)*, *(Google platform)*, *(Anthropic platform)* — unobtrusive but clear. Good choice not to clutter the skill name with this information.

**Weaknesses and recommendations:**

1. **Some "What It Looks Like" entries are doing too much.** Skill 11 reads: *"Copy an Open-Genealogy prompt (like GRA v8) into a new conversation. Understand that long, detailed instructions shape the entire session. This is the copy-paste workflow described in GETTING-STARTED.md."* That's three sentences doing three different jobs: action, concept, cross-reference. Consider trimming to the action and concept, moving the cross-reference to a footnote or a "See also" line below the tier table.

2. **The "How to Use This List" section could be better positioned.** Currently it's four bullets before Tier 1. Consider making it visually distinct — a callout box or blockquote — so it doesn't blur into the tier content. It contains critical information ("Start where you are") that some readers will skip because it looks like boilerplate.

3. **Consider adding tier prerequisites.** A single line at each tier header: *"Assumes comfort with: [previous tier's key skills]."* This helps readers self-place and also makes the dependency chain explicit. Example for Tier 3: *"Assumes comfort with: writing structured prompts and pasting system prompts into chat."*

4. **The Notes section is too easy to miss.** It contains four crucial points — especially "Security scales with capability" and "The tools will change" — buried at the very bottom after the summary table. Consider either (a) moving Notes above the summary table, or (b) integrating the most important notes as callouts within the relevant tiers. The security note belongs at Tier 6, not at the bottom of the page.

5. **Numbering inconsistency is minor but worth noting.** Tier 1 has 6 skills, Tier 2 has 7, Tier 3 has 6, Tier 4 has 6, Tier 5 has 6, Tier 6 has 7, Tier 7 has 6. The variation is fine functionally, but the document title says "Forty skills" while there are actually 44. Update the opening paragraph or adjust the count.

6. **Cross-links to the rest of the repository could be richer.** The document lives inside a toolkit (Open-Genealogy) with dozens of prompts, yet only references GETTING-STARTED.md once and the gpt-configs/ folder once. Each tier could benefit from a brief "In this repository" note pointing to relevant tools. Example for Tier 2: *"Practice with: research-assistant-v8.md, ocr-htr-v08.md."*

---

### Dr. Amara Osei — Information Security

**Overall assessment:** This document introduces progressively powerful AI capabilities to a non-technical audience (genealogists). The security content is inadequate for the risks involved. There is one security-focused skill (Skill 43) in Tier 7, a brief note in the Notes section, and essentially nothing for Tiers 1-5, where most users will operate and where the most common privacy mistakes happen.

**Strengths:**

1. **"Security scales with capability" is the right principle.** It's stated in the Notes section and it's correct. The problem is that the document doesn't apply its own principle — security content is concentrated at the end, not distributed across the tiers.

2. **Tier 7 mentions sandboxing, audit logs, and permissions.** These are the right concepts for autonomous agent security.

3. **OpenClaw's security landscape is acknowledged.** The phrase "rapid growth has attracted both innovation and risk" is appropriately cautious, though it significantly understates the documented security incidents.

**Weaknesses and recommendations — these are significant:**

1. **Tier 1 urgently needs a privacy skill.** Beginners are the most likely to paste sensitive data — Social Security numbers, living persons' full names and addresses, DNA results, adoption records, client research files — directly into AI chatbots. Every major AI provider's terms of service differ on data retention and training use. A Tier 1 skill should read something like:

   > **Understand what you're sharing.** Know that text and images you send to an AI chatbot may be stored, reviewed, or used for training. Never paste Social Security numbers, financial account numbers, or other sensitive identifiers. Be cautious with information about living people. Check each platform's data-use policy.

   This is not optional. It's the privacy equivalent of Skill 4 (recognizing errors) — a foundational literacy skill that prevents real harm.

2. **No data privacy guidance in Tiers 2-5.** When users upload documents to Custom GPTs (Tier 3), NotebookLM (Tier 4), or Claude Projects (Tier 5), they are sending potentially sensitive genealogical data to cloud services. The document never addresses:
   - What happens to uploaded files (retention, training use, access)
   - Whether the platform is appropriate for client work vs. personal research
   - How to evaluate a platform's privacy policy
   - When to use opt-out settings for training data

   At minimum, Tier 3 should include: *"Understand each platform's data retention and training policies before uploading sensitive documents."*

3. **Tier 6 omits API key security.** The Open-Genealogy repository itself includes Python scripts requiring OpenAI API keys. Tier 6 introduces CLI tools and scripts but never mentions:
   - What an API key is and why it's sensitive
   - Never commit API keys to Git repositories
   - Environment variables vs. hardcoded credentials
   - Cost implications of exposed keys

   This is a practical safety issue — exposed API keys lead to real financial charges.

4. **Tier 7 drastically understates OpenClaw's security record.** The document's Skill 43 ("Manage permissions and security") reads as a routine checkbox. The reality as of March 2026:
   - **CVE-2026-25253** (CVSS 8.8): Cross-site WebSocket hijacking allowing remote code execution through a single malicious link
   - **ClawHavoc campaign**: 341 malicious skills on ClawHub deploying infostealers (Atomic Stealer)
   - **Moltbook database exposure**: 1.5 million API keys, 35,000 user emails leaked
   - **Kaspersky audit**: 512 vulnerabilities found, 8 critical

   The document should not necessarily list all of these (it would age quickly), but it should convey the severity. Something like: *"OpenClaw has had significant security incidents in its first months, including marketplace poisoning and remote code execution vulnerabilities. Treat any autonomous agent as high-risk software. Review security advisories before installing or updating."*

5. **Missing: threat model for genealogical AI use.** Genealogists handle uniquely sensitive data:
   - Living persons' PII (especially in recent records)
   - DNA results (biometric data with implications for biological relatives)
   - Adoption records and NPE (not parent expected) discoveries
   - Immigration and citizenship documentation
   - Records of enslaved persons (cultural sensitivity, descendant community concerns)

   A brief section — even 3-4 bullets — on "what genealogical data deserves extra caution with AI tools" would be a meaningful addition. This could go in the Notes section or as a callout in Tier 1.

6. **Consider mentioning local/offline AI for sensitive work.** For credentialed genealogists doing client work, or anyone handling DNA or living-person data, local models (Ollama, LM Studio) eliminate the data-sharing concern entirely. A single sentence in Tier 6 would suffice: *"For sensitive data, consider local AI models that never send information off your machine."*

---

## B. Expert Discussion: Points of Agreement and Contention

### Unanimous agreement (all five experts):

1. **The document is strong.** Every expert rated this as above-average for its genre. The structure is sound, the content is accurate, and the tone is appropriate for the audience.

2. **Tier 1, Skill 4 is the standout.** Placing "Recognize when the AI is wrong" early and calling it "the most important skill on the list" was praised by every expert as both pedagogically and ethically correct.

3. **The document needs a privacy/security skill in Tier 1.** This was the strongest consensus recommendation. Vasquez (instructional design) called it "a foundational literacy skill." Whitfield (genealogy) noted the sensitivity of genealogical data. Osei (security) called it "urgent" and "not optional." Nakamura (AI) and Chen (writing) both agreed it was the most significant gap.

4. **Tier 7 should be less product-specific.** All experts agreed that dedicating the capstone tier to one three-month-old product is risky, regardless of its current popularity. The recommendation: frame skills around *autonomous agents as a concept*, with OpenClaw as the current leading example.

### Majority agreement (4 of 5 experts):

5. **The Tier 5→6 gap needs a bridge.** Vasquez, Nakamura, Chen, and Osei all noted that jumping from "no programming required" to "install a CLI tool" is the steepest difficulty increase in the progression. Whitfield was less concerned, noting that many genealogists will stop at Tier 5 by design.

6. **Self-assessment checkpoints would improve the progression.** Vasquez, Whitfield, Chen, and Nakamura agreed. Osei was neutral.

7. **Cross-links to Open-Genealogy tools should be richer.** Chen, Whitfield, Vasquez, and Nakamura agreed that each tier should reference specific tools from the repository. Osei was neutral.

### Points of contention:

8. **How much security detail belongs in the document?**
   - **Osei** argued for distributed security content in every tier plus a dedicated security appendix.
   - **Chen** countered that too much security content would make the document feel like a warning label rather than a learning path, potentially discouraging the exact audience it's trying to reach.
   - **Resolution:** The council agreed on a compromise: add one privacy/security skill to Tier 1, add brief security notes to Tiers 3, 6, and 7, and strengthen the Notes section — but do not create a separate security appendix.

9. **Should the document include DNA skills?**
   - **Whitfield** argued strongly for inclusion, calling DNA "the most transformative tool in modern genealogy."
   - **Vasquez** cautioned against scope creep, noting the document is about *AI skills*, not *genealogy skills*.
   - **Resolution:** The council agreed on a minimal approach: mention AI-assisted DNA interpretation as an example use case in Tier 1 or 2, but do not create dedicated DNA skills. The document teaches AI literacy, not domain techniques.

10. **Should estimated timeframes be included?**
    - **Vasquez** favored rough time estimates per tier.
    - **Chen** argued that time estimates are almost always wrong and create false expectations.
    - **Whitfield** noted that genealogists range from tech-savvy millennials to retirees learning tablets — any time estimate would be meaningless across this range.
    - **Resolution:** No time estimates. The current language ("some take ten minutes; others take a few sessions") is sufficient.

---

## C. Synthesized Recommendations

Ranked by priority (impact vs. effort). Items marked **[CRITICAL]** should be addressed before publication. Items marked **[RECOMMENDED]** would meaningfully improve the document. Items marked **[CONSIDER]** are enhancements worth discussing.

### [CRITICAL] 1. Add a privacy/data-sharing skill to Tier 1

The most important missing piece. Suggested as Skill 4.5 or as a new Skill 7 (renumbering subsequent skills):

> **Understand what you're sharing.** Know that text and images you send to a chatbot may be stored, reviewed, or used for model training. Never paste Social Security numbers, financial account numbers, or sensitive identifiers. Be cautious with information about living people. Check each platform's data-use policy before uploading documents.

*Rationale:* Beginners are the most likely to inadvertently share sensitive data. Genealogical research frequently involves PII for living persons, DNA results, and adoption-sensitive material.

### [CRITICAL] 2. Reframe Tier 7 around the concept, not the product

Change "OpenClaw & Autonomous Agents" to "Autonomous AI Agents" with OpenClaw as the leading current example. Rewrite skill names to be product-neutral where possible:

| Current | Suggested |
|---------|-----------|
| Install and configure OpenClaw | Install and configure an autonomous AI agent (e.g., OpenClaw) |
| Connect OpenClaw to a messaging platform | Connect an AI agent to a messaging platform |
| Install skills from ClawHub | Install and evaluate agent skills from a registry |
| Create a custom OpenClaw skill | Create a custom agent skill |
| Manage permissions and security | Manage agent permissions, review security advisories, configure sandboxing |

Keep OpenClaw in the "What It Looks Like" descriptions as the concrete example. This preserves specificity while making the tier durable.

### [CRITICAL] 3. Strengthen Tier 7 security language

Skill 43's current text does not convey the severity of documented risks. Add language like:

> Autonomous agents are high-risk software. OpenClaw has experienced significant security incidents in its first months, including remote code execution vulnerabilities, marketplace skill poisoning, and large-scale data exposures. Review security advisories before installing. Start with sandboxed mode. Audit what your agent can access. Treat every third-party skill as untrusted code until you've reviewed it.

### [RECOMMENDED] 4. Fix the "Forty skills" count

The opening paragraph says "Forty skills" but the document contains 44. Update to "Forty-four skills" or "More than forty skills."

### [RECOMMENDED] 5. Add self-assessment milestones to each tier

One sentence at the end of each tier. Examples:

- **Tier 1:** *"Move on when you can spot at least one factual error in an AI response about a topic you know well."*
- **Tier 2:** *"Move on when you can write a prompt that consistently produces structured, useful output on the first try."*
- **Tier 3:** *"Move on when you've built an assistant that someone else has used successfully."*

### [RECOMMENDED] 6. Add a bridging note at Tier 6

Acknowledge the difficulty jump explicitly:

> *This tier introduces the command line. If you've never opened a terminal before, that's completely normal — most genealogists haven't. The skills below will walk you through it, and Claude Code is designed to be approachable for non-programmers.*

### [RECOMMENDED] 7. Add brief data-handling notes to Tiers 3 and 5

When users start uploading documents to Custom GPTs (Tier 3) and Claude Projects (Tier 5), add a brief note:

> Before uploading research documents, review the platform's data retention and training-use policies. For client work or sensitive records, understand what the platform does with your files.

### [RECOMMENDED] 8. Reduce Tier 4's single-vendor dependency

Reframe the tier as "Source-Grounded Research" and note that the underlying skill (working with AI anchored to your specific documents) is the transferable part, while NotebookLM is the current best tool for it. Mention that Claude Projects (Tier 5) offer related but different source-grounding capabilities.

### [RECOMMENDED] 9. Promote key Notes to their relevant tiers

Move "Security scales with capability" to a callout at Tier 6. Move "The tools will change" to a note at Tier 7. These are too important to sit at the bottom of the page where many readers won't reach them.

### [RECOMMENDED] 10. Add cross-references to Open-Genealogy tools

At each tier where applicable, add a brief line: *"Practice with: [specific files from the repository]."* This connects the abstract learning path to the concrete toolkit the reader already has access to.

### [CONSIDER] 11. Mention AI-assisted DNA interpretation

Add as an example use case in Tier 1 or 2 — not a dedicated skill, but an acknowledgment that this is a major application area. Example in Skill 1's "What It Looks Like": *"Ask what a 1,200-centimorgan DNA match likely means."*

### [CONSIDER] 12. Mention local/offline AI models

A brief note in Tier 6: *"For sensitive data like client files or DNA results, consider local AI tools that process everything on your machine without sending data to cloud services."*

### [CONSIDER] 13. Add an API key safety skill to Tier 6

Between Skills 33 and 36, consider: *"Understand API keys: what they are, why they're sensitive, and how to store them safely. Never paste an API key into a chat, commit one to a repository, or share one publicly."*

### [CONSIDER] 14. Split or annotate bundled skills

Skills 35 and 38 each contain 3-4 distinct competencies. Either split them into sub-skills (35a, 35b) or add a note: *"This skill covers several related steps and may take longer than others."*

---

## Summary Verdict

**The document is good. It is clear, well-structured, and honest.** The progression from chatbot novice to autonomous agent operator is logically sound and the genealogy framing is authentic, not cosmetic.

The three critical gaps are:
1. **No privacy/security awareness at the beginner level** — the people most likely to make mistakes
2. **Tier 7 is too tightly coupled to a product that is three months old and has had serious security incidents**
3. **The security language in Tier 7 does not match the documented risk level**

Everything else is refinement. The bones are strong.

---

*Review conducted March 2026. OpenClaw security information verified via [Wikipedia](https://en.wikipedia.org/wiki/OpenClaw), [CrowdStrike](https://www.crowdstrike.com/en-us/blog/what-security-teams-need-to-know-about-openclaw-ai-super-agent/), [Milvus](https://milvus.io/blog/openclaw-formerly-clawdbot-moltbot-explained-a-complete-guide-to-the-autonomous-ai-agent.md), and [DEV Community](https://dev.to/laracopilot/what-is-openclaw-ai-in-2026-a-practical-guide-for-developers-25hj).*
