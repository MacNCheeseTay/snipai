#!/bin/bash
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null; then
  echo "Python 3 is not installed. Install it from https://www.python.org/downloads/macos/ then run this again."
  read -n 1 -s -r -p "Press any key to close"
  exit 1
fi
python3 -m venv .venv && .venv/bin/pip install -q -r requirements-mac.txt || { echo "Dependency install failed."; read -n 1 -s -r -p "Press any key to close"; exit 1; }
[ -f ~/.snipai_key ] && export GEMINI_API_KEY="$(cat ~/.snipai_key)"
if [ -z "$GEMINI_API_KEY" ]; then
  echo "Get a free key at https://aistudio.google.com/apikey"
  read -r -p "Paste your Gemini API key: " GEMINI_API_KEY
  echo "$GEMINI_API_KEY" > ~/.snipai_key && chmod 600 ~/.snipai_key
  export GEMINI_API_KEY
fi
echo "SnipAI running. Ctrl+Opt+A full screen, Ctrl+Opt+S snip, Ctrl+Opt+H hide, Ctrl+Opt+Q quit."
echo "First run: allow Screen Recording and Accessibility for Terminal in System Settings > Privacy & Security, then run again."
.venv/bin/python snipai_mac.py
