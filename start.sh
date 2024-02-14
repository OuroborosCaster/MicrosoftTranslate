#!/bin/sh

ln -sf /dev/stdout /app/logs/access.log && ln -sf /dev/stderr /app/logs/error.log &

gunicorn -c gunicorn.conf.py app:app