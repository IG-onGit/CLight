# CLI Command Reference

All commands are methods on `clight.system.main.main`, invoked as `clight <command> [args...]`. Running `clight` with no arguments (or `clight help`) lists commands with their inline `# comment` description, auto-extracted from source.

## `clight new`

Create a new project in the current (empty) directory.

- Fails if `.system/sources/clight.json` already exists in the CWD ("Project already exists!").
- Prompts an interactive form (via `inquirer`) for: **Name, Version, Description, Link, CMD, Author, Mail, Project Type** (App/Module), **Repository Type** (Local/GitHub/GitLab), **License** (one of 8, optional), **Operating System**. Fields prefixed `!` in the internal `__inputs()` map are required.
- Writes the answers to `.system/sources/clight.json`.
- Normalizes `CMD` by replacing `-` with `_`.
- Registers the project's `.bat` alias in the catalog (`{{CMD}}.bat` template).
- Copies the entire `clight/skeleton/` tree into the project directory.
- Renders `README.md` from the CLight-side template, injecting the auto-generated `## Commands` section (from `index.py`'s docstring comments).
- If a License was chosen, renders that license file to `LICENSE` in the project root.
- Adds Repository Type scaffolding (see below).

## `clight add`

Register an **existing** project folder (with a valid `.system/index.py` and `.system/sources/clight.json`) into the catalog, without recreating any skeleton files. Fails if the index file or config is missing/invalid, or if a project with the same CMD is already registered.

## `clight module <name>`

Create a new custom module file at `.system/modules/<name, lowercased first letter>.py`, rendered from the `{{module}}.py` template (class name = `name` as given). Requires an existing project (`clight.json` present) and a non-empty `name`. Fails if the module file already exists.

## `clight reform (-t)`

Re-run the creation form to edit an existing project's params (all fields except `CMD` and `Project Type`, which are immutable after creation). For `License`, an extra `"Remove"` option is offered.

- Writes updated `clight.json`.
- Unless `-t` is passed, also regenerates `README.md` and re-adds/removes the `LICENSE` file and Repository Type scaffolding to match the new answers.
- `-t` skips template regeneration and only persists the param changes.

## `clight version (number)`

Bump or set the project's semantic version.

- With no argument: interactively bumps via [`SemVer.bump`](05-semver.md) (asks change type — patch/minor/major — and, for a first major-with-no-tag release, optionally a pre-release stage).
- With an explicit `number` argument: validates it against SemVer format and sets it directly (fails if it equals the current version or is invalid).
- Updates `Version` in `clight.json` and rewrites any `v<old>` / `**Version**: <old>` occurrences in the project's `README.md` to the new version.

## `clight all`

Lists every registered project's CMD name, one per line, by reading the catalog folder.

## `clight install`

Locally builds and `pip install`s the current project **without publishing**, useful for testing the packaging output. Stages a fresh build in `clight/package/` (see [Packaging & Publishing](06-packaging-and-publishing.md)), runs `pip install .` against it, then clears the staging folder.

## `clight update`

Convenience wrapper: `uninstall()` → sleep 5s → `install()`. Used to refresh a local test install after code changes.

## `clight uninstall`

Runs `pip uninstall -y <CMD>` for the current project.

## `clight publish (-t)`

Builds the distributable package the same way as `install`, then:

- `-t` (test flag): just `pip install .` locally (same effect as `install`, without clearing steps skipped).
- Repository Type ≠ `"Local"`: refuses to publish directly — "Project will be published when changes are pushed to `<type>`!" (CI handles it — see [CI/CD Integration](07-ci-cd.md)).
- Repository Type == `"Local"`: prompts for (or reuses saved, encrypted) PyPI credentials, then runs `setup.py sdist bdist_wheel` and `twine upload`.

## `clight remove <project>`

Removes a project from the catalog: deletes its `.bat` alias and its `clight.json` config. **Does not delete the project's source directory** — this only unregisters it.

## `clight pypidel`

Deletes the saved, encrypted local PyPI credentials file (`clight/system/sources/.pypi`), if one exists.

## `clight execute <index-path> [cmd] [args...]`

Internal command, invoked by a registered project's `.bat` alias (not meant to be typed by end users directly, though it can be). Loads and runs the target project's `index.py`, dispatching `cmd` the same way CLight dispatches its own commands. See [Architecture](01-architecture.md) for the full mechanism.

## `clight deploy <username> <token>`

Non-interactive publish path used by CI (GitHub Actions / GitLab CI templates call this with secrets injected as arguments). Builds the package the same way as `publish`, then uploads directly via `twine` using the given PyPI username/token — no prompts, no saved-credential flow.

## Help output

`clight` (no args) or `clight help` prints every public method (not prefixed `_`) found in the target file (CLight's own `main.py`, or a project's `index.py` under `execute`), paired with the inline comment following the `def` line. This is also what populates the `## Commands` section of a generated project's `README.md`.
