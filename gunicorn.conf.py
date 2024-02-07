# gunicorn.conf
# 并行工作进程数
workers = 1
# 指定每个工作者的线程数
threads = 12
# 监听内网端口5000
bind = '0.0.0.0:5000'
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
# 设置访问日志和错误信息日志路径
errorlog = 'logs/error.log'
accesslog = 'logs/access.log'
#X-Forwarded-For header - - [date] "HTTP method request_URI HTTP version" status response_size "referer" "user_agent"
access_log_format = '"%({X-Forwarded-For}i)s" - - %(t)s "%(m)s %(U)s %(H)s" %(s)s %(b)s "%(f)s" "%(a)s"'
# 设置日志记录水平
loglevel = 'debug'
