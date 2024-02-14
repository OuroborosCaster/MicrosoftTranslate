import settings

# gunicorn.conf
# 并行工作进程数
workers = settings.workers
# 指定每个工作者的线程数
threads = settings.threads
# 监听内网端口5000
bind = settings.ip+':'+settings.port
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
# 设置访问日志和错误信息日志路径
accesslog = settings.accesslog
errorlog = settings.errorlog
#X-Forwarded-For header - - [date] "HTTP method request_URI HTTP version" status response_size "referer" "user_agent"
access_log_format = settings.access_log_format
# 设置日志记录水平
loglevel = settings.loglevel
