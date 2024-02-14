#!/bin/sh

gunicorn -c gunicorn.conf.py app:app > /dev/stdout 2> /dev/stderr