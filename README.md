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

Windows only. Do not use it where exam or interview rules prohibit outside help.
