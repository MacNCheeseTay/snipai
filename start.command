#!/bin/bash
cd "$HOME/SnipAI" || { echo "Not installed. Run the install command from the README."; exit 1; }
pkill -f snipai_mac.py 2>/dev/null
export GEMINI_API_KEY="$(cat "$HOME/.snipai_key")"
nohup .venv/bin/python snipai_mac.py >snipai.log 2>&1 &
osascript -e 'display notification "Ctrl+Opt+A full screen, Ctrl+Opt+S snip" with title "SnipAI started"'
echo "SnipAI is running in the background. You can close this window."
