# VERIFICATION

- Run `python3 scripts/build_catalog.py --check` to detect missing or stale catalog content.
- Run `python3 -m unittest discover -s tests -v` for negative and positive registry tests.
- Run `python3 scripts/build_catalog.py` after editing skill directories to regenerate the catalog.
- UPR checker (if installed separately): `python scripts/upr.py check PATH --strict`. This is structural only, not software correctness or publication authorization.
- Manual checks remain required: provenance, data rights, secrets, dependency safety and owner publication approval.
