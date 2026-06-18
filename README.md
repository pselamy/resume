# Resume (resume-as-code)

Single source, **base + per-company variants**, compiled to PDF in CI and
published at [selamy.dev/resume](https://selamy.dev/resume/) — a list of
variants, each downloadable.

Public hub links: [selamy.dev](https://selamy.dev) ·
[GitHub profile](https://github.com/pselamy) ·
[LinkedIn](https://www.linkedin.com/in/patrickselamy) ·
[public agent-skills](https://github.com/selamy-labs/agent-skills)

## Structure

- `preamble.tex` — shared formatting: single-column, **ATS-safe**, standard
  fonts, real text, no multicol.
- `sections/` — shared content: header, projects pool, experience, skills,
  education.
- `variants/<name>.tex` — a variant built on the base with shared sections,
  a variant-specific summary, and target-specific emphasis.

## Add a variant

Copy `variants/writer.tex` to `variants/<company>.tex`, adjust the summary
and emphasis, then push. CI compiles it and publishes it automatically.

## Build

CI (`.github/workflows/deploy.yml`) compiles every `variants/*.tex` into a PDF,
generates the index, and deploys Pages. No local toolchain needed.

## Guardrail

Keep variants **single-column + ATS-parseable**, especially for ATS-driven
targets like Greenhouse. Beautiful-but-fancy multi-column templates break ATS
extraction.

Owner: Reeve (career agent) maintains content; structure/CI is fixed.
