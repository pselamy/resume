"""Only reviewed resume artifacts belong on the public site."""
from pathlib import Path
import re
import sys

site = Path(sys.argv[1])
pdfs = {f"resume-{p.stem}.pdf" for p in Path("variants").glob("*.tex")}
expected = pdfs | {"index.html", "style.css"}
actual = {p.name for p in site.iterdir()}
fails = []
if actual != expected:
    fails.append(f"unexpected files: {sorted(actual - expected)}; missing files: {sorted(expected - actual)}")
if any(not p.is_file() for p in site.iterdir()):
    fails.append("site contains a directory or non-file artifact")
links = set(re.findall(r'href="(resume-[^\"]+\.pdf)"', (site / "index.html").read_text()))
if links != pdfs:
    fails.append("index PDF links do not match the variant set")
if fails:
    print("PUBLIC SITE TEST FAILED:")
    for failure in fails:
        print(f"  - {failure}")
    sys.exit(1)
print(f"PASS: public site contains exactly {len(pdfs)} resume PDFs, index, and stylesheet.")
