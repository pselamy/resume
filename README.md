# Resume (resume-as-code)

Single source, **base + per-company variants**, compiled to PDF in CI and published to
**https://resume.selamy.dev** (GitHub Pages) — a list of variants, each downloadable.

## Structure
- `preamble.tex` — shared formatting (single-column, **ATS-safe**: standard fonts, real text, no multicol).
- `sections/` — shared content (header, projects pool, experience, skills, education).
- `variants/<name>.tex` — a variant *built on the base*: `\input{preamble}` + shared sections, with a variant-specific summary + emphasis/order. One file per target.

## Add a variant
Copy `variants/writer.tex` to `variants/<company>.tex`, adjust the summary + emphasis. Push — CI compiles it and it appears on the site automatically.

## Build
CI (`.github/workflows/deploy.yml`) compiles every `variants/*.tex` → `resume-<name>.pdf`, generates the index, and deploys Pages. No local toolchain needed.

## Guardrail
Keep variants **single-column + ATS-parseable** (esp. for ATS-driven targets like Greenhouse). Beautiful-but-fancy multi-column templates break ATS extraction.

Owner: Reeve (career agent) maintains content; structure/CI is fixed.
