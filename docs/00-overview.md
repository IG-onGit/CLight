# CLight — Technical Overview

**Version**: 2.4.14
**Language**: Python 3
**Entry point**: `clight` console script → `clight.system.main:main`

CLight is a Python framework and command-line tool that scaffolds, manages, and publishes other Python CLI applications ("projects" or "modules") to PyPI. It provides:

- A project generator (`clight new`) that creates a ready-to-run CLI skeleton
- A shared runtime library (the `cli` class) that generated projects import for I/O, prompts, sound, speech, encryption, file helpers, etc.
- A catalog system that registers every generated project as its own global CMD alias (a `.bat` file on the system `PATH`)
- A packaging/publish pipeline that builds a `setup.py`-based distribution and uploads it to PyPI, either locally or via CI (GitHub Actions / GitLab CI)
- Semantic version bumping with pre-release stage support (alpha/beta/rc)

## How the pieces fit together

```
User runs `clight <command>` in CMD
        │
        ▼
clight.system.main.main  (installed as console_script "clight")
        │
        ├─ if invoked in a project folder (or via the project's own .bat alias)
        │     → loads that project's .system/index.py and dispatches the sub-command
        │
        └─ otherwise → runs one of CLight's own commands (new, module, reform, version,
              all, publish, remove, install, update, uninstall, pypidel, execute, deploy)
```

Every project created by `clight new` gets:
1. A skeleton copied from `clight/skeleton/` into the project folder
2. A registered `.bat` file in `%USERPROFILE%\.clight\<CMD>.bat` that forwards to `clight execute "<path to index.py>" %*`
3. A `.system/sources/clight.json` config file holding the answers from the creation form (Name, Version, CMD, Author, Mail, Project Type, Repository Type, License, Operating System, Link, Description)

This means **every generated project's CMD alias is just a thin wrapper that calls back into CLight's `execute` command**, which loads the project's own `index.py` and routes to the requested sub-command dynamically.

## Documentation index

- [Architecture](01-architecture.md) — module layout, execution flow, the catalog/registration mechanism
- [CLI Command Reference](02-cli-commands.md) — every `clight` command, arguments, and behavior
- [Project Skeleton & Generated Projects](03-project-skeleton.md) — what `clight new` produces and how a generated project runs
- [The `cli` Runtime API](04-cli-api.md) — full reference for the shared helper class importable by generated projects
- [Semantic Versioning (`SemVer`)](05-semver.md) — version bump rules, pre-release stages, and the umbrella version algorithm
- [Packaging & Publishing](06-packaging-and-publishing.md) — how `install`/`publish`/`deploy` assemble a distributable package and ship it to PyPI
- [CI/CD Integration](07-ci-cd.md) — GitHub Actions and GitLab CI templates used by generated projects
