#!/usr/bin/env python3
"""Apply reviewed script patches to frames.json and check the chronology.

    python3 tools/script_patch.py --check     # check frames.json as it stands
    python3 tools/script_patch.py --apply     # apply patches/*.json in name order, then check, then write

A patch file (patches/<date>-<name>.json) holds:
  "set":      {id: {field: value}}                 plain field values (date, title, logline ...)
  "i18n":     {id: {"cy"|"es": {"title","logline"}}}
  "replace":  [{id, old, new, lang?, first?}]      exact text swap inside a logline / description ("first": only the first match)
  "move":     [{"id", "after"}]                    put scene `id` straight after scene `after`
  "date_sort":{id: "YYYY-MM-DD"}                   where the order rests on reasoning, not on the date text
  "act_starts": {act number: id of its first scene}
  "why":      {id: reason}                         read by people, ignored here
  "meta":     {"version", "date", "change"}        one changelog line

Applying is idempotent: a second run changes nothing, on the unfolded file or on a file script_fold.py has
already folded (folded and parked scenes are patched where they sit). Scenes are never dropped and ids never change.

The check (also run after --apply) fails when
  1. a scene's date_sort is earlier than the scene before it;
  2. a scene's date_sort falls outside its own date_range;
  3. act numbers go backwards;
  4. door numbers are not 1..N, an id repeats, or an event id sits in two scenes.
date_sort is the day a scene is placed at. A year-only or month-only date is placed at its first day
unless the patch gives a later day with the reason in "why".
— Claude agent
"""
import glob, json, re, sys

MON = {m: i + 1 for i, m in enumerate(
    "january february march april may june july august september october november december".split())}
MRE = "|".join(MON)


def parse(s):
    """date text -> ((y,m,d) first day, (y,m,d) last day, precision)"""
    t = s.lower()
    m = re.search(r"c\.\s*(\d+)\s*bc", t)
    if m:
        y = -int(m.group(1)); return (y, 1, 1), (y, 12, 31), "approx"
    m = re.search(r"c\.\s*ad\s*(\d+)", t)
    if m:
        y = int(m.group(1)); return (y, 1, 1), (y, 12, 31), "approx"
    m = re.search(r"(\d{1,2})(?:[–-](\d{1,2}))?\s+(" + MRE + r")\s+(\d{4})", t)
    if m:
        d1 = int(m.group(1)); d2 = int(m.group(2) or d1); mo = MON[m.group(3)]; y = int(m.group(4))
        return (y, mo, d1), (y, mo, d2), "day"
    m = re.search(r"(early|mid|late)?[- ]*(" + MRE + r")\s+(\d{4})", t)
    if m:
        lo, hi = {"early": (1, 10), "mid": (11, 20), "late": (21, 31), None: (1, 31)}[m.group(1)]
        return (int(m.group(3)), MON[m.group(2)], lo), (int(m.group(3)), MON[m.group(2)], hi), "month"
    m = re.search(r"(early|spring|summer|autumn|winter)\s+(\d{4})", t)
    if m:
        a, b = {"early": (1, 3), "spring": (3, 5), "summer": (6, 8), "autumn": (9, 11), "winter": (12, 12)}[m.group(1)]
        return (int(m.group(2)), a, 1), (int(m.group(2)), b, 31), "season"
    m = re.search(r"c\.\s*(\d{3,4})(?:[–-](\d{2,4}))?", t)
    if m:
        y = int(m.group(1)); y2 = m.group(2)
        if y2:
            y2 = int(y2) if len(y2) == 4 else int(str(y)[: len(str(y)) - len(y2)] + y2)
        return (y, 1, 1), (y2 or y, 12, 31), "approx"
    m = re.search(r"(\d{4})", t)
    if m:
        y = int(m.group(1)); return (y, 1, 1), (y, 12, 31), "year"
    m = re.search(r"(\d+)(?:st|nd|rd|th) century", t)
    if m:
        base = (int(m.group(1)) - 1) * 100
        q = re.search(r"(early|close of the|late|mid)", t)
        a, b = {"early": (0, 33), "mid": (34, 66), "late": (67, 99), "close of the": (90, 99)}.get(q.group(1) if q else None, (0, 99))
        return (base + a, 1, 1), (base + b, 12, 31), "approx"
    raise ValueError("date not understood: %r" % s)


def iso(t):
    y, m, d = t
    return ("-%04d" % -y if y < 0 else "%04d" % y) + "-%02d-%02d" % (m, d)


def uniso(s):
    neg = s.startswith("-"); y, m, d = s.lstrip("-").split("-")
    return (-int(y) if neg else int(y), int(m), int(d))


