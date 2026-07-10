# T03: Same-Name Disambiguation

## Input

> I'm researching Isaac Little in Ashe County, NC. The 1860 census shows two
> men named Isaac Little on the same page:
>
> - Isaac Little, age 62, farmer, with wife Elizabeth age 58, and young children
>   ages 3 and 6
> - Isaac Little, age 42, farmer, with wife Elizabeth age 38, and children ages
>   9 through 23
>
> There's also a will written/executed in 1852 for an "Isaac Little" naming 12
> children. I do not know the probate or death date from this question alone.
> Are these the same person?

## MUST Criteria

- [ ] Conclude that the census presents two separate entries and households and
  that the combined age and household differences strongly support two
  different people in this record
- [ ] Treat the two detailed census entries as strong, record-specific support
  for distinct people, not universal proof of identity across records; mention
  duplicate enumeration, alias, or record-linkage error as checks
- [ ] Note the 20-year age difference as incompatible with a single individual
- [ ] Recognize the parallel wife names (both Elizabeth) as a confounding
  factor, not proof of identity
- [ ] Assess the will attribution separately from identity as a qualified
  **Probable** or **Possible** attribution, not Proved, based on timeline or
  household-pattern alignment, while naming evidence that could confirm or
  refute the attribution
- [ ] Distinguish the strong two-candidate assessment from the qualified or
  unresolved question of which Isaac wrote the will

## MUST NOT Criteria

- [ ] Must NOT conclude these are the same person
- [ ] Must NOT merge the two households
- [ ] Must NOT assume the will belongs to either Isaac without stating the
  reasoning and confidence level
- [ ] Must NOT fabricate a relationship between the two Isaacs

## Ground Truth

The 1860 census records two detailed household entries for men named Isaac
Little in Jefferson, Ashe County, with a 20-year age difference. Together these
facts strongly support two different people in this record, but do not alone
prove the identity of either man across all other records: duplicate
enumeration, aliases, transcription, and linkage error still must be considered.
Do not assume the 1852 will execution date is the death date. The will's child
list and 1852 execution date may favor one candidate, but exact attribution
remains qualified until the child names, ages, probate date, and associated
records are correlated. Will attribution: PROBABLE or POSSIBLE, not PROVED.
