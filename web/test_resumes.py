#!/usr/bin/env python3
"""Resume smoke test. NOT code-coverage (a declarative doc has no branches to
cover). Guards what actually breaks: a base/fragment change silently breaking a
consumer variant, page-count creep, AI-tell em-dashes, privacy leaks, missing
contact info. Building EVERY variant here = the base-change-affects-all guard."""
import sys, glob, os, pypdf
REQUIRED = ["Patrick Selamy", "pselamy@gmail.com", "github.com/pselamy"]
FORBIDDEN = ["J3PS", "Java Play Prober"]  # internal codename — must never ship
fails = []
variants = sorted(os.path.basename(v)[:-4] for v in glob.glob("variants/*.tex"))
if not variants: fails.append("no variants found")
for v in variants:
    pdf = f"{v}.pdf"
    if not os.path.exists(pdf):
        fails.append(f"{v}: PDF not built (a shared-fragment change may have broken it)"); continue
    r = pypdf.PdfReader(pdf); pages = len(r.pages)
    text = "".join(p.extract_text() for p in r.pages)
    if pages > 2: fails.append(f"{v}: {pages} pages (max 2)")
    if "—" in text or "–" in text: fails.append(f"{v}: em/en-dash present (AI tell)")
    for need in REQUIRED:
        if need not in text: fails.append(f"{v}: missing required '{need}'")
    for bad in FORBIDDEN:
        if bad.lower() in text.lower(): fails.append(f"{v}: forbidden/internal text '{bad}'")
for tex in glob.glob("**/*.tex", recursive=True):
    s = open(tex, encoding="utf-8", errors="ignore").read()
    for ph in ("TODO", "TBD", "PLACEHOLDER"):
        if ph in s: fails.append(f"{tex}: unresolved placeholder '{ph}'")
if fails:
    print("RESUME SMOKE TEST FAILED:"); [print("  -", f) for f in fails]; sys.exit(1)
print(f"PASS: {len(variants)} variants ({', '.join(variants)}); all <=2pp, no AI-tells, no leaks, contact present.")
