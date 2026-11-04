"""Checks labels/employers against the packets. Usage: python3 judging/validate_judging.py (stdlib only)."""
import csv, json, re, sys
from pathlib import Path
R = Path(__file__).resolve().parent
problems = []

def packet_ids(path, header):
    ids, cur = {}, None
    for line in path.read_text().splitlines():
        m = re.match(header, line)
        if m: cur = m.group(1); ids[cur] = []; continue
        m = re.match(r"- (\d+) \|", line)
        if m and cur: ids[cur].append(m.group(1))
    return ids

for name, header in (("embed_bench", r"## (\S+) \|"), ("ranking", r"### (\S+ / \S+) /")):
    f = R / name / "labels.json"
    if not f.exists(): print(f"{name}: labels.json missing"); continue
    labels = json.loads(f.read_text())
    for key, ids in packet_ids(R / name / "packet.md", header).items():
        got = labels.get(key, {})
        for i in ids:
            if got.get(i) not in (0, 1): problems.append(f"{name}: {key} {i} unlabeled")
    print(f"{name}: {len(labels)} lists, {sum(len(v) for v in labels.values())} labels")

f = R / "coverage" / "employers.json"
if f.exists():
    data = json.loads(f.read_text())
    want = {(r["profession"], r["country"]) for r in csv.DictReader(open(R / "coverage" / "targets.csv"))}
    got = {(d["profession"], d["country"]) for d in data}
    problems += [f"coverage: missing {k}" for k in sorted(want - got)][:20]
    print(f"coverage: {len(got & want)}/{len(want)} targets")
for p in problems[:40]: print(" -", p)
print("OK" if not problems else f"{len(problems)} problems")
