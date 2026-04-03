# Example: Source Classification

Demonstrates the Three-Layer Evidence Model applied to a common
genealogical document.

## User Input

> I found my grandfather's death certificate from 1952 in North
> Carolina. It lists his birth date, parents' names, and cause of
> death. How should I classify this?

## Expected Behavior

The assistant should classify through all three layers:

**Source classification:** This is an **original source** — it was
created at or near the time of death by an official authority.

**Information classification (varies by fact):**

| Fact | Info Type | Why |
| ---- | --------- | --- |
| Date of death | **Primary** | Physician/funeral director: direct knowledge |
| Cause of death | **Primary** | Medical professional's direct observation |
| Birth date | **Secondary** | Informant was reporting, not witnessing |
| Parents' names | **Secondary** | Informant reported what they were told |

**Evidence classification:** Depends on the research question.
If the question is "When did grandfather die?" the death date is
**direct evidence**. If the question is "When was grandfather
born?" the birth date on the death certificate is **indirect
evidence** — it answers the question, but the informant was not
a witness to the birth.

**Key teaching point:** A single document is not uniformly
reliable. The death certificate is an excellent source for facts
about the death, but a weaker source for facts about the birth.
The assistant should never say "this is a primary source" —
the source is original; the *information* varies between primary
and secondary depending on which fact you examine.
