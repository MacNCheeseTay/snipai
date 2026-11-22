# SnipAI

Hotkey screenshot or snip, sent to Gemini, answer shown in a small overlay that is click-through, has no taskbar entry, and is excluded from screen capture (Windows 10 2004+).

| Hotkey | Action |
|---|---|
| Ctrl+Alt+A | capture all screens |
| Ctrl+Alt+S | drag to snip a region (Esc cancels) |
| Ctrl+Alt+H | hide overlay |
| Ctrl+Alt+Q | quit |

## Install

1. Install Python 3 from python.org (tick "Add python.exe to PATH").
2. Download this repo (green Code button, Download ZIP) and unzip it.
3. Double-click `run.bat`. It installs everything and asks for your free Gemini key once (aistudio.google.com/apikey).

`SNIPAI_MODEL` overrides the model (default `gemini-2.5-flash`). `py test_snipai.py` runs a smoke test of hotkeys, capture, and snip with the API call mocked.

Windows: run.bat. macOS: run.command (untested, written without a Mac; see below).

## macOS

1. Install Python 3 from python.org.
2. Download and unzip the repo, then in Terminal run `chmod +x run.command` once and double-click it.
3. Allow Screen Recording and Accessibility for Terminal in System Settings > Privacy & Security, then run again.

Hotkeys are Ctrl+Opt+A / S / H / Q. Snip uses the native macOS region picker.

Do not use it where exam or interview rules prohibit outside help.
