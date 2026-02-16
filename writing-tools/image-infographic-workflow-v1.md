# Workflow: Image and Infographic Creation v1

**Author:** Steve Little
**Created:** February 16, 2026
**Source:** Extracted from "Beyond Spell Check" presentation (GeneaBloggers, Feb 15, 2026)
**Supersedes:** InfographicGPT v6 (still available but no longer Steve's primary workflow)

---

## Overview

Steve's current approach to visual content creation uses a **two-tier workflow**: a quick path through Notebook LM for infographics, and an advanced three-step process through Claude Opus for custom image prompts. Both are described below.

---

## Tier 1: Quick Infographics via Notebook LM

**Best for:** Turning existing writing or research into shareable infographics with minimal effort.

**The Process:**

1. Open [Notebook LM](https://notebooklm.google.com/) (free from Google)
2. Add your sources — blog posts, articles, research notes, papers
3. Use Notebook LM's built-in infographic generation

**Why this works:** Notebook LM has made infographic creation "really, really easy" over the past several months. It reads your sources and produces well-designed infographics automatically.

**When to use:** When you want a good infographic quickly and don't need precise control over the visual output.

---

## Tier 2: Advanced Image Prompts via Claude Opus (Three-Step Process)

**Best for:** Custom images, precise visual storytelling, or when you want full control over what gets generated.

**The Three Steps:**

### Step 1: Learn

Tell Claude Opus 4.6:

> "Learn everything you can about writing an image prompt. Go to the [platform's] website and read about basic usage and best practices of writing an image prompt."

The AI will go read the official documentation on how to write an image prompt according to the platform that made the image generator. **Now it knows how to make the best image prompt.**

**Why this step matters — the self-awareness problem:** These models don't actually know what they can do. Their training data has a cutoff date, but their model cards, official documentation, and best-practice guides are published *after* that cutoff. So when you ask a model "what's the best way to write an image prompt?", it's drawing on outdated or incomplete self-knowledge. It will answer confidently — but often incorrectly.

The remedy: have the model use its internet access to read its own official documentation first. Step 1 doesn't just teach the AI about image prompts — it updates the AI on its own current capabilities.

### Step 2: Describe

Tell it what you want the image to be:

> "I want an image that [describes your vision]. Here is some of my writing for context: [paste relevant text]."

You can be as specific or as open-ended as you want. The AI now has best practices loaded and can combine them with your intent.

### Step 3: Generate

> "According to the best practices listed above on how to write an image prompt, take my writing and convert that to an image prompt in **markdown syntax in a code block**."

**Why "markdown syntax in a code block"?** These are what Steve calls "magic words":
- **Code block** makes the prompt easy to copy and paste into any image generation tool
- **Markdown syntax** is the writing format that language models understand best

### Complete Example Flow

```
USER: Learn everything you can about writing an image prompt. Go to the
      Google website and read about basic usage and best practices of
      writing an image prompt.

[AI reads official docs]

USER: I'm writing about my great-grandmother who immigrated from Norway
      in 1892. I want an image that captures the moment of arrival —
      the hope, the uncertainty, the new beginning. Here's my paragraph
      about her: [paste text]

[AI discusses the image concept with you]

USER: According to the best practices listed above, take my writing and
      convert that to an image prompt in markdown syntax in a code block.

[AI produces a properly formatted image prompt you can paste into any
 image generator]
```

---

## Choosing Between Tiers

| Factor | Tier 1 (Notebook LM) | Tier 2 (Claude Opus) |
|--------|----------------------|----------------------|
| **Speed** | Fast — minutes | Slower — multi-step conversation |
| **Control** | Limited — Notebook LM decides layout | Full — you guide every element |
| **Input** | Your existing sources | Your writing + verbal description |
| **Output** | Finished infographic | Image prompt (paste into generator) |
| **Cost** | Free | Claude Opus (paid) + image generator |
| **Best for** | Data visualization, research summaries | Custom illustrations, narrative images |

---

## Relationship to InfographicGPT v6

InfographicGPT v6 is a detailed technical prompt that generates interactive HTML/CSS/Chart.js infographics. It remains available at `writing-tools/infographic-v7.md` on GitHub and still works well for users who want that approach.

Steve's current practice has evolved toward the two-tier workflow described above:
- **Notebook LM** handles the quick infographic use cases that InfographicGPT was designed for
- **The three-step process** handles custom image creation with more control and better results

Both approaches are valid. Choose based on your comfort level and what you need.

---

## Key Principles

1. **Always have the model read official docs first** — this applies to image prompts and far beyond (see "Teach the Model About Itself" in the handout)
2. **Notebook LM is the easy button** — don't overcomplicate what can be simple
3. **The prompt is portable** — a well-crafted image prompt in a code block can go into any image generator (DALL-E, Midjourney, Gemini, etc.)
4. **Your writing is the input** — you don't need design skills; you need writing that describes what you want to see

---

## Context

This workflow was extracted from the "Beyond Spell Check" presentation transcript. Steve described it during the live session as his current process, noting: "I'll share with you my process for making infographics. You can do it the easy way in Notebook LM, and Notebook LM makes really, really good infographics. But if you want to take it to the next level, I'll share with you my process for doing that."

The presentation also covered:
- How Notebook LM infographics have become standard over the past 3-4 months
- Google AI Studio as an alternative interface to access Gemini Pro
- The "self-awareness problem" — why Step 1 (reading docs) matters for all model interactions

---

*v1 — February 16, 2026*
*Extracted from GeneaBloggers/DearMYRTLE presentation transcript*
