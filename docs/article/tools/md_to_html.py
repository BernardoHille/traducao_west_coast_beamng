"""Conversor Markdown -> HTML minimo para o artigo (sem dependencias externas).

Cobre o subconjunto usado em ARTIGO_TECNICO_PTBR.md: titulos, paragrafos, enfase, codigo inline e em bloco,
links, imagens (imagem seguida de legenda em italico vira <figure>), tabelas pipe, citacoes, listas
(um nivel de aninhamento) e regua horizontal.
Uso: python docs/article/tools/md_to_html.py [entrada.md] [saida.html]
"""
import html
import os
import re
import sys

ART = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

CSS = """
:root{--bg:#ffffff;--fg:#1c2026;--muted:#5b6470;--line:#dde1e6;--soft:#f5f7f9;--accent:#1d63c4;--code:#f1f3f5}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#15181c;--fg:#e6e8eb;--muted:#a3abb5;--line:#323840;--soft:#1d2126;--accent:#7fb0ff;--code:#22272d}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.65 "Segoe UI",system-ui,-apple-system,Arial,sans-serif}
main{max-width:960px;margin:0 auto;padding:32px 16px 80px}
h1{font-size:1.9rem;line-height:1.25;margin:0 0 .2em}
h1+h2{font-weight:500;color:var(--muted);margin-top:0;border:0}
h2{font-size:1.45rem;margin:2.2em 0 .6em;padding-top:.4em;border-top:1px solid var(--line)}
h3{font-size:1.15rem;margin:1.6em 0 .5em}
a{color:var(--accent)}
code{background:var(--code);padding:.1em .35em;border-radius:4px;font:0.88em Consolas,"Cascadia Mono",monospace;overflow-wrap:anywhere}
pre{background:var(--code);padding:14px 16px;border-radius:8px;overflow-x:auto}
pre code{background:none;padding:0}
blockquote{margin:1em 0;padding:.6em 1em;border-left:4px solid var(--accent);background:var(--soft)}
.table-wrap{overflow-x:auto;margin:1em 0}
table{border-collapse:collapse;width:100%;font-size:.92rem}
th,td{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}
th{background:var(--soft)}
figure{margin:1.6em 0}
figure img{display:block;max-width:100%;height:auto;margin:0 auto;border:1px solid var(--line);border-radius:6px;background:#fff}
figcaption{color:var(--muted);font-size:.92rem;margin-top:.6em}
hr{border:0;border-top:1px solid var(--line);margin:2em 0}
p.caption{color:var(--muted);font-size:.92rem}
@media print{body{font-size:11pt}main{max-width:none;padding:0}h2{break-before:auto}figure,table,pre{break-inside:avoid}a{color:inherit}}
"""


def inline(t):
    codes = []

    def keep(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    t = re.sub(r"`([^`]+)`", keep, t)
    t = html.escape(t, quote=False)
    t = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" loading="lazy">', t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{html.escape(codes[int(m.group(1))], quote=False)}</code>", t)
    return t


def slug(t):
    t = re.sub(r"<[^>]+>", "", t).lower()
    t = re.sub(r"[^\w\s-]", "", t, flags=re.U)
    return re.sub(r"\s+", "-", t.strip())


def convert(md):
    lines = md.splitlines()
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].startswith("```"):
                buf.append(lines[j])
                j += 1
            out.append("<pre><code>" + html.escape("\n".join(buf), quote=False) + "</code></pre>")
            i = j + 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            n, txt = len(m.group(1)), inline(m.group(2))
            out.append(f'<h{n} id="{slug(txt)}">{txt}</h{n}>')
            i += 1
            continue
        if ln.strip() == "---":
            out.append("<hr>")
            i += 1
            continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            head, body = cells[0], [r for r in cells[2:]]
            h = "<div class='table-wrap'><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            h += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
            out.append(h + "</tbody></table></div>")
            continue
        if ln.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].strip())
                i += 1
            out.append("<blockquote><p>" + inline(" ".join(buf)) + "</p></blockquote>")
            continue
        mi = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", ln)
        if mi:
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            cap = ""
            if j < len(lines) and lines[j].startswith("*Figura"):
                cap = f"<figcaption>{inline(lines[j].strip().strip('*'))}</figcaption>"
                i = j + 1
            else:
                i += 1
            out.append(f'<figure><img src="{mi.group(2)}" alt="{html.escape(mi.group(1))}" loading="lazy">{cap}</figure>')
            continue
        if re.match(r"^(\s*)([-*]|\d+\.)\s+", ln):
            out.append(list_block(lines, i))
            i = list_block.end
            continue
        if not ln.strip():
            i += 1
            continue
        buf = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||>|```|!\[|\s*([-*]|\d+\.)\s|---$)", lines[i]):
            buf.append(lines[i])
            i += 1
        txt = " ".join(s.strip() for s in buf)
        cls = ' class="caption"' if txt.startswith("*Tabela") else ""
        out.append(f"<p{cls}>{inline(txt)}</p>")
    return "\n".join(out)


def list_block(lines, i):
    """One list with optional nested items (indent >= 2)."""
    items, base = [], None
    ordered = bool(re.match(r"^\s*\d+\.\s", lines[i]))
    while i < len(lines):
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
        if not m:
            if lines[i].startswith("   ") and lines[i].strip() and items:
                items[-1][1].append(lines[i].strip())
                i += 1
                continue
            break
        ind = len(m.group(1))
        if base is None:
            base = ind
        if ind > base and items:
            items[-1][2].append(m.group(3))
        else:
            items.append([m.group(3), [], []])
        i += 1
    list_block.end = i
    tag = "ol" if ordered else "ul"
    html_items = []
    for text, cont, sub in items:
        s = inline(" ".join([text] + cont))
        if sub:
            s += "<ul>" + "".join(f"<li>{inline(x)}</li>" for x in sub) + "</ul>"
        html_items.append(f"<li>{s}</li>")
    return f"<{tag}>" + "".join(html_items) + f"</{tag}>"


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ART, "ARTIGO_TECNICO_PTBR.md")
    dst = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ART, "ARTIGO_TECNICO_PTBR.html")
    md = open(src, encoding="utf-8").read()
    title = re.search(r"^#\s+(.*)$", md, re.M).group(1).rstrip(":")
    body = convert(md)
    doc = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
           f'<meta name="viewport" content="width=device-width, initial-scale=1">'
           f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body><main>{body}</main></body></html>\n")
    open(dst, "w", encoding="utf-8").write(doc)
    print(f"{dst}  {len(doc) / 1e3:.0f} kB")


if __name__ == "__main__":
    main()
