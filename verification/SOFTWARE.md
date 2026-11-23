# SOFTWARE VERIFICATION

**Scope:** Local Python catalog generator/validator with no network actions or external package dependencies.

**Unit and negative tests:** `python3 -m unittest discover -s tests -v`.
**Consistency:** `python3 scripts/build_catalog.py --check`.
**Privacy review:** Manual audit of staged files and Git history before public pushes.
**Build/deployment:** Static repo only; no live service or runtime endpoint.
**Recovery:** Revert faulty commit/PR and regenerate catalog from known good skill files; no database migrations.
**Evidence:** Only actual executed command and output may be reported as PASS. Running CI is not the same as enforcing branch protection.
