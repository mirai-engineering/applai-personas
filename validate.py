"""Checks personas/ against matrix.csv. Usage: python3 validate.py   (stdlib only)."""
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KEYS = {"slug", "level", "profession", "band", "location", "region", "cv_language", "layout", "searches",
        "cross_check_roles", "output_languages", "cv"}
CV_KEYS = {"name", "headline", "contact", "summary", "experience", "education", "skills", "languages",
           "certifications", "projects", "extra_sections"}
STOP = {"en": {"the", "and", "with", "for", "of"}, "de": {"und", "der", "die", "mit", "für"},
        "fr": {"et", "le", "la", "avec", "pour"}, "es": {"y", "el", "la", "con", "para"}}
problems, names, emails = [], set(), set()
rows = list(csv.DictReader(open(ROOT / "matrix.csv")))
for r in rows:
    f = ROOT / "personas" / f"{r['slug']}.json"
    if not f.exists():
        problems.append(f"{r['slug']}: missing"); continue
    try:
        d = json.loads(f.read_text())
    except json.JSONDecodeError as e:
        problems.append(f"{r['slug']}: invalid JSON ({e})"); continue
    if set(d) != KEYS: problems.append(f"{r['slug']}: keys differ: {sorted(set(d) ^ KEYS)}"); continue
    if set(d["cv"]) != CV_KEYS: problems.append(f"{r['slug']}: cv keys differ: {sorted(set(d['cv']) ^ CV_KEYS)}"); continue
    for k, col in (("slug", "slug"), ("level", "level"), ("profession", "profession"), ("band", "band"),
                   ("region", "region"), ("cv_language", "cv_language")):
        if d[k] != r[col]: problems.append(f"{r['slug']}: {k}={d[k]!r}, matrix says {r[col]!r}")
    if d["location"] != r["country"]: problems.append(f"{r['slug']}: location != country")
    if d["output_languages"][0] != r["cv_language"]: problems.append(f"{r['slug']}: output_languages must start with the cv language")
    if [s["name"] for s in d["searches"]] != ["primary", "adjacent", "open"] or d["searches"][2]["roles"] != []:
        problems.append(f"{r['slug']}: searches must be primary, adjacent, open (open has no roles)")
    elif not d["searches"][0]["roles"] or not d["searches"][1]["roles"]:
        problems.append(f"{r['slug']}: primary and adjacent need a role")
    cv = d["cv"]
    if not cv["contact"]["email"].endswith("@example.com"): problems.append(f"{r['slug']}: email must use example.com")
    if cv["name"] in names: problems.append(f"{r['slug']}: duplicate name {cv['name']}")
    names.add(cv["name"])
    if not cv["experience"] or not all(e.get("bullets") is not None for e in cv["experience"]):
        problems.append(f"{r['slug']}: experience entries need bullets")
    words = re.findall(r"[a-zäöüéèàñáíóúç]+", (cv["summary"] + " " + " ".join(b for e in cv["experience"] for b in e["bullets"])).lower())
    lang = r["cv_language"]
    hits = {l: sum(w in s for w in words) for l, s in STOP.items()}
    if hits[lang] < max(hits.values()) and hits[lang] < 3:
        problems.append(f"{r['slug']}: text does not look {lang}")
extra = {p.stem for p in (ROOT / "personas").glob("*.json")} - {r["slug"] for r in rows}
problems += [f"{s}: not in matrix.csv" for s in sorted(extra)]
done = len(rows) - sum(1 for p in problems if p.endswith("missing"))
print(f"{done}/{len(rows)} files present, {len(problems)} problems")
for p in problems[:50]: print(" -", p)
sys.exit(1 if problems and done == len(rows) else 0)
