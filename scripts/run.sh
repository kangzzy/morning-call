#!/bin/bash
cd "$(dirname "$0")/.."
source .venv/bin/activate
source .env 2>/dev/null
python -m morning_call.main

# Play the generated audio
TODAY=$(date +%Y-%m-%d)
AUDIO="output/${TODAY}_morning.mp3"
if [ -f "$AUDIO" ]; then
    afplay "$AUDIO"
fi
