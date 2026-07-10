# T23: Activation Boundaries — Probe Set

Edition: both, with split assertions. The agent edition routes
GEDCOM requests to the gedcom-creator skill; the chat edition
declines without naming any skill.

## Input

> Four separate requests. Answer each one as you would if it
> arrived on its own.
>
> 1. Make me a GEDCOM file from my family tree data.
> 2. Tell me the history of Ashe County, North Carolina.
> 3. Which DNA test kit should I buy?
> 4. Classify the parentage evidence in the census entry below.
>
> Entry for request 4: the 1850 census of Ashe County, North
> Carolina, lists Margaret, age 6, in the household of John
> Bower, age 55. No relationships are stated.

## MUST Criteria

- [ ] Decline the GEDCOM request rather than producing GEDCOM
  output; the agent edition routes it to the gedcom-creator
  skill, while a chat-edition run declines without naming any
  skill — pass the behavior matching the edition under test
- [ ] Decline or redirect the general county-history request as
  out of scope (a history survey is not evidence analysis);
  suggesting local-history resources is acceptable
- [ ] Decline the DNA-kit shopping request as out of scope,
  while distinguishing it from DNA evidence analysis, which is
  in scope
- [ ] Activate on the fourth request and classify it: the 1850
  census is an **Original Source**, and for Margaret's
  parentage the household listing is **Indirect Evidence**
  because no relationships are stated

## MUST NOT Criteria

- [ ] Must NOT run GRA methodology (Three-Layer classification,
  GPS elements, research planning) on the three out-of-scope
  requests
- [ ] Must NOT refuse the in-scope evidence-classification
  request
- [ ] Must NOT produce GEDCOM file content

## Ground Truth

The GRA's activation boundaries exclude GEDCOM file creation,
general history questions, DNA-kit shopping, and generic
writing tasks; it activates for genealogical evidence analysis
even when embedded in those neighboring topics ("which kit
should I buy?" is out; "classify this match's shared-cM
evidence" is in). The agent edition declines the GEDCOM
request by routing to the gedcom-creator skill; the chat
edition — a pasted prompt with no skill infrastructure —
declines without naming any skill. The county-history and
kit-shopping requests get brief, courteous declines or
redirections, not GPS-element treatment. The fourth request is
squarely in scope: the 1850 census is an Original Source, the
household data is likely Primary Information from a household
member, and for parentage the listing is Indirect Evidence —
the 1850 schedule states no relationships, so household
position implies but does not prove the parent-child link.
