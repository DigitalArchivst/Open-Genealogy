# Hebrew Headstones

Specialized prompt for analyzing **Jewish cemetery headstones** — Hebrew and Yiddish inscriptions, gematria date conversion, patronymic identification, symbol interpretation, and cultural context.

## When to Use

Use this prompt when you have a photograph of a Jewish headstone and want to extract genealogical information: names, dates, observed Kohen- or Levi-associated designations and traditions, and family relationships. Symbols and titles are clues requiring corroboration, not proof of lineage.

## Recommended

| File | Description |
| --- | --- |
| [hebrew-headstone-helper-v9.md](hebrew-headstone-helper-v9.md) | 10-phase forensic analysis with confidence scoring |

## How It Works

The prompt guides AI through ten sequential phases:

1. **Forensic Triage** — image quality, legibility, script identification
2. **Transcription** — three formats: Hebrew, transliteration, English
3. **Identification Anchor** — patronymic string and observed designations or traditions
4. **Translation & Linguistics** — honorifics, abbreviations, register analysis
5. **Date Reconciliation** — gematria calculation, converter-backed Hebrew-to-Gregorian date, calendar and sunset conventions
6. **Physical Description** — material, carving, condition, lettering style
7. **Symbols** — observed clues, name symbols, regional variations, and alternatives
8. **Historical Context** — cemetery, burial customs, community roles
9. **Archival Summary** — structured table for genealogical records
10. **Confidence Assessment** — friction points, alternative interpretations, recommendations

## Tips

- **Image quality matters.** Close-ups of name and date lines are more useful than a single wide shot.
- **Provide context if you have it.** Known family names, cemetery location, and approximate era help AI distinguish similar Hebrew letters on weathered stones.
- **Check the gematria and use an exact converter.** Verify each complete Hebrew date with a tested converter or library, such as [Hebcal's Jewish Calendar Date Converter](https://www.hebcal.com/converter), then confirm it independently. A Hebrew month can cross a Gregorian year: 1 Tevet 5681 = 12 Dec 1920, while 26 Tevet 5681 = 6 Jan 1921.
- **State the calendar and sunset conventions.** Hebrew days begin at sunset. Record the civil-date mapping and any known event-time or local convention; a one-day difference may be a clue to investigate, not an automatic adjustment.

## Related

- [transcription/jewish-transcription-v2.md](../transcription/jewish-transcription-v2.md) — For Jewish documents (ketubot, vital records, yizkor books) rather than headstones
- [transcription/ocr-htr-v08.md](../transcription/ocr-htr-v08.md) — General-purpose handwritten document transcription

## Version History

| Version | Source | Notes |
| --- | --- | --- |
| v9.0 Opus | Synthesized from v6.0 + v7.0 + v8.1 | Current recommended version |
| v6.0–v8.1 | Arthur Sissman / Steve Little | Earlier versions available via the [Hebrew Headstone Helper Facebook group](https://www.facebook.com/groups/hebrewheadstonehelper) |
