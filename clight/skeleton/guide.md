# Building on this CLight skeleton

This project was created by `clight new` and is a **CLight** CLI application skeleton. This file explains how the skeleton works and how to build your CLI commands on top of it.

## How this project runs

Your project doesn't run standalone with `python something.py`. Instead:

- `clight new` registered a global shell command for you, using the **CMD** name was chosen during setup (e.g. `myapp`).
- `clight` loads `.system/imports.py`, then `.system/index.py`, instantiates the `index` class, and dispatches whatever sub-command and arguments you typed.

So `myapp demo hello` finds the `demo` method on the `index` class in `.system/index.py` and calls it as `demo(self, "hello")`.

**To test project after editing it**, just run your CMD alias, e.g. `myapp`, `myapp demo hello`, etc. No build step, no `python` invocation needed — just type your command directly.

## Folder structure

```
<project-root>/
├── .system/
│   ├── imports.py         ← ALL your imports go here (pip packages + your own modules)
│   ├── index.py            ← Your CLI commands live here — this is the surface users interact with
│   ├── modules/             ← Your custom modules/classes, one file per module
│   │   └── jobs.py          ← Example module included in the skeleton
│   └── sources/              ← Non-code resources (icons, data files, templates, etc.)
├── .gitignore
├── README.md                ← Auto-generated; its "## Commands" section is regenerated from index.py
└── (LICENSE, .github/ or .gitlab-ci.yml — depending on choices made in `clight new`)
```

Do not rename or remove `.system`, `.system/modules`, `.system/sources`, `.system/imports.py`, or `.system/index.py` — CLight's packaging and dispatch logic depends on these exact names and locations.

## `.system/index.py` — where your commands live

This is the only file CLight actually dispatches to. Every **public** method you add here becomes a CLI sub-command automatically — there is no separate command registration step.

```python
from imports import *


class index:
    ####################################################################################// Load
    def __init__(self, app="", cwd="", args=[]):
        self.app, self.cwd, self.args = app, cwd, args
        # runs once per invocation, before your command executes
        pass

    def __exit__(self):
        # optional — runs on Ctrl+C (SIGINT/SIGTERM), use it to clean up if needed
        pass

    ####################################################################################// Main
    def demo(self, param=""):  # (param) - Test demo method with param
        if not param:
            return "Invalid param!"

        cli.hint(param)

        return self.__helper()

    ####################################################################################// Helpers
    def __helper(self):
        return jobs.test()
```

Rules to follow when adding commands:

- **Public method = CLI command.** `def deploy(self, target=""):` becomes `<cmd> deploy <target>`. Method arguments map positionally to CLI arguments and always arrive as strings — validate/convert as needed.
- **Always add a trailing `# comment` on the `def` line**, in the form `# (args) - Description`. This is not optional decoration — it's parsed by CLight to build the `<cmd>` help list and the `README.md` `## Commands` section. Follow the existing `demo` method as the format example.
- **Return value convention** (do not `print()` your final result — `return` it):
  - Return a string ending in `!` → printed as an error (red).
  - Return any other non-empty string → printed as success (green).
  - Return nothing/`None` → use this when your command already printed its own output via `cli.*` methods (progress, prompts, multiple info lines, etc.).
- **Private/helper methods** should be prefixed with `__` (e.g. `__helper`). These are never exposed as commands, so use them freely for logic you don't want callable directly.
- Keep the **Load / Main / Helpers** section structure (the `#####...// Section` comments) — it's the convention used throughout CLight itself and keeps generated projects consistent and easy to navigate.
- `self.app` = project root path, `self.cwd` = the directory the user ran the command from (these are often different — use `self.cwd` for anything relative to where the user is standing).

## `.system/imports.py` — the single place for all imports

```python
from clight.system.importer import cli  # DON'T REMOVE THIS LINE

import os
import sys
from modules.jobs import jobs
```

