# Architecture

## Package layout

```
clight/
├── __init__.py                     (empty — marks package root)
├── licenses/                       8 OSI license templates, selected by name during `new`/`reform`
│   ├── Apache Software License
│   ├── BSD License
│   ├── GNU Affero General Public License v3
│   ├── GNU General Public License v3 (GPLv3)
│   ├── GNU Lesser General Public License v3 (LGPLv3)
│   ├── ISC License (ISCL)
│   ├── MIT License
│   └── Mozilla Public License 2.0 (MPL 2.0)
├── package/
│   └── .placeholder                Working directory used as a build/staging area during install/publish/deploy
├── skeleton/                       Template copied into every new project by `clight new`
│   ├── .gitignore
│   └── .system/
│       ├── imports.py              Central import file for the generated project
│       ├── index.py                Default CLI command definitions (starts with a `demo` command)
│       ├── modules/jobs.py         Example custom module
│       └── sources/logo.ico
└── system/                         CLight's own implementation
    ├── main.py                     The `main` class — CLight's command dispatcher and entry point
    ├── importer.py                 Central import file for CLight itself (mirrors the generated-project pattern)
    ├── modules/
    │   ├── cli.py                  Shared static-method utility class, importable by every generated project
    │   └── semver.py               Semantic version parsing/bumping logic
    └── sources/                    Templates and resources rendered into new/published projects
        ├── {{CMD}}.bat             Template for a project's registered CMD alias
        ├── {{module}}.py           Template for `clight module <name>`
        ├── __init__.py             Rendered into the final PyPI package
        ├── main.py                 Rendered as the package's console-script entry point
        ├── init.py                 Rendered as `__init__.py` when Project Type == "Module"
        ├── setup.py                Template rendered into `setup.py` for the built package
        ├── README.md               Template rendered into the new project's README
        ├── .gitlab-ci.yml          Template copied when Repository Type == "GitLab"
        ├── .github/                Templates copied when Repository Type == "GitHub"
        │   ├── labels.yml
        │   └── workflows/publish.yml
        ├── ansi_escape              Regex pattern file used by `cli.filter`
        └── *.wav                    Sound effects used by `cli.sound` (start, ready, done, error, ask, set, unset)
```

## Entry point and dispatch (`clight/system/main.py`)

The console script `clight` maps to `clight.system.main:main`. `main.__init__` runs on every invocation:

1. **Catalog setup** — ensures `%USERPROFILE%\.clight` exists. This folder holds one `.bat` file per registered project.
2. **Environment setup** (`__loadEnvironment`) — on first run, adds the catalog folder to the user's `PATH` registry key (Windows) and asks the user to restart CMD. Subsequent runs skip this once the catalog path is already present.
3. **Project directory resolution** (`__projectDir`) — decides what "project" context this invocation is running in:
   - If `.system/sources/clight.json` exists in the current working directory, that's the active project (a CLight project itself, running its own commands like `version`/`publish`).
   - If the first CLI argument is `execute`, the project directory is derived from the `index.py` path passed as the second argument (this is how a generated project's `.bat` alias invokes CLight).
   - Otherwise, defaults to CLight's own identity (Name/Version/CMD/Author/Mail hardcoded in source) and current directory.
4. **Config load** (`__loadProject`) — loads `.system/sources/clight.json` into `self.params` if present.
5. **Signal handlers** — registers `SIGINT`/`SIGTERM` → `__shutDown`, which calls the running command's `__exit__` hook (if defined) before exiting.
6. **Banner + dispatch** — prints project name/version/author banner, then `__loadCommand` resolves `sys.argv[1:]` against methods on `self` (the `main` instance) and invokes the requested command.

## Command dispatch mechanics (`__loadCommand`)

- No arguments, or the command is `"help"`, or the method doesn't exist → prints the auto-generated help list (method names + trailing `# comment` docstrings extracted via regex from the source file).
- Otherwise resolves `getattr(object, cmd)` and calls it with the remaining `sys.argv` as positional string arguments.
- Return value convention: methods return a plain string.
  - String ending in `!` → printed via `cli.error` (with the `!` stripped, then re-appended by `cli.error`).
  - Any other non-empty string → printed via `cli.done` (green).
  - Empty/`None` → nothing printed (the command handled its own output).
- `TypeError`/generic `Exception` from the command are caught and reported via `cli.error` rather than crashing.

This same `__loadCommand`/help mechanism is reused for **generated projects** via the `execute` command (see below), so a generated project's `index.py` methods follow the identical convention (docstring comments become help text, return values become success/error messages).

## The catalog / registration mechanism

Every project gets a `.bat` file at `%USERPROFILE%\.clight\<CMD>.bat`:

```bat
@echo off
clight execute "<absolute path to project's .system/index.py>" %*
```

Because the catalog folder is on `PATH`, typing the project's own `CMD` alias anywhere in the shell invokes this `.bat`, which re-enters `clight` with the `execute` sub-command. `main.execute()`:

1. Resolves the project root from the given `index.py` path.
2. Loads `.system/sources/clight.json` as `self.called` (the project's own config).
3. Dynamically imports `.system/imports.py` (which pulls in `clight.system.importer.cli` plus the project's own pip/module imports) and then `.system/index.py`.
4. Instantiates `index(project_path, cwd, extra_args)` and dispatches the requested sub-command through the same `__loadCommand` logic used for CLight's own commands.
5. Refuses to run if `Project Type == "Module"` (modules are meant to be imported into an app, not executed directly).

`main.all()` lists every registered project by reading file names out of the catalog folder (minus the `.placeholder` and `.bat` extension). `main.remove(item)` deletes both the `.bat` file and the project's `clight.json` config (it does **not** delete the project's source files).

## Import pattern (`importer.py`)

Both CLight itself (`clight/system/importer.py`) and every generated project (`.system/imports.py`) follow the same pattern: a single file is the canonical place to `import` third-party and stdlib modules, plus `cli` and (for CLight itself) `SemVer`. Generated project code (`index.py`, custom modules) does `from imports import *` (or `from clight.system.importer import cli` in the raw skeleton) so that all needed names are available without each file repeating imports.

This is also what makes automatic dependency detection possible during packaging — see [Packaging & Publishing](06-packaging-and-publishing.md).

## Distinguishing "App" vs "Module" project types

Set during `clight new`/`reform` as `Project Type`:

- **App** — a full CLI application. `main.py` is rendered so the entry point directly instantiates and runs `index`.
- **Module** — a single importable pip package, not meant to be run as a CLI. When building (`__preparePackage` → `__renderModule`), the `.system` folder is renamed to `__system__`, import paths are rewritten (`from modules.` → `from .modules.`, `from imports import *` → `from <cmd>.__system__.imports import *`), and the package's `__init__.py` (rendered from `system/sources/init.py`) exposes every public attribute of an `index` instance at the package's top level via `globals()[item] = getattr(_obj_, item)`. Running it as a CLI via `execute` is explicitly blocked ("Modules should be imported into the project!").
