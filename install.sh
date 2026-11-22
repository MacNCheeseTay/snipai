#!/bin/bash
# One-paste installer for macOS: curl -fsSL https://raw.githubusercontent.com/MacNCheeseTay/snipai/main/install.sh | bash
set -e
D="$HOME/SnipAI"
PY=""
for c in python3.14 python3.13 python3.12 python3.11 python3; do
  command -v $c >/dev/null && $c -c 'import sys; sys.exit(sys.version_info < (3, 11))' && PY=$c && break
done
[ -n "$PY" ] || { echo "Python 3.11 or newer is required (macOS's built-in Python is too old)."; echo "Install it from https://www.python.org/downloads/macos/ then paste the command again."; exit 1; }
mkdir -p "$D" && cd "$D"
curl -fsSL https://github.com/MacNCheeseTay/snipai/archive/refs/heads/main.tar.gz | tar xz --strip-components=1
rm -rf .venv
$PY -m venv .venv
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
