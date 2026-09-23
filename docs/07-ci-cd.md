# CI/CD Integration

When a generated project's **Repository Type** is `GitHub` or `GitLab`, CLight copies a ready-made CI pipeline into the project that automatically publishes to PyPI on every push to `main`, calling `clight deploy` non-interactively.

## GitHub Actions (`.github/workflows/publish.yml`)

Copied from `clight/system/sources/.github/workflows/publish.yml`.

```yaml
name: Publish to PyPI

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  Deploy:
    if: |
      github.ref == 'refs/heads/main' &&
      !contains(github.event.head_commit.message, '[!deploy]')
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: |
          python -m pip install --upgrade pip
          python -m pip install clight
          clight help
      - run: |
          clight deploy "${{ secrets.PYPI_USERNAME }}" "${{ secrets.PYPI_API_TOKEN }}"
          exit 0
        env:
          PYPI_USERNAME: ${{ secrets.PYPI_USERNAME }}
          PYPI_API_TOKEN: ${{ secrets.PYPI_API_TOKEN }}
```

Key points:
- Runs on `windows-latest` (CLight's own environment/registry logic is Windows-oriented — see `__loadEnvironment` in [Architecture](01-architecture.md)).
- Triggered on push to `main`, or manually via `workflow_dispatch`.
- **Skip mechanism**: a commit message containing `[!deploy]` prevents the job from running — useful for doc-only or non-release commits.
- Installs `clight` itself fresh from PyPI, then calls `clight deploy` with the two required PyPI repo secrets.
- `exit 0` after deploy ensures the step (and job) reports success even if `twine upload` prints warnings to stderr.
- Also copies `.github/labels.yml` (issue label definitions: `bug`, `enhancement`, `question` — not consumed by any workflow directly, just a convenience template for repo setup).

**Required repo secrets**: `PYPI_USERNAME`, `PYPI_API_TOKEN` (must be added manually under repo Settings → Secrets).

## GitLab CI (`.gitlab-ci.yml`)

Copied from `clight/system/sources/.gitlab-ci.yml`.

```yaml
stages:
  - deploy

deploy:
  stage: deploy
  image: python:3.9
  script:
    - python -m pip install --upgrade pip
    - python -m pip install clight
    - clight deploy "$PYPI_USERNAME" "$PYPI_API_TOKEN" || true
    - exit 0
  only:
    - main
  variables:
    PYPI_USERNAME: $PYPI_USERNAME
    PYPI_API_TOKEN: $PYPI_API_TOKEN
```

- Runs on the `python:3.9` Docker image, only on pushes to `main`.
- `|| true` plus `exit 0` similarly force the job to succeed regardless of the deploy step's own exit code.
- **Required CI/CD variables**: `PYPI_USERNAME`, `PYPI_API_TOKEN` (added under repo Settings → CI/CD → Variables, ideally masked/protected).

## Switching or removing CI

Changing **Repository Type** via `clight reform` automatically swaps these files: switching to `Local` removes any existing `.github/` folder or `.gitlab-ci.yml`; switching between `GitHub`/`GitLab` removes the old type's files before adding the new type's (`main.__addRepositoryType`, see [Architecture](01-architecture.md)).

## Relationship to `clight publish`

With a non-`Local` Repository Type, `clight publish` run locally **refuses to upload** and just informs the user that pushing to `main` will trigger the CI deploy instead — the local/CI paths are mutually exclusive by design, preventing double-publishing the same version.
