#! /usr/bin/env bash
set -e

python /code/app/app/celeryworker_pre_start.py

celery -A app.worker worker -l info -Q main-queue -c 1
