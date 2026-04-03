# Example: Conflict Resolution

Demonstrates GPS Element 4 — resolving conflicting evidence.

## User Input

> My great-grandmother's birth year shows up differently in
> every record:
>
> - 1870 Census: age 2 (born ~1868)
> - 1880 Census: age 14 (born ~1866)
> - 1900 Census: born May 1869
> - Death certificate (1945): born 1867
> - Family Bible: born May 12, 1868
>
> Which one is right?

## Expected Behavior

The assistant should NOT simply pick one. It should:

**1. Classify each source and information type:**

| Source | Source Type | Info Type | Informant |
| ------ | ---------- | --------- | --------- |
| 1870 Census | Original | Indeterminate | Head of household |
| 1880 Census | Original | Indeterminate | Head of household |
| 1900 Census | Original | Indeterminate | Head of household |
| Death cert | Original | Secondary | Named informant |
| Family Bible | Depends on entry date | Possibly Primary | Unknown |

**2. Assess independence:**

The census records share a common problem: ages were often
rounded or estimated by the enumerator. But they represent three
independent enumeration events with (likely) different
enumerators. The death certificate informant was reporting
decades after the event. The Family Bible's reliability depends
on when the entry was made — contemporaneous entries are primary
information; later entries are secondary.

**3. Apply preponderance hierarchy:**

The assistant should note that the Family Bible entry, *if made
near the time of birth*, would be the strongest evidence (primary
information in a potentially original source). The 1900 census
is notable for being the only federal census that asked birth
month and year rather than just age.

**4. State a conclusion with confidence level:**

"Evidence suggests (**Probable**) a birth date of approximately
May 1868, supported by the Family Bible and consistent with the
1870 census. The 1880 census and death certificate diverge by
1-2 years, which is common for age reporting in this era. To
strengthen this to **Proved**, locate a birth or baptismal record
in [appropriate jurisdiction]."

**Key teaching point:** The assistant resolves conflicts using
evidence quality, not majority vote. Five sources disagreeing
is normal — the question is which informant was closest to the
event.
