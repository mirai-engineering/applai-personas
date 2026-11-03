# Task: write fictional job-seeker personas

You are writing test data for a job-search evaluation. Each persona is a fictional candidate whose CV and
job searches will be run through a job-search feed, to find where matching and employer coverage fail.
Nothing here touches real people, real services or secrets. Do not call any external API.

## What to produce

For every row of `matrix.csv` (266 rows), write `personas/<slug>.json`, in the same shape as the files in
`examples/` (copy their keys exactly; they are the schema). One file per row, no other output files.

The columns of a row are constraints, not suggestions:

| Column | Meaning |
|---|---|
| `slug` | the file name and the `slug` field |
| `profession`, `seed_role` | the field and a typical role. Write the title the way a candidate in that country would on a CV (German `Projektleiter`, Spanish `Ingeniero de datos`...), not a translation of `seed_role` |
| `level`, `band` | intern / junior / mid / senior / exec and years of experience; dates and scope must fit |
| `country`, `city`, `region` | where the candidate lives (`location` is the country, CV contact location is the city) |
| `cv_language` | the language the CV text is written in; `output_languages` lists it first |
| `messiness` | `clean`: linear career. `noisy_titles`: real-world, inconsistent titles (abbreviations, internal job grades, "Sr."). `career_change`: the target role differs from the earlier career. `returner`: a career gap. `non_linear`: lateral moves, short stints. `two_roles`: the candidate could search two different professions |

## Rules for each persona

1. **Fictional and consistent.** Invented name, `example.com` email, phone `+<country code> ... 0000 <n>`.
   Employers are invented (plausible names for the country and industry). At most one well-known
   employer per persona, only when it makes sense for the level. Dates, degrees and years add up.
2. **Evidence like a real CV.** Mixed bullets: some with a measured result, many without. Tools, standards
   and terms of the profession in the CV's language. Do not write a CV that repeats the job title as its
   skills list; real people don't.
3. **Searches.** `searches` has `primary` (the role the person would type), `adjacent` (a neighbouring
   title) and `open` (empty roles, the person typed nothing). Use titles as typed in that country; mix
   English and local terms when that is realistic (German users often type English titles).
   `cross_check_roles`: one role from a different profession, as in the examples.
4. **Variety within the matrix.** Names, industries, employer sizes, universities and layouts differ across
   personas. Do not reuse a persona's content. Vary `layout` among `classic`, `sidebar`, `dense`.
5. **Length.** 2 to 4 experience entries (interns 1 to 2), 3 to 5 bullets for the latest, 1 to 3 for older.

## Work in batches and check yourself

After every 25 files run `python3 validate.py` (it checks keys, language, uniqueness and that every row of
the matrix has a file). Fix what it reports. Commit each batch to the branch you are on with the message
`personas: batch <n> (<first slug> .. <last slug>)`. When all 266 pass, push the branch and stop.
You may use subagents for batches if that is faster; the validator is the arbiter.

## Do not

- touch `matrix.csv`, `validate.py` or `examples/`;
- include real people, real contact details, or anything secret;
- write anything outside `personas/`.
