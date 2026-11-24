#!/usr/bin/env python3
"""Turn Pluto static-HTML exports into readable posts that use the site's own layout.

For every entry in _data/notebooks.yml whose url is a Pluto export
(/notebooks/<name>.html), this reads the results Pluto already stored inside
the export and writes notebooks/<name>/index.html. The notebook is NOT re-run:
text, code, printed output and plots come out exactly as they are in your
notebook. Code you folded in Pluto stays hidden, code you left open is shown.
The original export stays at /notebooks/<name>.html as the interactive version.

Usage (from the repository root):  python3 _tools/pluto2post.py
Needs: pip install msgpack pygments pyyaml
"""
import base64, html, json, os, re, sys

import msgpack, yaml
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JuliaLexer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FMT = HtmlFormatter(nowrap=True)
LEX = JuliaLexer()


def load_state(path):
    src = open(path, encoding="utf-8").read()
    m = re.search(r'pluto_statefile\s*=\s*"data:[^;"]*;base64,([^"]+)"', src)
    if not m:
        return None
    return msgpack.unpackb(base64.b64decode(m.group(1)), raw=False, strict_map_key=False)


def as_text(body):
    if isinstance(body, msgpack.ExtType):
        body = body.data
    if isinstance(body, (bytes, bytearray)):
        return bytes(body).decode("utf-8", "replace")
    return body if isinstance(body, str) else str(body)


def as_bytes(body):
    if isinstance(body, msgpack.ExtType):
        return body.data
    if isinstance(body, str):
        return body.encode("latin-1", "replace")
    return bytes(body)


def esc(s):
    return html.escape(s, quote=False)


def render_value(val, mime):
    """Render one (value, mime) pair from a tree/table, inline."""
    if mime == "application/vnd.pluto.tree+object":
        return render_tree(val)
    if mime == "application/vnd.pluto.table+object":
        return render_table(val)
    if mime == "text/html":
        return as_text(val)
    return esc(as_text(val))


def render_tree(t):
    typ = t.get("type")
    prefix = esc(t.get("prefix", "") or "")
    parts = []
    for el in t.get("elements", []):
        if el == "more":
            parts.append("…")
            continue
        k, (v, vm) = el
        rv = render_value(v, vm)
        if typ in ("NamedTuple", "struct"):
            parts.append(f"{esc(str(k))} = {rv}")
        elif typ == "Dict":
            parts.append(f"{render_value(*k) if isinstance(k, list) else esc(str(k))} =&gt; {rv}")
        else:
            parts.append(rv)
    inner = ", ".join(parts)
    if typ == "Tuple":
        return f"({inner})"
    if typ == "NamedTuple":
        return f"({inner})"
    if typ == "struct":
        return f"{prefix}({inner})"
    if typ == "Dict":
        return f"{prefix or 'Dict'}({inner})"
    return f"{prefix}[{inner}]"


def render_table(t):
    names = t.get("schema", {}).get("names", [])
    head = "".join(f"<th>{'…' if n == 'more' else esc(str(n))}</th>" for n in names)
    rows = []
    for row in t.get("rows", []):
        if row == "more":
            rows.append(f'<tr><td colspan="{len(names) + 1}">…</td></tr>')
            continue
        i, cells = row
        tds = "".join("<td>…</td>" if c == "more" else f"<td>{render_value(*c)}</td>" for c in cells)
        rows.append(f"<tr><th>{esc(str(i))}</th>{tds}</tr>")
    return f'<div class="nb-table"><table><thead><tr><th></th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


def strip_scripts(s):
    return re.sub(r"<script\b.*?</script>", "", s, flags=re.S | re.I)


