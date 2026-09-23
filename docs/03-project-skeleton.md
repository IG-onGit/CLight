# Project Skeleton & Generated Projects

## What `clight new` produces

Running `clight new` in an empty folder clones `clight/skeleton/` and adds a few rendered files:

```
<project-root>/
├── .gitignore                  (from skeleton, contains __pycache__)
├── README.md                   (rendered from system/sources/README.md template)
├── LICENSE                     (rendered from clight/licenses/<chosen>, if a license was picked)
├── .github/ or .gitlab-ci.yml  (added if Repository Type is GitHub/GitLab — see below)
└── .system/
    ├── imports.py              from imports import cli  # central import file
    ├── index.py                CLI command definitions — this is your app's surface
    ├── modules/
    │   └── jobs.py             example custom module (index.py's demo command calls jobs.test())
    ├── sources/
    │   ├── logo.ico
    │   └── clight.json         written directly by `new`, not copied from skeleton
```

## `.system/index.py` — the command surface

```python
from imports import *


class index:
    def __init__(self, app="", cwd="", args=[]):
        self.app, self.cwd, self.args = app, cwd, args
        pass

    def __exit__(self):
        pass

    def demo(self, param=""):  # (param) - Test demo method with param
        if not param:
            return "Invalid param!"
        cli.hint(param)
        return self.__helper()

    def __helper(self):
        return jobs.test()
```

- **`__init__(self, app, cwd, args)`** — called once per invocation by `main.execute()`. `app` is the project root path, `cwd` is the directory the user ran the command from, `args` is any extra `sys.argv` beyond the command name (rarely needed since each public method receives its own args as positional parameters).
- **`__exit__(self)`** — optional; if present, called when the process receives `SIGINT`/`SIGTERM` (Ctrl+C), letting you clean up before exit.
- **Public methods** (not prefixed `_`) become CLI sub-commands, e.g. `demo` → `<cmd> demo <param>`. The trailing `# (param) - description` comment is required for the auto-generated help text and for the project's `README.md` `## Commands` section (rendered at `new`/`reform` time).
- **Return convention**: return a string ending in `!` for an error (printed red), any other non-empty string for success (printed green), or nothing if you already printed your own output via `cli`.
- Methods prefixed with `__` (name-mangled private) are helpers, not exposed as commands — matches the **Load / Main / Helpers** three-section convention CLight itself uses throughout its own code.

## `.system/imports.py` — centralized imports

```python
from clight.system.importer import cli  # DON'T REMOVE THIS LINE

import os
import sys
from modules.jobs import jobs
```

Every pip package and custom module your project needs should be imported **only here**. `index.py` and every custom module then do `from imports import *`, giving them all the same names without repeating import statements. This convention is what lets CLight auto-detect your project's third-party dependencies when packaging (see [Packaging & Publishing](06-packaging-and-publishing.md)) — it parses this file's `import`/`from ... import` statements with a regex, filters out stdlib/builtin names and `clight` itself, and feeds the remainder into `setup.py`'s `install_requires`.

Special directives, both are comments parsed at package-build time only (they don't affect runtime):
- `# import <module>==<major:minor:patch>` — pins an exact version for a module imported normally below it.
- `# import <name>` + `# !install` at the end of the actual import line — for cases where the pip package name differs from the importable module name (e.g. `soupsieve` pip package vs. `from bs4 import BeautifulSoup`). The commented name is what gets added to `install_requires`; the `!install` marker on the real import line is stripped by `__collectModules` before dependency parsing, but signals "resolve the pip name from the comment above, not from this import statement."

## `.system/modules/*.py` — custom modules

Created via `clight module <name>`, rendered from the `{{module}}.py` template:

```python
from imports import *


class {{module}}:
    def __init__(self):
        pass

    def test():
        obj = {{module}}()
        val = obj.__helper()
        return val

    def __helper(self):
        return "{{module}}.helper"
```

Import them into `imports.py` as `from modules.<name> import <ClassName>` and they become available everywhere via `from imports import *`.

## Repository Type scaffolding

Set at creation (or changed via `reform`), controls what deployment automation is added to the project root:

- **Local** — no CI files; `clight publish` runs `twine upload` from your machine using saved/prompted PyPI credentials.
- **GitHub** — copies `.github/labels.yml` and `.github/workflows/publish.yml` into the project. The workflow triggers on push to `main` (unless the commit message contains `[!deploy]`) and calls `clight deploy` with `PYPI_USERNAME`/`PYPI_API_TOKEN` repo secrets.
- **GitLab** — copies `.gitlab-ci.yml`, same trigger/secrets pattern via `clight deploy`.

Switching Repository Type via `reform` removes the previous type's files before adding the new type's (or none, for Local).

## Running a generated project

Once registered (via `new` or `add`), the project's `CMD` becomes a global shell command (after restarting CMD once, so the catalog folder is picked up on `PATH`). Typing `<cmd>` with no arguments prints the same auto-generated help list `clight` uses for its own commands. Typing `<cmd> demo hello` runs `index.demo(self, "hello")`.

Internally this works because the registered `.bat` file is just:

```bat
@echo off
clight execute "<absolute path>/.system/index.py" %*
```

— see [Architecture](01-architecture.md) for the full dispatch chain.
