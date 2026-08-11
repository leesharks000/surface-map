#!/usr/bin/env python3
"""build_dodecad_nodes.py — generate Atlas nodes from the heteronym records.

MANUS, 2026-08-10: "lets generate nodes from there, and from the network map,
without overwriting whats there. and we can simply regenerate when its full."

So this APPENDS. It writes one block, delimited by markers, and rewrites only
what lies between them. Everything the Atlas already holds — the disambiguation,
the provenance chain, the network list, the seven JSON-LD blocks — is untouched.
Run it again when more records exist and the block regenerates in place.

The source of truth is datasets/heteronyms/records/*.json, which carry rooms,
arks, institutions, journals, traversals and verification state in structured
form. The Atlas named five of twelve positions and omitted every heteronym
verified on 2026-08-10; generating from the records means it cannot fall behind
again, because adding a record adds a node.

    python3 scripts/build_dodecad_nodes.py            # report
    python3 scripts/build_dodecad_nodes.py --apply
"""
import glob
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
RECORDS = ROOT.parent / 'live/datasets/heteronyms/records'
ATLAS = ROOT / 'index.html'
START = '<!-- DODECAD-NODES-START generated from datasets/heteronyms/records -->'
END = '<!-- DODECAD-NODES-END -->'


def load():
    out = []
    for f in sorted(glob.glob(str(RECORDS / '*.json'))):
        d = json.loads(pathlib.Path(f).read_text())
        cv = d.get('corpus_verified') or {}
        room = None
        rooms = d.get('rooms')
        if isinstance(rooms, list) and rooms:
            room = rooms[0].get('name')
        elif isinstance(rooms, dict):
            room = rooms.get('name')
        inst = (d.get('institution') or {})
        out.append({
            'name': d.get('name'),
            'slug': d.get('person_id'),
            'function': (d.get('function') or '')[:80],
            'institution': inst.get('name') if isinstance(inst, dict) else None,
            'room': room,
            'ark': (d.get('ark') or {}).get('name'),
            'journal': (d.get('journal') or {}).get('name') if isinstance(d.get('journal'), dict) else None,
            'surface': (d.get('surface') or {}).get('canonical') or (d.get('seating') or {}).get('surface'),
            'records': cv.get('on_surface'),
            'corpus': cv.get('live_citable_authorial'),
            'verified': bool(cv.get('READ_AS_RENDERED')),
            'traversals': (d.get('traversal_logs') or {}).get('count'),
        })
    return out


def render(rows):
    cells = []
    for r in rows:
        bits = [b for b in (r['institution'], r['room'], r['ark']) if b]
        sub = ' &middot; '.join(bits)[:96]
        link = (f'<a href="{r["surface"]}">{r["name"]}</a>' if r['surface']
                else f'<span style="color:var(--text-dim)">{r["name"]}</span>')
        meta = []
        if r['records']:
            meta.append(f'{r["records"]} records')
        if r['corpus']:
            meta.append(f'{r["corpus"]} live works')
        if r['traversals']:
            meta.append(f'{r["traversals"]} traversals')
        cells.append(
            '<div style="margin-bottom:6px">'
            f'{link} <span style="color:var(--text-dim);font-size:.9em">'
            f'&mdash; {r["function"]}</span>'
            + (f'<br><span style="color:var(--text-dim);font-size:.82em">{sub}</span>'
               if sub else '')
            + (f'<br><span style="color:var(--accent);font-size:.78em">'
               f'{" &middot; ".join(meta)}</span>' if meta else '')
            + '</div>')
    n = len(rows)
    return (
        f'{START}\n'
        '<h4 style="font-size:0.78em;color:var(--accent-bright);margin:14px 15px 4px 15px;'
        'text-transform:uppercase;letter-spacing:0.04em;font-weight:500">'
        f'The Dodecad &mdash; {n} of 12 positions mapped</h4>\n'
        '<div style="padding:0 15px;font-size:0.75em;color:var(--text-dim);margin:0 0 10px 0;'
        'font-style:italic">Generated from the heteronym records. Each position is a node; '
        'its institution, room and ark are its edges.</div>\n'
        '<div style="padding:0 15px;display:grid;'
        'grid-template-columns:repeat(auto-fit,minmax(260px,1fr));column-gap:24px;row-gap:4px;'
        'font-size:0.82em;line-height:1.55">\n' + '\n'.join(cells) + '\n</div>\n'
        f'{END}'
    )


if __name__ == '__main__':
    rows = load()
    block = render(rows)
    s = ATLAS.read_text()
    if START in s:
        s2 = re.sub(re.escape(START) + r'.*?' + re.escape(END), block, s, flags=re.S)
        mode = 'regenerated in place'
    else:
        m = re.search(r'(<h4[^>]*>\s*Allied Sites\s*</h4>)', s)
        anchor = m.start() if m else s.rfind('</div>')
        s2 = s[:anchor] + block + '\n' + s[anchor:]
        mode = 'appended'
    print(f'  {len(rows)} record(s) → {mode}')
    for r in rows:
        print(f'    {r["name"]:<20} {r["records"] or "—":>4} records · '
              f'{"verified" if r["verified"] else "not read"}')
    if '--apply' in sys.argv:
        ATLAS.write_text(s2)
        print('  written')
