#!/bin/bash
set -e

echo "=== Ensuring pip ==="
python3 -m ensurepip --upgrade || true
python3 -m pip install --upgrade pip || true

echo "=== Installing dependencies ==="
python3 -m pip install -r requirements.txt

echo "=== Collecting static files ==="
python3 manage.py collectstatic --noinput --clear

echo "=== Build finished ==="
