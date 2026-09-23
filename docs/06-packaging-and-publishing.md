# Packaging & Publishing

`clight install`, `clight publish`, and `clight deploy` all share the same package-assembly pipeline, differing only in what happens after the package is assembled. This document covers `main.py`'s helper methods that do the heavy lifting.

## Staging area

All three commands use `clight/package/` (inside the installed CLight package itself) as a scratch/staging directory:

1. `__clearFolder(package)` — wipes it clean (keeps `.placeholder` if present).
2. Creates `package/<CMD>/`.
3. `__cloneSkeleton(project, package/<CMD>, skip=["\\.github\\", "\\.gitlab-ci.yml"])` — copies the **entire real project directory** (not the CLight skeleton template — the user's actual project source) into the staging folder, excluding `.git`, `vendor`, `__pycache__`, `.TODO` files, `desktop.ini`, and (always) `.github`/`.gitlab-ci.yml` CI config.
4. `__rebasePackage` — moves `.gitignore`, `LICENSE`, and `README.md` up from `package/<CMD>/` to `package/` (the actual `setup.py`-relative root), rewriting `.gitignore` lines to be prefixed with `<CMD>/` so they still apply correctly at the new nesting level.
5. `__preparePackage` — the core packaging step (below).
6. `os.chdir(package)` then the command-specific build/upload step runs.
7. `__clearFolder(package)` again to clean up afterward.

## `__preparePackage`

Given the staged `package/<CMD>/` folder:

1. Renders `__init__.py` and `main.py` from the `system/sources/` templates into the package root (`{{...}}` placeholders filled from `self.params`, i.e. the project's `clight.json`).
2. **Dependency auto-detection** (`__collectModules`): parses `.system/imports.py` with a regex (`import\s+(\S+)|from\s+(\S+)\s+import`), skipping lines containing `!install` markers on the initial pass, then for each imported top-level module name:
   - Skips anything containing `"clight"` (it's an implicit dependency, always added directly in the `setup.py` template).
   - Skips it if a same-named folder exists inside `.system/` (implies it's a local module, not a pip package).
   - Skips it if it's a Python builtin/stdlib module (computed via `pkgutil.iter_modules` over `sysconfig.get_paths()["stdlib"]`, plus `builtins.__dict__` and `sys.builtin_module_names`).
   - Skips `"yaml"` specifically (bundled as a `clight` dependency already, via PyYAML).
   - Everything else becomes a quoted entry for `setup.py`'s `install_requires` list.
3. **File manifest** (`__collectFiles`): walks the entire staged package directory and lists every file's relative path (for `package_data` in `setup.py`), so non-`.py` resources (icons, wav files, etc.) ship inside the wheel/sdist. For **Module**-type projects, `.system/` path segments are rewritten to `__system__/` to match the renaming that happens next.
4. Detects README presence (`__detectReadme`) → sets `long_description`/`long_description_content_type` lines.
5. Detects license type from the `LICENSE` file's first line (`__detectLicense`), matching it against the list of bundled license names, producing a PyPI `License :: OSI Approved :: <Name>` classifier (or `"Undefined"` if no match).
6. Sets the `Operating System ::` classifier from `self.params["Operating System"]` (`__detectSystem`, replacing `/` with `::`).
7. Renders `setup.py` from the `system/sources/setup.py` template with all the above filled in.
8. If `Project Type == "Module"`, calls `__renderModule` (see [Architecture](01-architecture.md#distinguishing-app-vs-module-project-types) for the import-path rewriting and `.system` → `__system__` rename it performs).

## Command-specific behavior after staging

| Command | Behavior |
|---|---|
| `clight install` | `pip install .` against the staged package. Local test only — never touches PyPI. |
| `clight publish` (no flag) | If `Repository Type != "Local"`, **refuses** and tells the user it'll publish automatically via CI on push. If `Repository Type == "Local"`, prompts for/reuses PyPI credentials, runs `pip install setuptools wheel twine`, `python setup.py sdist bdist_wheel`, then `twine upload dist/* -u <user> -p <token> --verbose`. |
| `clight publish -t` | Same staging, but just `pip install .` locally (equivalent to `install`, ignoring `Repository Type`). |
| `clight deploy <user> <token>` | Same build steps as `publish`'s Local path, but credentials are passed as arguments (no prompts, no saved-credential flow) — this is what the GitHub/GitLab CI templates invoke. |

## Local PyPI credential storage

`__getCredentials()`:
- If `clight/system/sources/.pypi` exists, prompts only for the **Password Key**, decrypts the stored JSON (`{"username": ..., "token": ...}`) via `cli.decrypt`, and returns it.
- Otherwise prompts for `PYPI_USERNAME` and `PYPI_API_TOKEN` directly, then asks whether to save them. If yes, prompts for a Password Key and writes the encrypted blob (via `cli.encrypt`) to `.pypi`.
- `clight pypidel` removes this saved file, forcing credentials to be re-entered (and optionally re-saved) next time.

This is a **process-argument-based** credential flow for `twine` (`-u`/`-p` flags) — be aware credentials passed this way can be visible in process listings on shared/multi-user machines.

## Version bump requirement

Per PyPI rules (a given version number can only be uploaded once), the project's version must be incremented before each publish — `clight version` handles this (see [SemVer](05-semver.md)). Nothing in the publish/deploy pipeline itself checks or enforces this; attempting to re-upload an existing version will simply fail at the `twine upload` step.
