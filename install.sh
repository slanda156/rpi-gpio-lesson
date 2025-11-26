#!/bin/sh
set -e

FORCE=0
[ "$1" = "--force" ] && FORCE=1

# Check if .venv exists
if [ -d ".venv" ]; then
    if [ $FORCE -eq 0 ]; then
        echo ".venv already exists. Skipping creation."
    else
        echo "Overriding: recreating .venv..."
        python -m virtualenv .venv
    fi
else
    echo "Creating virtual environment..."
    python -m virtualenv .venv
fi

# Activate and install
. .venv/bin/activate

pip install pip-tools
pip-compile
pip-sync
