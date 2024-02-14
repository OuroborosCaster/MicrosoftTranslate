#!/bin/sh

gunicorn -c gunicorn.conf.py app:app

tail -f /app/logs/access.log &
tail -f /app/logs/error.log &
