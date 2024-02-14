#!/bin/sh

gunicorn -c gunicorn.conf.py app:app

tail -f ./logs/access.log > /dev/stdout &
tail -f ./logs/error.log > /dev/stderr &