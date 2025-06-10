# gunicorn.conf.py
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
#worker_class = "gevent"  # For async workers (install gevent if needed)
workers = 2  # Start with fewer workers for Render.com
timeout = 120
keepalive = 5
accesslog = "-"  # stdout
errorlog = "-"  # stdout
capture_output = True
loglevel = "info"


