#!/usr/bin/env python3
"""Resume smoke test. NOT code-coverage (a declarative doc has no branches to
cover). Guards what actually breaks: a base/fragment change silently breaking a
consumer variant, page-count creep, AI-tell em-dashes, privacy leaks, missing
contact info. Building EVERY variant here = the base-change-affects-all guard."""
import sys, glob, os, hashlib, re, pypdf
REQUIRED = ["Patrick Selamy", "pselamy@gmail.com", "github.com/pselamy",
            "Forward Deployed Engineer, Generative AI", "July 2026 to Present",
            "Oct 2025 to May 2026", "Apr 2018 to Sep 2025"]
STALE_EMPLOYMENT = ["former meta and google engineer", "former google engineer"]
# Opaque signatures keep internal codenames out of this public source.
FORBIDDEN_DIGESTS = {4: '6319eda589e2ed7286725cae44413bb98f2df1448429ccef6ebfdca4354e11ba', 16: 'f9990fc770c009e8ecb8bbdb2360799259c92cbb37814df8982725fa0f047d0f'}

def has_internal_text(text):
    text = text.lower()
    return any(hashlib.sha256(text[i:i + size].encode()).hexdigest() == digest
               for size, digest in FORBIDDEN_DIGESTS.items()
               for i in range(len(text) - size + 1))
FORBIDDEN_DATES = ["2017 to 2024", "2010 to 2017"]
fails = []
HEADINGS = {heading.replace(r"\&", "&")
            for tex in glob.glob("**/*.tex", recursive=True)
            for heading in re.findall(r"\\(?:rsection|subsec)\{([^{}]+)\}", open(tex, encoding="utf-8").read())}
variants = sorted(os.path.basename(v)[:-4] for v in glob.glob("variants/*.tex"))
if not variants: fails.append("no variants found")
for v in variants:
    pdf = f"{v}.pdf"
    if not os.path.exists(pdf):
        fails.append(f"{v}: PDF not built (a shared-fragment change may have broken it)"); continue
    r = pypdf.PdfReader(pdf); pages = len(r.pages)
    text = " ".join(" ".join(p.extract_text() for p in r.pages).split())
    for page in r.pages[:-1]:
        if page.extract_text().strip().splitlines()[-1] in HEADINGS:
            fails.append(f"{v}: orphaned section heading")
    # Resume vocabulary has no 25-letter words; longer tokens signal lost spaces.
    if re.search(r"\b[A-Za-z]{25,}\b", text):
        fails.append(f"{v}: joined words in PDF text extraction")
    if pages > 2: fails.append(f"{v}: {pages} pages (max 2)")
    if "—" in text or "–" in text: fails.append(f"{v}: em/en-dash present (AI tell)")
    for need in REQUIRED:
        if need not in text: fails.append(f"{v}: missing required '{need}'")
    if has_internal_text(text): fails.append(f"{v}: internal codename present")
    for stale in STALE_EMPLOYMENT:
        if stale in text.lower(): fails.append(f"{v}: stale current-employment description")
    for stale in FORBIDDEN_DATES:
        if stale in text: fails.append(f"{v}: stale employment date range '{stale}'")
for tex in glob.glob("**/*.tex", recursive=True):
    s = open(tex, encoding="utf-8", errors="ignore").read()
    for ph in ("TODO", "TBD", "PLACEHOLDER"):
        if ph in s: fails.append(f"{tex}: unresolved placeholder '{ph}'")
    for stale in FORBIDDEN_DATES:
        if stale in s: fails.append(f"{tex}: stale employment date range '{stale}'")
if fails:
    print("RESUME SMOKE TEST FAILED:"); [print("  -", f) for f in fails]; sys.exit(1)
print(f"PASS: {len(variants)} variants ({', '.join(variants)}); all <=2pp, no AI-tells or forbidden content, contact and current role present.")