def render_output(out):
    mime, body = out.get("mime"), out.get("body")
    if mime == "text/html":
        h = strip_scripts(as_text(body)).strip()
        # Widgets that only work inside Pluto (e.g. TableOfContents) leave just a <style>: drop those.
        visible = re.sub(r"<style\b.*?</style>|<[^>]+>", "", h, flags=re.S | re.I).strip()
        if not visible and not re.search(r"<(img|svg|video|iframe|table)\b", h, re.I):
            return ""
        return f'<div class="nb-html">{h}</div>'
    if mime == "text/plain":
        t = as_text(body)
        return f'<pre class="nb-out">{esc(t)}</pre>' if t.strip() else ""
    if mime == "image/svg+xml":
        svg = re.sub(r"<\?xml[^>]*\?>", "", as_text(body))
        return f'<figure class="nb-fig">{svg}</figure>'
    if mime in ("image/png", "image/jpeg", "image/gif"):
        b64 = base64.b64encode(as_bytes(body)).decode()
        return f'<figure class="nb-fig"><img src="data:{mime};base64,{b64}" alt=""></figure>'
    if mime == "application/vnd.pluto.tree+object":
        return f'<pre class="nb-out">{render_tree(body)}</pre>'
    if mime == "application/vnd.pluto.table+object":
        return render_table(body)
    if mime == "application/vnd.pluto.stacktrace+object":
        msg = body.get("msg", "") if isinstance(body, dict) else as_text(body)
        return f'<pre class="nb-out nb-error">{esc(str(msg))}</pre>'
    return ""


ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
PKG_NOISE = re.compile(r"^\s*(Activating|Precompiling|Installing|Updating|Resolving|No Changes)\b.*$\n?", re.M)


def printed_logs(result):
    """Only what the notebook printed itself (println etc.), not progress bars or Pkg messages."""
    out = []
    for log in result.get("logs") or []:
        if not str(log.get("file", "")).replace("\\", "/").endswith("io/stdout.jl"):
            continue
        msg = log.get("msg")
        if isinstance(msg, list) and msg and isinstance(msg[0], str):
            out.append(msg[0])
    text = PKG_NOISE.sub("", ANSI.sub("", "".join(out)))
    return f'<pre class="nb-out nb-stdout">{esc(text)}</pre>' if text.strip() else ""


def code_block(code):
    return f'<div class="highlight nb-code"><pre><code>{highlight(code, LEX, FMT)}</code></pre></div>'


def convert(state):
    """Cells become HTML in notebook order. Consecutive cells that only show code
    (no output) are drawn as one code block; the ones before the first text cell
    (usually `using ...`) go into a collapsed "Setup" box."""
    parts, pending, seen_output = [], [], False

    def flush():
        nonlocal pending
        if pending:
            block = code_block("\n\n".join(pending))
            if not seen_output:
                block = f'<details class="nb-setup"><summary>Setup code</summary>{block}</details>'
            parts.append(f'<div class="nb-cell">{block}</div>')
            pending = []

    for cid in state["cell_order"]:
        inp, res = state["cell_inputs"][cid], state["cell_results"][cid]
        if inp.get("metadata", {}).get("disabled"):
            continue
        code = inp.get("code", "")
        show_code = not inp.get("code_folded") and code.strip()
        out = printed_logs(res) + render_output(res.get("output", {}))
        if not out:
            if show_code:
                pending.append(code.strip("\n"))
            continue
        flush()
        seen_output = True
        parts.append(f'<div class="nb-cell">{code_block(code) if show_code else ""}{out}</div>')
    flush()
    return "\n".join(parts)


def front_matter(entry, interactive_url):
    fm = {
        "layout": "notebook",
        "title": entry.get("title", ""),
        "date": str(entry.get("date", "")),
        "tags": entry.get("tags", []) or [],
        "interactive": interactive_url,
    }
    return "---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + "---\n"


def main():
    entries = yaml.safe_load(open(os.path.join(ROOT, "_data", "notebooks.yml"), encoding="utf-8")) or []
    done = 0
    for e in entries:
        url = str(e.get("url", ""))
        m = re.fullmatch(r"/notebooks/([^/]+)\.html", url)
        if not m:
            continue
        src = os.path.join(ROOT, "notebooks", m.group(1) + ".html")
        if not os.path.exists(src):
            print(f"skip {url}: file not found", file=sys.stderr)
            continue
        state = load_state(src)
        if state is None:
            print(f"skip {url}: not a Pluto export", file=sys.stderr)
            continue
        dst_dir = os.path.join(ROOT, "notebooks", m.group(1))
        os.makedirs(dst_dir, exist_ok=True)
        with open(os.path.join(dst_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(front_matter(e, url))
            f.write(convert(state) + "\n")
        done += 1
        print(f"converted {url} -> /notebooks/{m.group(1)}/")
    print(f"{done} notebook(s) converted")


if __name__ == "__main__":
    main()
