# Licensing and Rights

CC BY-NC-SA applies only to Steve-authored content within its stated scope. It does not license third-party or historical images, captured model outputs, quotations, or other material that Steve does not have authority to license.

The root [`LICENSE`](LICENSE) contains the complete Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International legal code. The SPDX identifier is `CC-BY-NC-SA-4.0`, and the canonical license URL is <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

For a shorter navigation guide, see the [Rights and License Matrix](docs/RIGHTS-AND-LICENSE-MATRIX.md). It identifies common paths that need a separate rights check; the full path matrix below remains the controlling repository guidance.

## How Scope Works

- Unless a row below says otherwise, `CC-BY-NC-SA-4.0` applies to the copyrightable portions of the current repository authored by Steve Little.
- A local license declaration applies to the material it identifies. This matrix does not revoke an earlier grant or add terms that the original declaration did not contain.
- Third-party and historical material is excluded from Steve's license even when it is embedded in a licensed document. Follow the source-specific rights note or obtain permission from the rights holder.
- Git tags, release assets, and historical revisions retain the terms and notices distributed with those artifacts. This current-tree policy does not relicense them retroactively.
- Public availability is not a license. Where the status below is unresolved, no additional reuse permission is granted by this repository.

## Path Matrix

| Path or material | Status | Exact identifier and URL | Reuse scope |
| --- | --- | --- | --- |
| Steve-authored portions of `**/*`, except as listed below | Repository baseline | `CC-BY-NC-SA-4.0`; <https://creativecommons.org/licenses/by-nc-sa/4.0/> | Attribution required; noncommercial use only; adaptations must use compatible ShareAlike terms. Third-party material is excluded. |
| Current GRA materials under `skills/gra/**`, except the two restored legacy paths below | Same as baseline | `CC-BY-NC-SA-4.0`; local full terms at `skills/gra/LICENSE` | Applies only to Steve-authored portions. |
| `gpt-configs/open-geneagpt-v0.4.txt`; `gpt-configs/website-frontend-v3.txt` | Preserved local exception | `CC-BY-4.0`; <https://creativecommons.org/licenses/by/4.0/> | The files say "Creative Commons 4.0 Attribution License." That declaration supplies version and license elements clearly enough to map to the SPDX identifier without changing the files. |
| `photo-restoration/archive/photo-conservator-v1.md`; `photo-restoration/photo-conservator-v2.md`; `transcription/archive/transcription-v02.txt`; `transcription/archive/transcription-v03.txt`; `transcription/archive/transcription-v04.txt` | Preserved local exception | `CC-BY-NC-4.0`; <https://creativecommons.org/licenses/by-nc/4.0/> | These files expressly identify CC BY-NC 4.0. ShareAlike is not added by this matrix. |
| `image-analysis/deep-look-v2.md` | Unresolved local shorthand | Exact declaration: `Creative Commons BY-NC`; SPDX identifier: unresolved; canonical URL: unresolved because no version is stated | Do not assume version 4.0 or add ShareAlike. See `image-analysis/RIGHTS.md`. |
| `image-analysis/Deep-Look-v2-Four-Models-Full-Results.pdf` | Mixed artifact | Steve-authored editorial portions: repository baseline where no narrower local statement applies; embedded prompt: unresolved `Creative Commons BY-NC`; Bower photograph and captured model outputs: excluded | The photograph has no documented photographer, owner, or permission record in the repository. No reuse license is granted for it. See `image-analysis/RIGHTS.md`. |
| `skills/gra/companion-reference.md`; `skills/gra/research-assistant-v8.5-full.md` | Frozen restored legacy artifacts | Exact declaration: `CC4-BY-NC`; SPDX identifier: unresolved; canonical URL: unresolved because the shorthand is malformed | Preserved to maintain historical URLs and bytes. Do not reinterpret the shorthand as a current license grant. |
| `writing-tools/narrative-assistant-v3.md` | Unresolved informal permission | Exact declaration: `Free to use and share`; SPDX identifier: none; canonical URL: none | The statement does not define attribution, commercial use, adaptation, or version terms. Do not treat it as a Creative Commons license. |
| `skills/gedcom-creator/scripts/gedcom_builder.py` | Narrow code exception | `MIT`; complete terms at `skills/gedcom-creator/LICENSE`; <https://spdx.org/licenses/MIT.html> | MIT applies only to the builder script, based on the owner-authored declaration and restored full terms. |
| Other content under `skills/gedcom-creator/**` | Same as repository baseline | `CC-BY-NC-SA-4.0`; root `LICENSE` | The skill prose, README, tests, and examples are expressly outside the narrow MIT grant and remain under the authored-content baseline where Steve owns them. |
| `genealogy-ai-starter-workspace/records/record-*.jpg` | U.S. federal record images; excluded from repository CC license | No Creative Commons license is applied by this repository | Reuse status and item-level provenance are documented in `genealogy-ai-starter-workspace/records/RIGHTS.md`. |
| `media/steve-on-5-part-prompt.mp3` | Rights holder and recording provenance unresolved; excluded from repository CC license | SPDX identifier: none; canonical URL: none | Repository access does not grant reuse permission. See `media/RIGHTS.md`. |
| Captured model outputs in `benchmark/case-studies/ashe-county-nc/*.md` and the Deep Look PDF | Third-party or authorship-uncertain material; excluded | No license granted by this repository | Steve-authored framing remains within the baseline where separable. The captured outputs are not relicensed. |
| Other third-party quotations, images, logos, trademarks, and source excerpts anywhere in the repository | Excluded | Follow the notice supplied with the material or the source's terms | No repository-wide license is asserted over material Steve does not own. |

## Attribution for Baseline Content

When reusing baseline content, identify Steve Little as creator, identify the source path or title, link to this repository when practical, link to `CC-BY-NC-SA-4.0`, and indicate changes. Do not imply endorsement.

## Machine-Readable Companion

[`LICENSE-MATRIX.json`](LICENSE-MATRIX.json) repeats this policy in structured form using exact SPDX identifiers where the evidence supports them. Unresolved and excluded material deliberately has a `null` SPDX expression instead of a guessed license.

As reviewed on 2026-07-10, GitHub Licensee compares the root license file against a short list of recognized licenses. GitHub's specific Creative Commons keywords include `CC-BY-4.0` and `CC-BY-SA-4.0`, but not `CC-BY-NC-SA-4.0`; a family-level result or `NOASSERTION` must not be "fixed" by substituting a broader license. See [GitHub's license-detection documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository#detecting-a-license).
