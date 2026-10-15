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
- `sections/` — shared content: header, projects pool, experience, and skills.
- `sections/current-role.tex` — current employment, shared by every variant;
  prior roles remain in the historical experience sections.
- `variants/<name>.tex` — a variant built on the base with shared sections,
  a variant-specific summary, and target-specific emphasis.

## Add a variant

Copy `variants/writer.tex` to `variants/<company>.tex`, adjust the summary
and emphasis, and register the new path in the `root_file` list in
`.github/workflows/deploy.yml`. Verify locally before pushing to `main`;
CI then compiles it and publishes it automatically.

## Build

CI (`.github/workflows/deploy.yml`) compiles every `variants/*.tex` into a PDF,
generates the index, and deploys Pages. No local toolchain needed.

For local validation with TeX Live, latexmk, and Python with pypdf installed:

```sh
for v in variants/*.tex; do
  latexmk -pdf -file-line-error -halt-on-error -interaction=nonstopmode "$v" || exit 1
done
python3 web/test_resumes.py
```

The smoke test checks every variant for current employment, established date
guards, contact details, internal-content signatures, and a maximum of two
pages. It also rejects stranded section headings and joined words in extracted
PDF text. After site assembly, `python3 web/test_site.py site` permits only the
résumé PDFs, index, and stylesheet and verifies the index links.

## Guardrail

Keep variants **single-column + ATS-parseable**, especially for ATS-driven
targets like Greenhouse. Beautiful-but-fancy multi-column templates break ATS
extraction.

Owner: Reeve (career agent) maintains content; structure/CI is fixed.
