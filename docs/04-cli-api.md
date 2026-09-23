# The `cli` Runtime API

`clight.system.modules.cli.cli` is a class of `staticmethod`-style functions (called on the class directly, e.g. `cli.info("...")`) shared by CLight itself and every generated project (via `from imports import *`). It centralizes terminal output, prompts, sound, speech, file I/O, encryption, and misc utilities.

## Output

| Method | Description |
|---|---|
| `cli.hint(message, update=False)` | Print in yellow. |
| `cli.done(message, update=False)` | Print in green (success). |
| `cli.info(message, update=False)` | Print in cyan. |
| `cli.error(message, update=False)` | Print in red, with a trailing `!` appended automatically. |
| `cli.trace(message)` | Print only when `cli.dev = True`; prefixed with `● `. Useful for developer-only diagnostic output. |
| `cli.line(color="", char="─")` | Print a full-terminal-width divider line, optionally colored. |
| `cli.unline(amount=1)` | Erase the previous `amount` printed lines (cursor-up + clear, enables Windows VT100 mode first). |

`update=True` on `hint`/`done`/`info`/`error` makes the line end with `\r` instead of `\n` (padded with spaces) so the next print overwrites it in place — useful for progress-style status updates, but only when `cli.dev` is `False`.

All output methods call `cli.pauseLoading()`/`cli.continueLoading()` around the print so they don't collide with an active spinner started by `cli.setLoading()`.

## User input

| Method | Description |
|---|---|
| `cli.input(hint="Enter", must=False)` | Free-text prompt. If `must`, re-prompts until non-empty. Plays the "ask" sound in voice mode. |
| `cli.selection(hint="Select", options=[], must=False)` | Single-choice list prompt (via `inquirer`). Adds a `"Skip"` option unless `must=True`; returns `""` if skipped or `options` is empty. |
| `cli.selections(hint="Select", options=[], must=False)` | Multi-choice checkbox prompt. If `must` and nothing selected, re-prompts recursively. |
| `cli.confirmation(hint="Confirm", must=False)` | y/n prompt, returns `bool`. If `must`, requires an explicit `y`. |
| `cli.clear()` | Clears the terminal (`cls` on Windows, `clear` elsewhere). |

In `cli.mode == "voice"`, `selection`/`selections`/`confirmation` also speak the prompt aloud via `cli.speak`.

## Data helpers

| Method | Description |
|---|---|
| `cli.value(key, data, default="")` | Safe dict/list lookup: returns `data[key]` if present (supports both string keys and integer indices for lists), else `default`. |
| `cli.isValue(value)` | Truthiness check. |
| `cli.isPath(path)` / `cli.isFile(path)` / `cli.isFolder(path)` | Existence checks via `os.path`. |
| `cli.chars(length=50)` | Random alphanumeric string of given length. |
| `cli.template(content, replacers={})` | Replaces every `{{key}}` placeholder in `content` with `str(replacers[key])`. This is the same templating mechanism CLight uses internally to render skeleton/source files. |

## File I/O

| Method | Description |
|---|---|
| `cli.read(file)` | Reads a file as UTF-8 (errors replaced), returns `""` if missing/not a file. |
| `cli.write(file, content)` | Overwrites (or creates) a file with `content`. Returns `False` if `file` is falsy, else the file path. |
| `cli.append(file, content, newline=True)` | Appends `content` to a file; prepends `\n` if the file already exists and `newline=True`. No-op if `content` is blank. |
| `cli.yaml(file)` | Reads and parses a YAML file into a dict (`{}` if missing/empty). |

## Sound & speech

| Method | Description |
|---|---|
| `cli.sound(name)` | Plays a bundled `.wav` from `system/sources/`: `start`, `ready`, `done`, `error`, `ask`, `set`, `unset`. Uses `pygame.mixer`. |
| `cli.speak(text, speed=None, voice=None)` | Text-to-speech via `pyttsx3`. Defaults to `cli.speed` (150) and `cli.voice` (index 1) class attributes if not overridden per call. |
| `cli.listen()` | Records from the microphone and transcribes via Google's speech recognition (`SpeechRecognition`). Plays `start`/`done`/`error` sounds around the attempt; returns the recognized text or `False` on failure/silence. |
| `cli.mode` | Class attribute, `"text"` (default) or `"voice"` — when `"voice"`, prompts also speak themselves aloud and play the "ask" sound. |

## Process execution

| Method | Description |
|---|---|
| `cli.execute(line, message="", background=False)` | Runs a shell command; `subprocess.run` (foreground, checked) or `subprocess.Popen` (`background=True`, fire-and-forget). Prints `message` via `cli.done` on success or `cli.error` on `CalledProcessError`. Returns `bool`. |
| `cli.command(line, wait=True, hide=False, location=".", get=False)` | Lower-level shell runner with finer control: `get=True` captures and returns stdout instead of streaming it; `hide=True` suppresses stdout/stderr; `wait=False` uses `Popen` instead of `run`; `location` sets the working directory (defaults to CWD). Always returns `""` unless `get=True`. |

## Encryption

| Method | Description |
|---|---|
| `cli.encrypt(text, key)` | Derives a Fernet key from `key` via PBKDF2-HMAC-SHA256 (100k iterations, random 16-byte salt), encrypts `text`, and returns `base64(salt + ciphertext)` as a string. Returns `""` on failure (logged via `cli.trace`). |
| `cli.decrypt(encrypted, key)` | Inverse of `encrypt` — extracts the salt, re-derives the key, and decrypts. Returns `""` on failure. |

This is exactly how CLight itself stores local PyPI credentials (`clight/system/sources/.pypi`), encrypted with a user-supplied Password Key.

## Text filtering

`cli.filter(text, length=1_000)` — sanitizes untrusted text before printing/using it: truncates to `length`, strips ANSI/OSC escape sequences (pattern loaded from `system/sources/ansi_escape`), Unicode-normalizes (NFC), drops control/format characters and bidirectional-override characters (keeping `@`/`&` as safe exceptions), and only allows a fixed set of ASCII letters/digits/punctuation plus newline/tab. Intended as a defensive measure against terminal-injection or spoofing via untrusted strings (e.g. text from external APIs or speech recognition).

## Progress bar & spinner

| Method | Description |
|---|---|
| `cli.setProgress(total=1, hint="")` | Initializes a progress bar out of `total` steps. |
| `cli.addProgress(done=1, hint="")` | Advances the bar by `done` steps and redraws (`\r`-based inline bar with `█`/`-` fill and percentage). |
| `cli.cutProgress()` | Clears the current progress line without finalizing. |
| `cli.endProgress(message="")` | Forces the bar to 100%, clears the line, and optionally prints `message` via `cli.info`. |
| `cli.setLoading(message="Loading")` | Starts a background daemon thread animating a `message ...` dot spinner. Ends any prior spinner first. |
| `cli.pauseLoading()` / `cli.continueLoading()` | Temporarily pause/resume the spinner (used internally by the output methods so prints don't collide with the spinner). |
| `cli.endLoading()` | Stops and joins the spinner thread. |

## Class attributes summary

| Attribute | Default | Purpose |
|---|---|---|
| `cli.mode` | `"text"` | `"voice"` enables spoken prompts. |
| `cli.speed` | `150` | Default TTS words-per-minute. |
| `cli.voice` | `1` | Default TTS voice index. |
| `cli.dev` | `False` | Enables `cli.trace` output and disables in-place (`update=True`) line overwriting. |
| `cli.load` | `{"done": 0, "total": 1, "hint": ""}` | Internal progress-bar state. |
