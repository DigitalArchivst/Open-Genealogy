<!-- markdownlint-disable MD013 -->

# Immigration Identity Profile

This file shows the first deliverable in an immigration research problem: a profile built from destination-country evidence before searching arrival or origin records.

Immigration research is a record-cluster problem. The profile tells you which clusters to search, which variants to try, and what not to assume.

## Profile Template

| Field | Confirmed from sources | Possible clue | Inference or hypothesis | Open question |
| --- | --- | --- | --- | --- |
| Full name and variants | | | | |
| Approximate birth year | | | | |
| Country, region, parish, county, town, or locality clues | | | | |
| Approximate arrival window | | | | |
| Ports, crossings, or routes to consider | | | | |
| Residence after arrival | | | | |
| Family, associates, neighbors, sponsors, witnesses, or traveling companions | | | | |
| Religion, language, occupation, or community | | | | |
| Naturalization, citizenship, alien-registration, or border events | | | | |
| Newspapers, churches, cemeteries, directories, or local organizations | | | | |
| Origin-country record targets | | | | |

## Working Rules

1. Start after arrival. Use what is known in the destination country before searching ships or origin records.
2. Extract every place clue, then label it as confirmed, possible, ambiguous, or inferred.
3. Treat name variants, place variants, transliterations, anglicizations, and nicknames as search hypotheses.
4. Use family, associates, neighbors, witnesses, sponsors, destination contacts, and traveling companions to test identity and origin.
5. Move to origin-country records only when the locality is specific enough to search responsibly.
6. Log every search, including searches that find nothing.

## Immigration Record Clusters

| Cluster | Why It Matters | What Can Go Wrong |
| --- | --- | --- |
| Passenger lists and manifests | arrival date, ship, port, last residence, contact person, destination | index errors, second-page dependencies, repeated trips, port assumptions |
| Border crossings | Canada/U.S. or other overland movement, repeated travel, route clues | crossing does not always equal immigration |
| Naturalization and citizenship | legal status, court, witnesses, ship/date/port, prior names | laws and forms vary by time and jurisdiction |
| Alien-registration and immigration files | twentieth-century legal-status evidence, photos, addresses, relatives, ship/date clues | access rules, privacy, and identifiers vary |
| Census and local records | arrival year, status, language, household, community | reported information may be wrong or inconsistent |
| Church, cemetery, newspaper, and community records | origin clues, language, religion, chain migration | often indirect; needs correlation |
| Origin-country records | birth, baptism, marriage, residence, departure, civil status | requires specific locality and historical jurisdiction |

## Prompt

```text
Using only the files in this folder, build an immigration identity profile from destination-country evidence. Separate confirmed facts, possible clues, inferences, conflicts, and open questions. Create a variant grid for names and places. Recommend the next searches, but do not identify an origin place unless the evidence supports it.
```
