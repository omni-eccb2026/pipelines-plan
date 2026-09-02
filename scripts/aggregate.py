#!/usr/bin/env python3
"""Exercise 17: plot RSS over time from denet traces.

    python3 scripts/aggregate.py prof/*.jsonl        # -> prof/rss.svg

denet already summarises a trace (`denet stats FILE`); the one thing it does
not do is draw the curve, so that is all this does.

ponytail: hand-rolled SVG instead of matplotlib — the `prof` env in exercise 17
only has denet in it, and a line chart is not worth a second install. Swap in
matplotlib if you ever need axes ticks, log scales or more than one panel.
"""
import json
import sys

W, H, PAD = 900, 380, 55
COLORS = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e"]


def load(path):
    """-> (label, [(seconds, rss_mb), ...]) for one denet .jsonl trace."""
    t0, pts = None, []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if t0 is None:                      # first line is the header
                t0 = rec.get("t0_ms")
                if t0 is not None:
                    continue
            agg = rec.get("aggregated")
            if not agg or "ts_ms" not in rec:
                continue
            if t0 is None:
                t0 = rec["ts_ms"]
            pts.append(((rec["ts_ms"] - t0) / 1000.0, agg["mem_rss_kb"] / 1024.0))
    return path.rsplit("/", 1)[-1].removesuffix(".jsonl"), pts


def svg(series, out):
    xs = [x for _, pts in series for x, _ in pts]
    ys = [y for _, pts in series for _, y in pts]
    if not xs:
        sys.exit("no samples found — did denet write anything?")
    xmax, ymax = max(xs) or 1.0, max(ys) or 1.0
    sx = lambda x: PAD + x / xmax * (W - 2 * PAD)
    sy = lambda y: H - PAD - y / ymax * (H - 2 * PAD)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'font-family="sans-serif" font-size="12">',
         f'<rect width="{W}" height="{H}" fill="white"/>',
         f'<path d="M{PAD},{PAD} V{H-PAD} H{W-PAD}" stroke="#999" fill="none"/>',
         f'<text x="{PAD}" y="{PAD-16}">peak {ymax:.0f} MB · {xmax:.0f} s</text>']
    for i, (label, pts) in enumerate(series):
        c = COLORS[i % len(COLORS)]
        d = " ".join(f"{'M' if j == 0 else 'L'}{sx(x):.1f},{sy(y):.1f}"
                     for j, (x, y) in enumerate(pts))
        p.append(f'<path d="{d}" stroke="{c}" stroke-width="1.6" fill="none"/>')
        p.append(f'<text x="{W-PAD-140}" y="{PAD+16*i}" fill="{c}">{label}</text>')
    p.append("</svg>")
    with open(out, "w") as fh:
        fh.write("\n".join(p))


def selfcheck():
    import tempfile, os
    trace = ('{"pid":1,"t0_ms":1000}\n'
             '{"ts_ms":1500,"aggregated":{"mem_rss_kb":1024}}\n'
             '{"ts_ms":2000,"aggregated":{"mem_rss_kb":4096}}\n')
    d = tempfile.mkdtemp()
    path = os.path.join(d, "t.jsonl")
    open(path, "w").write(trace)
    label, pts = load(path)
    assert label == "t", label
    assert pts == [(0.5, 1.0), (1.0, 4.0)], pts
    out = os.path.join(d, "t.svg")
    svg([(label, pts)], out)
    body = open(out).read()
    assert "peak 4 MB" in body, body[:200]
    assert body.count("<path") == 2, body           # axes + one series
    print("selfcheck ok")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--selfcheck"]:
        selfcheck()
    elif not args:
        sys.exit(__doc__)
    else:
        series = [load(a) for a in args]
        out = args[0].rsplit("/", 1)[0] + "/rss.svg" if "/" in args[0] else "rss.svg"
        svg(series, out)
        for label, pts in series:
            print(f"{label:12s} peak {max(y for _, y in pts):8.0f} MB  "
                  f"{len(pts):4d} samples  {max(x for x, _ in pts):6.1f} s")
        print(f"wrote {out}  (compare peak with max_rss in *_performance.txt)")
