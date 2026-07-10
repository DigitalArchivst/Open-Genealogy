# Photo Restoration & Enhancement

Prompts for **historical photograph restoration** that use bounded, evidence-supported changes and preserve the untouched source image as the master.

## Recommended

| Prompt | Purpose |
| --- | --- |
| **[restoration-v2.md](restoration-v2.md)** | Universal high-standard restoration. **Default.** |
| **[photo-conservator-v2.md](photo-conservator-v2.md)** | "Do-no-harm" conservation workflow with sidecar provenance. |
| **[photo-reconstructor-v3.md](photo-reconstructor-v3.md)** | For severely damaged photos. |
| **[damage-removal-v3.md](damage-removal-v3.md)** | Museum-grade intensive restoration. |

## Preservation and Provenance

All current prompts produce a clearly labeled derivative, not an altered replacement for the source. Keep an untouched master, make only changes supported by the visible image, and disclose inferred regions, residual damage, and uncertainty in a sidecar provenance record or restoration log. Do not use an in-image watermark unless a user explicitly requests it.

## Archive

The `archive/` folder contains legacy versions.
