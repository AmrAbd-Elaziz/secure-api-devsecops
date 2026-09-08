#!/bin/sh

set -eu

python -c "from app import initialize_database; initialize_database()"

exec gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 1 \
    --threads 4 \
    --access-logfile - \
    --error-logfile - \
    app:app