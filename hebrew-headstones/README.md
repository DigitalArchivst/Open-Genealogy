# Hebrew Headstones

Specialized prompt for analyzing **Jewish cemetery headstones** — Hebrew and Yiddish inscriptions, gematria date conversion, patronymic identification, symbol interpretation, and cultural context.

## When to Use

Use this prompt when you have a photograph of a Jewish headstone and want to extract genealogical information: names, dates, lineage (Kohen/Levi/Israelite), and family relationships.

## Recommended

| File | Description |
|------|-------------|
| [hebrew-headstone-helper-v9.md](hebrew-headstone-helper-v9.md) | 10-phase forensic analysis with confidence scoring |

## How It Works

The prompt guides AI through ten sequential phases:

1. **Forensic Triage** — image quality, legibility, script identification
2. **Transcription** — three formats: Hebrew, transliteration, English
3. **Identification Anchor** — patronymic string and lineage/caste
4. **Translation & Linguistics** — honorifics, abbreviations, register analysis
5. **Date Reconciliation** — gematria calculation, Hebrew-to-Gregorian conversion, Sunset Rule
6. **Physical Description** — material, carving, condition, lettering style
7. **Symbols** — lineage markers, name symbols, regional variations
8. **Historical Context** — cemetery, burial customs, community roles
9. **Archival Summary** — structured table for genealogical records
10. **Confidence Assessment** — friction points, alternative interpretations, recommendations

## Tips

- **Image quality matters.** Close-ups of name and date lines are more useful than a single wide shot.
- **Provide context if you have it.** Known family names, cemetery location, and approximate era help AI distinguish similar Hebrew letters on weathered stones.
- **Check the gematria.** AI can make arithmetic errors. The prompt requires showing work — verify it.
- **Use the Sunset Rule.** Hebrew days begin at sunset, so a one-day discrepancy between Hebrew and secular dates is normal, not an error.

## Related

- [transcription/jewish-transcription-v2.md](../transcription/jewish-transcription-v2.md) — For Jewish documents (ketubot, vital records, yizkor books) rather than headstones
- [transcription/ocr-htr-v08.md](../transcription/ocr-htr-v08.md) — General-purpose handwritten document transcription

## Version History

| Version | Source | Notes |
|---------|--------|-------|
| v9.0 Opus | Synthesized from v6.0 + v7.0 + v8.1 | Current recommended version |
| v6.0–v8.1 | Arthur Sissman / Steve Little | Earlier versions available via the [Hebrew Headstone Helper Facebook group](https://www.facebook.com/groups/hebrewheadstonehelper) |
