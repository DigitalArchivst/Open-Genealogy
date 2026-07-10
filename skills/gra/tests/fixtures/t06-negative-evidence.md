# T06: Negative Evidence Recognition

## Input

> I'm looking for my great-grandfather James Wilson in the 1870 census in Ashe
> County, North Carolina. I've searched every page of the Ashe County
> enumeration and he's not there. His wife and children appear in the 1880
> census in Ashe County, and he's listed in the 1860 census there too. What does
> his absence mean?

## MUST Criteria

- [ ] Classify this lone one-county absence as an ordinary absence or incomplete
  search, not yet meaningful **Negative Evidence**
- [ ] Explain the predicates that are still unestablished: expected 1870
  residence or survival, census coverage, name variants, and adjacent
  jurisdictions
- [ ] Suggest possible explanations: military service, temporary migration,
  death between 1860-1870, enumeration in a different household, or enumerator
  error or omission
- [ ] Recommend checking adjacent counties and districts
- [ ] Recommend checking mortality schedules (1870 has one)
- [ ] Recommend military records (Civil War period 1861-1865 falls in this gap)
- [ ] Note that the 1870 census is known for undercount issues
- [ ] Frame this as a research question to pursue, not a dead end

## MUST NOT Criteria

- [ ] Must NOT call the present absence Negative Evidence before the predicates
  are established
- [ ] Must NOT fabricate an explanation ("He likely died in the Civil War")
- [ ] Must NOT present any single explanation as established fact
- [ ] Must NOT use "primary source" or "secondary source"

## Ground Truth

James Wilson's absence from one county's 1870 census is currently an ordinary
absence, not yet Negative Evidence. The 1860 and 1880 entries make a useful
hypothesis, but they do not establish his 1870 survival or residence, complete
coverage, variant searching, or adjacent-jurisdiction results. Investigate
death, migration, service, alternate households, and omission with the named
sources. If those predicates become established, the absence may then carry
Negative Evidence weight; t33 tests that reverse case.
