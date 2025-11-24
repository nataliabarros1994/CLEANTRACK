"""
Gunicorn Configuration for CleanTrack Production
"""
import multiprocessing
import os

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Restart workers after this many requests (to prevent memory leaks)
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/cleantrack/gunicorn_access.log"
errorlog = "/var/log/cleantrack/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "cleantrack"

# Server mechanics
daemon = False  # Systemd will handle daemonization
pidfile = "/var/run/cleantrack/gunicorn.pid"
user = "cleantrack"
group = "cleantrack"
umask = 0o007

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Environment
raw_env = [
    f"DJANGO_SETTINGS_MODULE=cleantrack.settings_production",
]
