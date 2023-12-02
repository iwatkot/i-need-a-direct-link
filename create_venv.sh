#!/bin/bash

# Checking if .venv dir already exists.
if [ -d ".venv" ]; then
    echo "VENV dir (.venv) already exists, it will be removed."
    rm -rf .venv
fi

echo "VENV will be created"

# Creating VENV dir with selected python executable.
python3 -m venv .venv && \
source .venv/bin/activate && \

# Installing requirements from requirements.txt.
echo "Install requirements..." && \
pip3 install -r requirements.txt && \
echo "Requirements have been successfully installed, VENV ready." && \
deactivate
