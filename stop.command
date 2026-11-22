#!/bin/bash
pkill -f snipai_mac.py && MSG="SnipAI stopped" || MSG="SnipAI was not running"
osascript -e "display notification \"$MSG\" with title \"SnipAI\""
echo "$MSG. You can close this window."
