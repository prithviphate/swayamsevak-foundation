#!/bin/bash
set -e

echo "=== Creating virtual environment ==="
python3 -m venv .venv

echo "=== Installing dependencies ==="
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

echo "=== Collecting static files ==="
.venv/bin/python manage.py collectstatic --noinput --clear

echo "=== Build finished ===" 