**Every pip package and every one of your own modules must be imported here, and only here.** `index.py` and every custom module then start with `from imports import *`, which pulls in everything declared in this file — you never repeat an import elsewhere.

This matters beyond convenience: when the project is packaged for PyPI (`clight install` / `clight publish` / `clight deploy`), CLight scans this exact file to auto-detect your third-party dependencies and populate `setup.py`'s `install_requires`. If a package is imported anywhere other than here, it will be missed and your published package will be broken for other users.

Special cases:

- **Pinning a version**: comment it above the real import, `# import <module>==<major:minor:patch>`, then import normally below.
  ```python
  # import openai==0:28
  import openai
  ```
- **pip package name differs from the importable module name** (e.g. installing `soupsieve` but importing `bs4`): add a commented line with the pip name, and mark the actual import line with `# !install`.
  ```python
  # import soupsieve
  from bs4 import BeautifulSoup  # !install
  ```

## `.system/modules/` — your custom modules

Don't hand-write module files — generate them with:

```
clight module <Name>
```

This creates `.system/modules/<name>.py` (lowercased first letter) from a template:

```python
from imports import *


class Name:
    def __init__(self):
        pass

    def test():
        obj = Name()
        val = obj.__helper()
        return val

    def __helper(self):
        return "Name.helper"
```

After generating it, wire it in by adding an import to `.system/imports.py` (e.g. `from modules.name import Name`), then it's available anywhere via `from imports import *` — including inside `index.py`. Use modules to group related logic (API clients, data processing, integrations) out of `index.py`, keeping your command methods thin.

The skeleton ships with one example module, `.system/modules/jobs.py`, which `index.demo()` calls as `jobs.test()` — a working reference for the pattern.

## `.system/sources/` — bundled resources

Put non-Python resources here (icons, data files, templates, static assets). This folder is automatically included in the packaged distribution when you publish, so anything your code needs to `cli.read()` or load at runtime at a fixed relative path should live here, not scattered elsewhere in the project.

## The shared `cli` helper

Every file that does `from imports import *` has access to the `cli` class — CLight's shared utility library. Use it instead of raw `print()`/`input()`/`open()` so your CLI behaves consistently (colors, prompts, sound, etc.):

- Output: `cli.info()`, `cli.done()`, `cli.hint()`, `cli.error()`, `cli.trace()` (dev-only, enable with `cli.dev = True`)
- Prompts: `cli.input()`, `cli.selection()`, `cli.selections()`, `cli.confirmation()`
- Files: `cli.read()`, `cli.write()`, `cli.append()`, `cli.yaml()`, `cli.template()`
- Checks: `cli.isValue()`, `cli.isPath()`, `cli.isFile()`, `cli.isFolder()`
- Process: `cli.command()`, `cli.execute()`
- Misc: `cli.chars()`, `cli.sound()`, `cli.speak()`, `cli.listen()`, `cli.encrypt()`/`cli.decrypt()`, `cli.filter()`
- Progress/spinner: `cli.setProgress()`/`cli.addProgress()`/`cli.endProgress()`, `cli.setLoading()`/`cli.endLoading()`

Full signatures and behavior are documented in the CLight repository's `docs/04-cli-api.md`.

## Typical workflow for adding a feature

1. If you need new logic grouped together, run `clight module <Name>` and import it in `.system/imports.py`.
2. Add a public method to `.system/index.py` for each new command, following the return-value and comment conventions above.
3. Use `cli.*` helpers for all I/O instead of built-ins.
4. Run your CMD alias directly in CMD to test (e.g. `myapp yourcommand arg1`).

## Things not to do

- Don't rename `index.py`, `imports.py`, the `modules/` or `sources/` folders — CLight's dispatch and packaging code depends on these exact paths.
- Don't import pip packages anywhere except `.system/imports.py` — they won't be detected for packaging.
- Don't `print()` command results directly in `index.py` methods when a `return` value would do — return values get the right color automatically.
- Don't remove the `# comment` from a command method's `def` line — it breaks the auto-generated help and README.
