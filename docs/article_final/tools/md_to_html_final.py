"""Final article: Markdown -> HTML with a cover page, a navigable table of contents and print page breaks.

Reuses the minimal converter of the first edition (docs/article/tools/md_to_html.py, imported, not modified) and adds:
  - a sober cover (title, subtitle, author, version, BeamNG.drive, date), no logos;
  - a table of contents built from the '# Parte' and '## n.' headings, with anchors;
  - print CSS: A4, page break before each part, figures and tables kept whole, images limited in height.
The PDF is printed from this HTML by Microsoft Edge (headless), the method of the first edition.

    python docs/article_final/tools/md_to_html_final.py
    "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" --headless --disable-gpu --no-pdf-header-footer
        --print-to-pdf=docs/article_final/ARTIGO_TECNICO_FINAL_PTBR.pdf docs/article_final/ARTIGO_TECNICO_FINAL_PTBR.html
"""
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.abspath(os.path.join(HERE, ".."))
sys.dont_write_bytecode = True  # never write __pycache__ into docs/article/ (the first edition stays untouched)
sys.path.insert(0, os.path.abspath(os.path.join(ART, "..", "article", "tools")))
import md_to_html as base  # noqa: E402  (first-edition converter, unchanged)

EXTRA_CSS = """
.cover{min-height:90vh;display:flex;flex-direction:column;justify-content:center;padding:40px 8px}
.cover .kicker{color:var(--muted);text-transform:uppercase;letter-spacing:.08em;font-size:.85rem;margin-bottom:18px}
.cover h1{font-size:2.2rem;margin:0 0 .3em;border:0}
.cover .sub{font-size:1.25rem;color:var(--muted);margin:0 0 1.6em}
.cover .tag{font-style:italic;color:var(--muted);margin:0 0 2.4em}
.cover dl{display:grid;grid-template-columns:max-content 1fr;gap:6px 18px;margin:0;font-size:1rem}
.cover dt{color:var(--muted)}
.cover dd{margin:0;font-weight:600;overflow-wrap:anywhere}
.cover dd code{font-size:.74rem}
.cover .note{margin-top:3em;font-size:.85rem;color:var(--muted);max-width:640px}
nav.toc{margin:1em 0 2em;padding:1em 1.4em;border:1px solid var(--line);border-radius:8px;background:var(--soft)}
nav.toc h2{margin:.2em 0 .6em;border:0;padding:0;font-size:1.3rem}
nav.toc ol{list-style:none;margin:0;padding:0}
nav.toc li{margin:.15em 0}
nav.toc li.part{margin-top:.7em;font-weight:700}
nav.toc li.sec{padding-left:1.2em}
nav.toc a{text-decoration:none;color:var(--fg)}
nav.toc a:hover{color:var(--accent)}
h1.part{font-size:1.6rem;margin:2.4em 0 .4em;padding-top:.5em;border-top:3px solid var(--accent)}
figure img{max-height:78vh;object-fit:contain}
@page{size:A4;margin:16mm 14mm 16mm 14mm}
@media print{
  .cover{min-height:0;height:255mm;break-after:page}
  nav.toc{break-after:page;background:none}
  h1.part{break-before:page;border-top:0;margin-top:0}
  figure img{max-height:205mm}
  h2,h3{break-after:avoid}
  tr{break-inside:avoid}
  pre{white-space:pre-wrap;overflow:visible;font-size:8pt}
  pre code{overflow-wrap:anywhere}
  .table-wrap{break-inside:auto}
}
"""


def cover(md):
    title = re.search(r"^#\s+(.*)$", md, re.M).group(1).strip()
    sub = re.search(r"^##\s+(.*)$", md, re.M).group(1).strip()
    tag = re.search(r"^>\s+(.*)$", md, re.M).group(1).strip()
    rows = dict(re.findall(r"^\|\s*\*\*([^*]+)\*\*\s*\|\s*(.*?)\s*\|\s*$", md, re.M))
    keep = ["Autor", "Versão documentada", "Tag", "BeamNG.drive", "Data", "Pacote", "SHA-256"]
    dl = "".join(f"<dt>{html.escape(k)}</dt><dd>{base.inline(rows[k])}</dd>" for k in keep if k in rows)
    return (f'<section class="cover"><div class="kicker">Artigo técnico final · v1.0</div>'
            f"<h1>{html.escape(title)}</h1><p class='sub'>{html.escape(sub)}</p><p class='tag'>{html.escape(tag)}</p>"
            f"<dl>{dl}</dl><p class='note'>Projeto independente. BeamNG.drive é um produto da BeamNG GmbH; "
            "as normas da SENATRAN/CONTRAN foram usadas como referência. Nenhum deles endossa este trabalho.</p></section>")


def toc(md):
    items = []
    for m in re.finditer(r"^(#|##)\s+(.*)$", md, re.M):
        level, text = m.group(1), m.group(2).strip()
        if level == "#" and text.startswith("Parte"):
            items.append(("part", text))
        elif level == "##" and (re.match(r"\d+\.", text) or text in ("Resumo", "Referências") or text.startswith("Apêndice")):
            items.append(("sec", text))
    lis = "".join(f'<li class="{k}"><a href="#{base.slug(base.inline(t))}">{base.inline(t)}</a></li>' for k, t in items)
    return f'<nav class="toc"><h2>Sumário</h2><ol>{lis}</ol></nav>'


def main():
    src = os.path.join(ART, "ARTIGO_TECNICO_FINAL_PTBR.md")
    dst = os.path.join(ART, "ARTIGO_TECNICO_FINAL_PTBR.html")
    md = open(src, encoding="utf-8").read()
    # the cover replaces the title block (title, subtitle, tagline); the metadata table stays in the body
    body_md = re.sub(r"\A#\s+.*\n##\s+.*\n\n>\s+.*\n", "", md)
    body = base.convert(body_md)
    body = re.sub(r'<h1 id="(parte-[^"]*)">', r'<h1 class="part" id="\1">', body)
    title = re.search(r"^#\s+(.*)$", md, re.M).group(1).strip()
    doc = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width, initial-scale=1">'
           f"<title>{html.escape(title)}</title><style>{base.CSS}{EXTRA_CSS}</style></head><body><main>"
           f"{cover(md)}{toc(md)}{body}</main></body></html>\n")
    open(dst, "w", encoding="utf-8").write(doc)
    print(f"{dst}  {len(doc) / 1e3:.0f} kB")


if __name__ == "__main__":
    main()
