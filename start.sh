#!/usr/bin/env bash
# Exit on error
set -o errexit
python -m gunicorn core.asgi:application -k uvicorn.workers.UvicornWorker
