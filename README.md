# SnipAI

Hotkey screenshot or snip, sent to Gemini, answer shown in a small overlay that is click-through, has no taskbar entry, and is excluded from screen capture (Windows 10 2004+).

| Hotkey | Action |
|---|---|
| Ctrl+Alt+A | capture all screens |
| Ctrl+Alt+S | drag to snip a region (Esc cancels) |
| Ctrl+Alt+H | hide overlay |
| Ctrl+Alt+Q | quit |

## Install

1. Install Python 3.11 or newer from python.org (tick "Add python.exe to PATH").
2. Download this repo (green Code button, Download ZIP) and unzip it.
3. Double-click `run.bat`. It installs everything and asks for your free Gemini key once (aistudio.google.com/apikey).

`SNIPAI_MODEL` overrides the model (default `gemini-3.8-flash`). `py test_snipai.py` runs a smoke test of hotkeys, capture, and snip with the API call mocked.

Windows: `run.bat`. macOS: see below (untested, written without a Mac).

## macOS

1. Install Python 3.11 or newer from python.org (the Python that comes with macOS is too old).
2. Open Terminal (Cmd+Space, type Terminal) and paste:

```
curl -fsSL https://raw.githubusercontent.com/MacNCheeseTay/snipai/main/install.sh | bash
```

3. Double-click **SnipAI Start** on your Desktop to turn it on, **SnipAI Stop** to shut it down completely. (If macOS blocks it the first time: right-click, Open.)
4. First start: allow Screen Recording and Accessibility for Terminal in System Settings > Privacy & Security.

Hotkeys are Ctrl+Opt+Cmd+A / S / H / Q (hold Control, Option and Command together). Snip uses the native macOS region picker.

Do not use it where exam or interview rules prohibit outside help.
