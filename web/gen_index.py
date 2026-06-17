import sys, os
site = sys.argv[1]
pdfs = sorted(f for f in os.listdir(site) if f.startswith("resume-") and f.endswith(".pdf"))
def label(f): return f[len("resume-"):-4].replace("-", " ").title()
items = "\n".join(
    f'    <li><span class="v">{label(f)}</span>'
    f'<a class="btn" href="{f}" download>Download PDF</a>'
    f'<a class="btn ghost" href="{f}">View</a></li>' for f in pdfs
) or "    <li>No resume variants built yet.</li>"
print(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Patrick Selamy — Resumes</title><link rel="stylesheet" href="style.css"></head>
<body><main>
  <h1>Patrick Selamy</h1>
  <p class="sub">Resume variants, tailored from one source. Choose the cut for the role.</p>
  <ul class="variants">
{items}
  </ul>
  <p class="foot">Each variant is built from <code>variants/*.tex</code> in CI and published here automatically.</p>
</main></body></html>""")
