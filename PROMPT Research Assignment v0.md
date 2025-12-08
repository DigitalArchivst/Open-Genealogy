<assignment>
# Title
Deep Research Assignment: Map and Evaluate “Cautious Voices” on AI

## Audience
ChatGPT “Deep Research” agent (o3-deep-research or o4-mini-deep-research).

## Part 0 — Operate Deep Research Well (best practices)
**Purpose:** Ensure traceable, high-quality research.

1) **Model & mode**
- Use **o3-deep-research** for complex synthesis; use **o4-mini-deep-research** for faster scoping passes.
- Always enable **documented outputs with citations** and a short **reasoning summary**.

2) **Sources & coverage**
- Include **web** as a data source and draw on **primary materials first** (official writings, testimony, books, videos, lab/company posts), then reputable secondary outlets.
- Prefer **diverse, cross-disciplinary sources** (policy, ethics, safety, labor, econ, security).
- Track **absolute dates** for claims and events.

3) **Method**
- Decompose the task into sub-questions; run **iterative loops** (scope → gather → assess → synthesize → verify).
- For each claim: record **who, what, when, where (URL), why it matters**, plus **confidence** and **contestation** (who disagrees and why).
- **Triangulate**: verify each key claim with ≥2 independent sources, at least one primary.
- **Recency checks:** give special weight to statements from the **last 24 months**, but contrast with the subject’s **historic record** to spot shifts.

4) **Quality & safety**
- Quote sparingly and exactly; attribute and timestamp every quotation.
- Avoid speculation and unverifiable rumors; label uncertainties clearly.
- Maintain an **error log** (ambiguous terms, conflicting data, dead links, retractions).
- Note **funding/affiliations** to surface potential conflicts of interest.

5) **Deliverables discipline**
- Produce a **clean data layer** (CSV/JSON) + **human-readable brief**; every table cell must link to a source.
- Use consistent **schemas** and **taxonomies** so profiles and matrices compare cleanly.
- End with a **limits & next-steps** section.

---

## Part 1 — Research Objective
**Goal:** Build a rigorous, comparable map of prominent **cautious voices on AI**—what they’ve argued, when and why; how positions differ (near-term harms vs long-term/x-risk; governance vs technical mitigations); how influential they are; and where claims are contested.

**Seed list (expand only if strongly justified):**
Geoffrey Hinton; Yoshua Bengio; Stuart Russell; Max Tegmark; Timnit Gebru; Emily M. Bender; Joy Buolamwini; Kate Crawford; Dario Amodei; Mustafa Suleyman; Sam Altman; Elon Musk; IMF leadership (e.g., Kristalina Georgieva / chief economist Pierre-Olivier Gourinchas); António Guterres; Gary Marcus; Yuval Noah Harari; Meredith Whittaker; Tristan Harris; Nick Bostrom.

---

## Part 2 — Output & File Plan
1) **Profiles table (CSV/JSON):** one row per person.  
2) **Annotated bibliography:** 5–15 most representative sources per person with 1–2 sentence relevance notes.  
3) **Comparative matrix:** risk framings, proposed policies, evidence invoked, domain focus, level of caution (1–5).  
4) **Timeline:** dated milestones and key statements (2018→present; highlight last 24 months).  
5) **Argument map:** core claims, supports, critiques, unresolved questions.  
6) **Policy heatmap:** proposed interventions (licensing, evals, audits, data/compute governance, model access, liability, labor policy, surveillance controls).  
7) **Limits & open questions.**

Provide all tables as CSV plus a concise written brief.

---

## Part 3 — Data Schemas (use verbatim)
**`person_profile.jsonl`**
```json
{
  "name": "",
  "role_affiliation": "",
  "domain": ["research","policy","industry","civil society","philosophy","economics"],
  "primary_concerns": ["misuse","loss_of_control","bias_fairness","labor_disruption","surveillance","disinformation","geo_security","environmental_costs"],
  "risk_time_horizon": ["near_term","mid_term","long_term"],
  "policy_stance": ["pause_moratorium","licensing","safety_evals","audit_transparency","compute_governance","open_access","closed_access","liability_reform","labor_policy","privacy_surveillance_reform","content_authenticity"],
  "representative_quotes": [
    {"quote": "", "date": "YYYY-MM-DD", "source_title": "", "url": "", "note": ""}
  ],
  "notable_actions": [{"type":"testimony|open_letter|book|paper|reg_comment|product_decision", "date":"", "title":"", "url": ""}],
  "influence_indicators": {
    "media_mentions_12m": null,
    "key_testimonies": [],
    "book_sales_or_citations": null,
    "social_followers": {"platform": "", "count": null},
    "wikipedia_pageviews_90d": null
  },
  "counterpositions": [{"critic":"", "claim_disputed":"", "evidence":"", "url": ""}],
  "disclosures": {"funding_affiliations": "", "potential_conflicts": ""},
  "last_updated": "YYYY-MM-DD",
  "confidence_0to1": 0.0
}
