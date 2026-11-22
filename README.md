# SnipAI

Hotkey screenshot or snip, sent to Gemini, answer shown in a small overlay that is click-through, has no taskbar entry, and is excluded from screen capture (Windows 10 2004+).

| Hotkey | Action |
|---|---|
| Ctrl+Alt+A | capture all screens |
| Ctrl+Alt+S | drag to snip a region (Esc cancels) |
| Ctrl+Alt+H | hide overlay |
| Ctrl+Alt+Q | quit |

```
pip install -r requirements.txt
set GEMINI_API_KEY=your-key   (free key: aistudio.google.com)
py snipai.py
```

`SNIPAI_MODEL` overrides the model (default `gemini-2.5-flash`). `py test_snipai.py` runs a smoke test of hotkeys, capture, and snip with the API call mocked.

Windows only. Do not use it where exam or interview rules prohibit outside help.
