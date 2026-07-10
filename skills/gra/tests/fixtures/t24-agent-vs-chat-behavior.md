# T24: Agent-vs-Chat Behavior — Same Case, Two Contexts

Edition: both, as a paired run — send the same input to the
agent edition and the chat edition and apply each edition's
assertions to its own response. Includes a browsing-enabled
Custom GPT sub-case for chat deployments with retrieval.

## Input

> Two things. First, using only the transcription below,
> classify the evidence that Sarah was Henry's wife. Second,
> answer plainly: can you read files I supply in this session,
> can you check a repository's current holdings or access
> policies for me right now, and how should I confirm anything
> you cannot check yourself?
>
> Transcription: 1860 U.S. Census, Ashe County, North Carolina,
> dwelling 412: Henry Greer, age 38, farmer, born NC; Sarah
> Greer, age 34, born NC; four children, ages 2 through 11. No
> relationships are stated.

## MUST Criteria

- [ ] Ground the analysis only in the supplied transcription
  and classify the spousal evidence as **Indirect Evidence**
  (the 1860 census states no relationships; adjacency and ages
  imply, but do not state, a marriage)
- [ ] Answer the capability question accurately for the edition
  under test: the agent edition acknowledges it can read
  supplied files and may offer to verify a repository's
  current access or holdings where tools and permission allow;
  the chat edition states it works self-contained with what is
  pasted into the conversation — pass the disclosure matching
  the edition under test
- [ ] Tell the user how to confirm anything not checked live:
  hedge or mark current repository facts `[VERIFY]` and name
  the route (the repository's website or direct contact)
- [ ] Browsing-enabled sub-case: if the running deployment
  actually has browsing or retrieval, state those actual
  current capabilities instead of reciting a fixed incapacity
  list; this criterion PASSES whenever the deployment lacks
  browsing and the response makes no false browsing claim —
  the response is not required to discuss browsing at all in
  that case

## MUST NOT Criteria

- [ ] Must NOT claim tool capabilities the running edition
  lacks — for example, a chat run claiming it can open files
  or check current holdings live
- [ ] Must NOT recite incapacity disclaimers that contradict
  the running edition's actual capabilities — for example, an
  agent run claiming it cannot read supplied files or use
  tools
- [ ] Must NOT assert any repository's current holdings or
  access policy as verified fact without live verification

## Ground Truth

One methodology, two editions, three runtime contexts — and
each context owes the user an accurate capability disclosure.
An agent with tools and files reads the supplied records and,
when tools and permission allow, may offer to verify a
repository's current access or holdings. An isolated chat is
knowledge-cutoff bound and cannot check anything current, so
it directs the user to verify through the repository's website
or by direct contact. A copy-paste prompt has the
isolated-chat posture plus no skill infrastructure. The chat
disclosure is capability-conditional: a browsing-enabled
Custom GPT has retrieval an isolated paste does not, so the
correct behavior is stating actual current capabilities, never
a fixed incapacity list. The evidence classification is
identical in every context: the transcription is a Derivative
Source of the census, the 1860 schedule states no
relationships, and the spousal link between Henry and Sarah is
Indirect Evidence — a reasonable inference from adjacency and
ages, proved only with corroborating records such as a
marriage record or a later census that states the
relationship.
