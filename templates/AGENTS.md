# AGENTS.md — <PROJECT_NAME>

<!-- Template source: CloudCrane-Software/.github templates/AGENTS.md
     Instantiate per repo: replace <PROJECT_NAME>, adjust the map and commands.
     This file is a MAP, not a manual. Keep it under 400 lines. -->

One sentence: <ONE_SENTENCE_WHAT_THIS_REPO_IS>.

## Directory map

```
<path>/     <what lives here, one line each — no essays>
```

## Build & test commands

```bash
uv sync                    # install pinned deps from uv.lock
uv run pytest              # full test suite (testcontainers services are started by tests)
uv run pytest -m "not integration"   # fast unit-only pass
uv run ruff check .        # lint
uv run ruff format --check .         # formatting gate
uv run mypy kernel gateway reconciler  # type gate (strict on new modules)
```

## Code conventions

- Python 3.12, dependency management via `uv` only; `uv.lock` is committed and authoritative.
- Lint/format: ruff; types: mypy (new modules strict); tests: pytest.
- Commits: Conventional Commits, English (`feat:` `fix:` `chore:` `eval:` `docs:`).
- Infrastructure config: YAML (compose / workflows / OPA bundle data), Rego (OPA policies
  only), SQL (DDL/migrations only). Any language exception requires an ADR under
  `docs/adr/`.

## Prohibitions (each rule has an executable checkpoint)

1. Never modify eval thresholds or eval suites together with product code.
   Checkpoint: CI guard workflow fails a PR that touches both (`.github/workflows/guard.yml`).
2. Never put secrets in code, config, logs or git history.
   Checkpoint: `uv run pytest tests/test_no_secrets.py` (pattern scan) + pre-commit `detect-secrets` hook.
3. Never push directly to `main`; all changes go through PR.
   Checkpoint: branch protection (required PR + status checks + no force push).
4. Never bypass the action gateway for external side effects; never treat UNKNOWN as a
   terminal state; never cache an ALLOW decision.
   Checkpoint: `uv run pytest tests/test_architecture_guards.py` (static guards).
5. Never weaken or delete a CHECK constraint / trigger in the DDL.
   Checkpoint: `uv run pytest tests/test_db_invariants.py` (P-3 / P-4 / F-2 / append-only).

## Working rules for agents

- Read this file before doing anything in this repo.
- Human instructions arrive as work-order files, never verbal. Do not expand scope
  beyond the work order; on unclear or blocked conditions, stop and report.
- Every non-trivial change ships with tests that would fail without the change.
- If a change touches eval assets in any way, split it: code PR first, eval PR second
  (or the reverse), never both in one PR.
