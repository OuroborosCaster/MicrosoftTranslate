#!/bin/sh

gunicorn -c gunicorn.conf.py app:app

ln -sf /dev/stdout /app/logs/access.log && ln -sf /dev/stderr /app/logs/error.log &
