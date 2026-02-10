#!/usr/bin/env bash
# Build script for Railway / Render
# Runs during deploy: installs deps, collects static files, runs migrations

set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
