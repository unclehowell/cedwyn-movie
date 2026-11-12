#!/usr/bin/env python3
"""Fold record-only scenes into the nearest real moment, park scenes outside the film, and regroup into parts.

    python3 tools/script_patch.py --apply && python3 tools/script_fold.py --apply

A fold file (folds/<date>-<name>.json) holds:
  "fold":     {target id: [ids]}   each listed scene leaves the door list and joins the target: its events and
                                   evidence are added to the target, and it is listed under the target's "also"
                                   (id, date, title, logline) to be shown as a dated on-screen caption.
  "appendix": {"from": id, "ids": [ids]}  scenes from `from` to the end, and the listed ids, move to F["appendix"].
  "add":      [{"after": id, "scene": {...}}]  a new scene.
  "parts":    [{"n", "en", "cy", "es", "start": id}]  replaces the act list; each part starts at `start`.
Nothing is deleted: a folded scene is kept whole in F["folded"] with "folded_into", a parked one in F["appendix"].
Idempotent. Runs the chronology check from script_patch.py before writing. — Claude agent
"""
import glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from script_patch import check, parse, iso


def apply(F, P):
    items = F["items"]; by = {x["id"]: x for x in items}
    F.setdefault("folded", []); F.setdefault("appendix", [])
    for a in P.get("add", []):
        s = a["scene"]
        if s["id"] not in by and not any(y["id"] == s["id"] for y in F["appendix"]):
            s = dict(s); s["date_sort"] = iso(parse(s["date_range"])[0])
            items.insert(items.index(by[a["after"]]) + 1, s); by[s["id"]] = s
    ap = P.get("appendix", {})
    park = list(ap.get("ids", []))
    if ap.get("from") in by:
        park += [x["id"] for x in items[items.index(by[ap["from"]]):]]
    for i in park:
        if i in by:
            x = by.pop(i); items.remove(x); F["appendix"].append(x)
    for target, ids in P.get("fold", {}).items():
        t = by[target]
        for i in ids:
            if i not in by: continue
            x = by.pop(i); items.remove(x); x["folded_into"] = target; F["folded"].append(x)
            t.setdefault("also", []).append({"id": i, "date": x.get("date_label") or x["date_range"], "title": x["title"], "logline": x["logline"]})
            for k in ("events", "evidence"):
                t[k] = (t.get(k) or []) + [e for e in (x.get(k) or []) if e not in (t.get(k) or [])]
    parts = P.get("parts")
    if parts:
        F["acts"] = [{k: p[k] for k in ("n", "en", "cy", "es")} for p in parts]
        starts = {p["start"]: p for p in parts}; cur = F["acts"][0]
        for x in items:
            if x["id"] in starts: cur = {k: starts[x["id"]][k] for k in ("n", "en", "cy", "es")}
            x["act"] = dict(cur)
    for n, x in enumerate(items, 1): x["n"] = n
    for lst in (F["folded"], F["appendix"]):
        for x in lst: x["n"] = None
    meta = P.get("meta")
    if meta and not any(c.get("version") == meta["version"] for c in F.get("changelog", [])):
        F["changelog"].append(meta); F["version"] = meta["version"]
    F["frames"] = len(items); m = len(items) * F.get("target_seconds_each", 120) // 60
    F["estimated_runtime"] = "%d h %02d min" % (m // 60, m % 60)
    return F


def main():
    F = json.load(open("frames.json", encoding="utf-8"))
    if "--apply" in sys.argv:
        for p in sorted(glob.glob("folds/*.json")):
            F = apply(F, json.load(open(p, encoding="utf-8"))); print("applied", p)
    errs = check(F)
    for e in errs: print("FAIL", e)
    sizes = {}
    for x in F["items"]: sizes[x["act"]["n"]] = sizes.get(x["act"]["n"], 0) + 1
    print("%d scenes, %d folded, %d parked, %d faults; parts %s" % (len(F["items"]), len(F.get("folded", [])), len(F.get("appendix", [])), len(errs), sizes))
    if errs: sys.exit(1)
    if "--apply" in sys.argv:
        open("frames.json", "w", encoding="utf-8").write(json.dumps(F, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