def apply(F, P):
    items = F["items"]; by = {x["id"]: x for x in items}
    every = dict(by)                      # folded and parked scenes are patched too, so a patch can be re-run on a folded file
    for x in (F.get("folded") or []) + (F.get("appendix") or []): every.setdefault(x["id"], x)
    for i, fields in P.get("set", {}).items():
        x = every[i]
        for k, v in fields.items():
            if k == "date":            # one date for the whole scene
                x["date_from"] = x["date_to"] = x["date_range"] = v
            else:
                x[k] = v
        if "logline" in fields and (isinstance(x.get("description"), str) or x.get("description") is None):
            x["description"] = fields["logline"]
    for i, langs in P.get("i18n", {}).items():
        x = every[i]; x.setdefault("i18n", {})
        for lang, v in langs.items():
            x["i18n"].setdefault(lang, {}).update(v)
    for r in P.get("replace", []):
        x = every[r["id"]]; lang = r.get("lang"); n = 1 if r.get("first") else -1
        tgt = x["i18n"][lang] if lang else x
        if r["new"] in tgt.get("logline", ""):
            continue                       # already applied
        if r["old"] not in tgt.get("logline", ""):
            raise SystemExit("replace: text not found in %s %s" % (r["id"], lang or "en"))
        tgt["logline"] = tgt["logline"].replace(r["old"], r["new"], n)
        if not lang and isinstance(x.get("description"), str) and r["new"] not in x["description"]:
            x["description"] = x["description"].replace(r["old"], r["new"], n)
    for mv in P.get("move", []):
        if mv["id"] not in by or mv["after"] not in by: continue   # one of the two is folded or parked
        x = by[mv["id"]]; items.remove(x); items.insert(items.index(by[mv["after"]]) + 1, x)
    starts = {v: int(k) for k, v in P.get("act_starts", {}).items()}
    if starts and not F.get("folded"):     # once folded, the parts come from the fold file
        acts = {a["n"]: a for a in F["acts"]}; cur = 1
        for x in items:
            cur = starts.get(x["id"], cur); x["act"] = dict(acts[cur])
    explicit = P.get("date_sort", {})
    for n, x in enumerate(items, 1):
        x["n"] = n
        if x["id"] in explicit:
            x["date_sort"] = explicit[x["id"]]
        elif "date_sort" not in x or x["id"] in P.get("set", {}):
            x["date_sort"] = iso(parse(x["date_range"])[0])
    meta = P.get("meta")
    if meta and not any(c.get("version") == meta["version"] for c in F.get("changelog", [])):
        F["changelog"].append(meta); F["version"] = meta["version"]; F["updated"] = meta["date"] + "T00:00Z"
        F["date_sort_rule"] = ("Every scene carries date_sort (YYYY-MM-DD): the day it is placed at. Scenes are in "
                               "non-decreasing date_sort order and each date_sort lies inside the scene's own date_range. "
                               "tools/script_patch.py --check fails otherwise. — Claude agent")
    F["frames"] = len(items)
    return F


def check(F):
    items = F["items"]; errs = []; prev = None; seen = {}; ev = {}
    for n, x in enumerate(items, 1):
        if x["n"] != n: errs.append("%s: door number %s, expected %s" % (x["id"], x["n"], n))
        if x["id"] in seen: errs.append("%s: id repeats" % x["id"])
        seen[x["id"]] = 1
        for e in set(x.get("events") or []):
            if e in ev: errs.append("event %s in %s and %s" % (e, ev[e], x["id"]))
            ev[e] = x["id"]
        lo, hi, _ = parse(x["date_range"])
        ds = uniso(x["date_sort"]) if x.get("date_sort") else lo
        if not (lo <= ds <= hi): errs.append("%s: date_sort %s outside '%s'" % (x["id"], x.get("date_sort"), x["date_range"]))
        if prev and ds < prev[0]: errs.append("%s (%s) is placed after %s (%s)" % (x["id"], x["date_range"], prev[1], prev[2]))
        if prev and x["act"]["n"] < prev[3]: errs.append("%s: act %s after act %s" % (x["id"], x["act"]["n"], prev[3]))
        prev = (ds, x["id"], x["date_range"], x["act"]["n"])
    return errs


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    path = "frames.json"
    F = json.load(open(path, encoding="utf-8"))
    if mode == "--apply":
        for p in sorted(glob.glob("patches/*.json")):
            F = apply(F, json.load(open(p, encoding="utf-8"))); print("applied", p)
    errs = check(F)
    for e in errs: print("FAIL", e)
    print("%d scenes, %d faults" % (len(F["items"]), len(errs)))
    if errs: sys.exit(1)
    if mode == "--apply":
        open(path, "w", encoding="utf-8").write(json.dumps(F, ensure_ascii=False, separators=(",", ":")))
        print("wrote", path, "version", F["version"])


if __name__ == "__main__":
    main()
