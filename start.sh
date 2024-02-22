#!/bin/sh

# 启动你的应用
gunicorn -c gunicorn.conf.py main:app &

# 实时查看访问日志文件的内容，并输出到STDOUT
tail -f logs/access.log &

# 实时查看错误日志文件的内容，并输出到STDERR
tail -f logs/error.log >&2 &

# 等待所有后台进程
wait
