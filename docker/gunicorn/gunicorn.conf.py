import multiprocessing
import os

bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"
workers = int(os.getenv("GUNICORN_WORKERS", "1"))
threads = int(os.getenv("GUNICORN_THREADS", "2"))
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "gthread")
timeout = 120
graceful_timeout = 30
keepalive = 5
accesslog = "-"
errorlog = "-"
capture_output = True
