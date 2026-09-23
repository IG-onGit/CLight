# Semantic Versioning (`SemVer`)

`clight.system.modules.semver.SemVer` implements version validation, interactive/programmatic bumping, and a multi-project "umbrella" version aggregator. Used by `clight version`.

## Version format

```
MAJOR.MINOR.PATCH[-<alpha|beta|rc>.N]
```

Validated by `SemVer.valid(version)` using a strict regex:
- No leading zeros in numeric segments (`01.2.3` is invalid).
- Pre-release label must be exactly `alpha`, `beta`, or `rc`, optionally followed by dot-separated numeric segments, OR a `build.<alphanumeric>` metadata suffix (though `SemVer.bump`'s own parsing only recognizes the `alpha|beta|rc` shape — see caveat below).

## `SemVer.bump(current, action=None)`

Two modes:

- **Interactive** (`action=None`, the default when called from `clight version` with no explicit number): prompts the user.
  1. If `current` already has a pre-release tag, first asks (`cli.confirmation`) whether to **promote** it to the next stage (`alpha → beta → rc → stable`). If confirmed, returns the promoted version immediately (patch/minor/major untouched, just the label changes or is dropped).
  2. Otherwise asks what kind of change this is: **Patch**, **Minor**, or **Major** (`__askChangeType`, mapped to `patch`/`minor`/`major`).
  3. If it's a **Major** bump on a currently-stable (no tag) version, additionally asks what **stage** to release as (`__askStage`): Stable, Alpha, Beta, or RC — attaching `-alpha.1`/`-beta.1`/`-rc.1` as needed.
- **Programmatic** (`action` given, e.g. `"patch"`/`"minor"`/`"major"`): skips all prompts, used by the test suite (`test_bump`).

Bump rules once the action is known:
- **Has an existing pre-release tag** (`__bumpTag`):
  - `patch` → increments the pre-release number only (`1.0.0-alpha.1` → `1.0.0-alpha.2`).
  - `minor`/`major` → bumps the respective numeric segment (resetting lower segments to 0) and **resets to `-<default_tag>.1`** (default tag is `"alpha"`).
- **No pre-release tag** (`__bumpNumber`): standard patch/minor/major increment with the usual carry-reset behavior (minor bump resets patch to 0; major bump resets minor and patch to 0).

Returns `""` (and logs an error) if `current` fails `SemVer.valid()`, or if `action` isn't one of `patch`/`minor`/`major`.

## `SemVer.valid(version)`

Standalone strict-format checker described above. `clight version <number>` uses this to reject a manually supplied version string before accepting it.

## `SemVer.umbrella(old_version, old_versions, new_versions)`

Computes a single aggregate version bump for a "parent"/umbrella package given the before/after versions of its N sub-packages (dependencies). Used when one release needs to reflect the combined significance of several component version bumps.

Algorithm:
1. For each sub-package, parse old/new versions and classify the change severity via `__bumpSeverity`:
   - **3 (major)** — new version's major number increased (and it's not a pre-release).
   - **2 (minor)** — minor number increased.
   - **1 (patch)** — patch number increased, OR a pre-release label/number advanced, OR a pre-release was **removed** (promoted to stable).
   - **0** — no relevant change.
2. Take the **highest severity across all sub-packages** and apply that to the umbrella version (major bump resets minor/patch to 0, etc. — same carry rules as `__bumpNumber`).
3. Separately, collect every sub-package's **new pre-release label/number** (if any). If any exist, pick the "best" one by precedence (`alpha=1 < beta=2 < rc=3`, ties broken by highest number) and attach it to the umbrella version as `-<label>.<number>`.
4. If no sub-package ended up with a pre-release tag, the umbrella version is fully stable.

This lets a monorepo-style umbrella package's version reflect "the most significant change among all its parts," while still surfacing the most advanced pre-release stage if any part is still in alpha/beta/rc.

## Built-in self-tests

`SemVer.test_check()`, `SemVer.test_bump()`, and `SemVer.test_umbrella()` are not registered as `clight` commands (they're not on `main`), but can be invoked directly, e.g. via a Python REPL or a debug script:

```python
from clight.system.modules.semver import SemVer
SemVer.test_check()   # validates SemVer.valid() against a table of known-good/bad version strings
SemVer.test_bump()    # validates SemVer.bump() against expected outputs for many scenarios
SemVer.test_umbrella() # validates SemVer.umbrella() against 20 multi-package aggregation scenarios
```

Each prints a pass/fail table (mismatches printed in default color/unmarked, matches in green via `cli.done`) and calls `sys.exit()` at the end.
