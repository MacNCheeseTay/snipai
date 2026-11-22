#!/bin/bash
# One-paste installer for macOS: curl -fsSL https://raw.githubusercontent.com/MacNCheeseTay/snipai/main/install.sh | bash
set -e
D="$HOME/SnipAI"
command -v python3 >/dev/null || { echo "Install Python 3 first: https://www.python.org/downloads/macos/ then paste the command again."; exit 1; }
mkdir -p "$D" && cd "$D"
curl -fsSL https://github.com/MacNCheeseTay/snipai/archive/refs/heads/main.tar.gz | tar xz --strip-components=1
python3 -m venv .venv
.venv/bin/pip install -q -r requirements-mac.txt
if [ ! -s "$HOME/.snipai_key" ]; then
  echo "Get a free key at https://aistudio.google.com/apikey"
  read -r -p "Paste your Gemini API key: " KEY </dev/tty
  echo "$KEY" > "$HOME/.snipai_key" && chmod 600 "$HOME/.snipai_key"
fi
chmod +x start.command stop.command
cp start.command "$HOME/Desktop/SnipAI Start.command"
cp stop.command "$HOME/Desktop/SnipAI Stop.command"
echo
echo "Done. Double-click 'SnipAI Start' and 'SnipAI Stop' on your Desktop."
echo "First start: allow Screen Recording and Accessibility for Terminal in System Settings > Privacy & Security."
