# Judging brief (three tasks, files in this folder)

You are the judge for a job-search evaluation. Everything is fictional and local: no real candidates, no external
calls. Do tasks 1 and 2 yourself, in order, in one pass each, with ONE standard (do not use subagents for them, and
do not go back to change earlier verdicts: consistency is the point). Task 3 may use subagents.

## The standard for tasks 1 and 2

A role is **Y** when this candidate would plausibly apply to it:
- right profession (the same function, or a neighbour a person with this CV would search), and
- roughly right level (within one step of the candidate's level; an intern CV vs a director role is N, an exec vs an
  intern role is N), and
- in or near the candidate's country (the location column; remote roles count only if they name the country).
Otherwise **N**. Keyword overlap alone is not enough: "Account Manager" at a bank is not a fit for a nurse. Judge from
title, company and location only. Language of the posting is not a reason to say N.

## Task 1: `embed_bench/packet.md` -> `embed_bench/labels.json`

Packet lines are `- <job_id> | title | company | location` under `## <slug> | level | country | headline`.
Write `{ "<slug>": { "<job_id>": 1 or 0, ... }, ... }` covering EVERY role of EVERY persona.

## Task 2: `ranking/packet.md` -> `ranking/labels.json`

Same standard. Roles sit under `### <slug> / <search> / searched ...`; a `label=` field is the feed's own match label,
IGNORE it when judging (it is what we are testing). Write `{ "<slug>/<search>": { "<job_id>": 1 or 0, ... }, ... }`
covering every role listed. The same job id may appear in several searches: judge it per candidate, once per search.

## Task 3: `coverage/targets.csv` -> `coverage/employers.json`

For each (profession, country) row, list up to 25 REAL employers that hire people in that role in that country,
mixing large and mid-size, local and international; no invented companies (a wrong name is fine, a made-up one is not).
Write a JSON list of `{"profession","country","employers":[{"name","why":"one line","ats_guess":"greenhouse|lever|ashby|workable|smartrecruiters|workday|successfactors|personio|other|unknown"}]}`.
These names are only candidates: a local tool will verify them against public job boards.

## Check and finish

Run `python3 judging/validate_judging.py` after each task and fix what it reports. Commit per task
(`judging: task 1`, ...) to the branch you are on, push it, and stop. Do not open a pull request.
